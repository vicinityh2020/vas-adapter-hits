import json
from datetime import datetime, timezone, timedelta

import requests
import rest_framework.status as status
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView

from .converters import conv
from .models import ParkingSpace, ParkingReservation


@csrf_exempt
def cancel_reservation(request, res_id):
    response = {
        'error': False,
        'message': 'success',
        'status': status.HTTP_200_OK,
        'body': [],
    }

    try:
        reservation = ParkingReservation.objects.get(reservation_unique=res_id)

    except ParkingReservation.DoesNotExist:
        response['error'] = True
        response['message'] = 'No reservation with id {}'.format(res_id)
        response['status'] = status.HTTP_404_NOT_FOUND
        return response

    reservation.delete()

    return JsonResponse(data=response, status=status.HTTP_200_OK)


@csrf_exempt
def view_parking_space(request, parking_slot_id):
    response = {
        'error': False,
        'message': 'success',
        'status': status.HTTP_200_OK,
        'body': [],
    }

    try:
        request.data = json.loads(request.body)

        parking_slot = ParkingSpace.objects.get(parking_space_id=parking_slot_id)

        # control lower boundaries
        af = conv.time_to_seconds(parking_slot.available_from)
        at = conv.time_to_seconds(parking_slot.available_to)
        request.data['from'] = request.data['from'] if request.data['from'] > af \
            else af

        # control upper boundaries
        request.data['to'] = request.data['to'] if request.data['to'] < at \
            else at

        res_queryset = ParkingReservation.objects.filter(parking_space=parking_slot)

    except ParkingReservation.DoesNotExist:
        response['body'].append({
            'start_time': conv.seconds_to_time(request.data['from']),
            'end_time': conv.seconds_to_time(request.data['to']),
        })

        return JsonResponse(data=response, status=status.HTTP_200_OK)

    except ParkingSpace.DoesNotExist:
        response['error'] = True
        response['message'] = 'Invalid parking id'
        response['status'] = status.HTTP_404_NOT_FOUND
        return JsonResponse(data=response, status=status.HTTP_404_NOT_FOUND)

    if len(res_queryset) == 0:
        # no reservations. Return full day!
        response['body'].append({
            'sensor_id': parking_slot.parking_space_id,
            'street_address': 'Mosseveien 18A',
            'price_per_minute': 0.11,
            'distance_in_km': 0.6,
            'start_time': parking_slot.available_from,
            'end_time': parking_slot.available_to,
        })
        return JsonResponse(data=response, status=status.HTTP_200_OK)

    sorted_queryset = res_queryset.order_by('time_start')

    min_from = conv.seconds_to_time(request.data['from'])
    max_to = conv.seconds_to_time(request.data['to'])

    for entry in sorted_queryset:
        if entry.time_start <= min_from <= entry.time_expire:
            min_from = entry.time_expire
        if entry.time_start <= max_to <= entry.time_expire:
            max_to = entry.time_start

    max_to_seconds = conv.time_to_seconds(max_to)
    min_from_seconds = conv.time_to_seconds(min_from)

    if (max_to_seconds - min_from_seconds) < 0:
        return JsonResponse(data=response, status=status.HTTP_200_OK)

    sorted_queryset = sorted_queryset.filter(time_start__gt=min_from, time_expire__lt=max_to)

    if len(sorted_queryset) == 0:
        response['body'].append({
            'sensor_id': parking_slot.parking_space_id,
            'street_address': 'Mosseveien 18A',
            'price_per_minute': 0.11,
            'distance_in_km': 0.6,
            'start_time': min_from,
            'end_time': max_to,
        })
        return JsonResponse(data=response, status=status.HTTP_200_OK)

    start = min_from_seconds + 60
    end = conv.time_to_seconds(sorted_queryset.first().time_start)

    # at least 2 minutes in between reservations
    if (end - start) > 120:
        response['body'].append({
            'sensor_id': parking_slot.parking_space_id,
            'street_address': 'Mosseveien 18A',
            'price_per_minute': 0.11,
            'distance_in_km': 0.6,
            'start_time': conv.seconds_to_time(start),
            'end_time': conv.seconds_to_time(end - 60),
        })

    res_count = len(sorted_queryset)
    for i in range(res_count):
        start = conv.time_to_seconds(sorted_queryset[i].time_expire)

        end = max_to if (i == res_count - 1) else sorted_queryset[i + 1].time_start
        end = conv.time_to_seconds(end)

        if (end - start) > 120:
            response['body'].append({
                'sensor_id': parking_slot.parking_space_id,
                'street_address': 'Mosseveien 18A',
                'price_per_minute': 0.11,
                'distance_in_km': 0.6,
                'start_time': conv.seconds_to_time(start + 60),
                'end_time': conv.seconds_to_time(end - 60),
            })

    return JsonResponse(data=response, status=status.HTTP_200_OK)


class ObjectsView(APIView):
    service_object_descriptor = {
        'adapter-id': 'vas-hits-uc1',
        'thing-descriptions': [
            {
                'oid': 'ae66d461-7545-42b6-8951-5ea593156bd8',
                'name': 'HITS - VAS Adapter',
                'type': 'core:Service',
                'version': '0.1b',
                'keywords': [],
                'properties': [],
                'events': [],
                'actions': []
            }
        ]
    }

    def get(self, request):
        return Response(self.service_object_descriptor, status=status.HTTP_200_OK)


class StatusView(APIView):
    r = {
        'error': False,
        'message': 'success',
        'status': 'OK',
    }

    def get(self, request):
        return Response(self.r, status=status.HTTP_200_OK)


@csrf_exempt
def reserve_parking(request, parking_slot_id):
    r = {
        'error': False,
        'message': 'success',
        'status': status.HTTP_200_OK,
        'body': {},
    }

    try:
        request.data = json.loads(request.body)
        parking_space = ParkingSpace.objects.get(parking_space_id=parking_slot_id)
    except ParkingSpace.DoesNotExist:
        r['error'] = True
        r['message'] = 'Invalid parking id'
        r['status'] = status.HTTP_404_NOT_FOUND
        return Response(r, status=status.HTTP_404_NOT_FOUND)

    from_time = conv.seconds_to_time(request.data['from'])
    to_time = conv.seconds_to_time(request.data['to'])

    serialized_reservation = ParkingReservation(
        parking_space=parking_space,
        username='testuser',
        date=datetime.strptime(request.data['date'], '%Y-%m-%d').date(),
        time_start=from_time,
        time_expire=to_time,
        reservation_unique=conv.generate_unique_res()
    )

    serialized_reservation.save()

    r['body'] = {
        'unique_res_id': serialized_reservation.reservation_unique,
        'time_start': from_time,
        'time_expure': to_time,
        'date': serialized_reservation.date,
    }

    return JsonResponse(data=r, status=status.HTTP_200_OK)


@csrf_exempt
def sensor_event(request, subscriber_id, eid):
    try:
        request.data = json.loads(request.body)
        parking_space = ParkingSpace.objects.get(mac_address=request.data['sensor_id'])
    except ParkingSpace.DoesNotExist as e:
        print(e)
        return JsonResponse(data={}, status=status.HTTP_404_NOT_FOUND)
    except json.JSONDecodeError as e:
        print(e)
        return JsonResponse(data={}, status=status.HTTP_400_BAD_REQUEST)

    s = request.data['value']
    parking_space.sensor_status = s
    parking_space.save()

    lamp_id = 'eefb800a-24c6-4206-b112-ff6caffa9cc8' # TODO: replace with database entry

    url = 'http://127.0.0.1:9998/agent/remote/objects/{}/properties/color'.format(lamp_id)
    h = {
        'infrastructure-id': 'ae66d461-7545-42b6-8951-5ea593156bd8',
        'adapter-id': 'vas-hits-uc1',
        'Content-Type': 'application/json',
    }

    if  s == 'Occupied':
        requests.put(url=url, json={'color': 'red', 'blink': False}, headers=h)
    elif s == 'Vacant':
        a = requests.put(url=url, json={'color': 'green', 'blink': False}, headers=h)
        print(a)
    else:
        requests.put(url=url, json={'color': 'yellow', 'blink': False}, headers=h)

    return JsonResponse(data={}, status=status.HTTP_200_OK)