from datetime import datetime, time, timedelta

import json
import rest_framework.status as status
from django.db.models import Q
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView

from .converters import conv
from .models import ParkingSpace, ParkingReservation
from .serializers import ParkingReservationSerializer


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
        res_queryset = ParkingReservation.objects.filter(parking_space=parking_slot)

    except ParkingReservation.DoesNotExist:
        response['body'].append({
            'start_time': conv.seconds_to_time(request.data['from']),
            'end_time': conv.seconds_to_time(request.data['to']),
        })

        return JsonResponse(response, status=status.HTTP_200_OK)

    except ParkingSpace.DoesNotExist:
        response['error'] = True
        response['message'] = 'Invalid parking id'
        response['status'] = status.HTTP_404_NOT_FOUND
        return JsonResponse(response, status=status.HTTP_404_NOT_FOUND)

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
        return JsonResponse(response, status.HTTP_200_OK)

    sorted_queryset = sorted_queryset.filter(time_start__gt=min_from, time_expire__lt=max_to)

    if len(sorted_queryset) == 0:
        return JsonResponse(response, status=status.HTTP_200_OK)

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

    return JsonResponse(response, status=status.HTTP_200_OK)

# class ParkingSpaceView(APIView):
#
#     def post(self, request, parking_slot_id):
#
#         response = {
#             'error': False,
#             'message': 'success',
#             'status': status.HTTP_200_OK,
#             'body': [],
#         }
#
#         try:
#             parking_slot = ParkingSpace.objects.get(parking_space_id=parking_slot_id)
#             res_queryset = ParkingReservation.objects.filter(parking_space=parking_slot)
#
#         except ParkingReservation.DoesNotExist:
#             response['body'].append({
#                 'start_time': conv.seconds_to_time(request.data['from']),
#                 'end_time': conv.seconds_to_time(request.data['to']),
#             })
#
#             return Response(response, status=status.HTTP_200_OK)
#
#         except ParkingSpace.DoesNotExist:
#             response['error'] = True
#             response['message'] = 'Invalid parking id'
#             response['status'] = status.HTTP_404_NOT_FOUND
#             return Response(response, status=status.HTTP_404_NOT_FOUND)
#
#         sorted_queryset = res_queryset.order_by('time_start')
#
#         min_from = conv.seconds_to_time(request.data['from'])
#         max_to = conv.seconds_to_time(request.data['to'])
#
#         for entry in sorted_queryset:
#             if entry.time_start <= min_from <= entry.time_expire:
#                 min_from = entry.time_expire
#             if entry.time_start <= max_to <= entry.time_expire:
#                 max_to = entry.time_start
#
#         max_to_seconds = conv.time_to_seconds(max_to)
#         min_from_seconds = conv.time_to_seconds(min_from)
#
#         if (max_to_seconds - min_from_seconds) < 0:
#             return Response(response, status.HTTP_200_OK)
#
#         sorted_queryset = sorted_queryset.filter(time_start__gt=min_from, time_expire__lt=max_to)
#
#         if len(sorted_queryset) == 0:
#             return Response(response, status=status.HTTP_200_OK)
#
#         start = min_from_seconds + 60
#         end = conv.time_to_seconds(sorted_queryset.first().time_start)
#
#         # at least 2 minutes in between reservations
#         if (end - start) > 120:
#             response['body'].append({
#                 'sensor_id': parking_slot.parking_space_id,
#                 'street_address': 'Mosseveien 18A',
#                 'price_per_minute': 0.11,
#                 'distance_in_km': 0.6,
#                 'start_time': conv.seconds_to_time(start),
#                 'end_time': conv.seconds_to_time(end - 60),
#             })
#
#         res_count = len(sorted_queryset)
#         for i in range(res_count):
#             start = conv.time_to_seconds(sorted_queryset[i].time_expire)
#
#             end = max_to if (i == res_count - 1) else sorted_queryset[i + 1].time_start
#             end = conv.time_to_seconds(end)
#
#             if (end - start) > 120:
#                 response['body'].append({
#                     'sensor_id': parking_slot.parking_space_id,
#                     'street_address': 'Mosseveien 18A',
#                     'price_per_minute': 0.11,
#                     'distance_in_km': 0.6,
#                     'start_time': conv.seconds_to_time(start + 60),
#                     'end_time': conv.seconds_to_time(end - 60),
#                 })
#
#         return Response(response, status=status.HTTP_200_OK)


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


class ParkingReservationView(APIView):
    r = {
        'error': False,
        'message': 'success',
        'status': status.HTTP_200_OK,
    }

    @csrf_exempt
    def post(self, request, parking_slot_id):
        try:
            parking_space = ParkingSpace.objects.get(parking_space_id=parking_slot_id)
        except ParkingSpace.DoesNotExist:
            self.r['error'] = True
            self.r['message'] = 'Invalid parking id'
            self.r['status'] = status.HTTP_404_NOT_FOUND
            return Response(self.r, status=status.HTTP_404_NOT_FOUND)

        from_time = conv.seconds_to_time(request.data['from'])
        to_time = conv.seconds_to_time(request.data['to'])

        reservation_json = {
            'username': 'testuser',
            'parking_space_id': parking_slot_id,
            'date': datetime.strptime(request.data['date'], '%d-%m-%Y').date(),
            'time_start': from_time,
            'time_expire': to_time,
        }

        serialized_reservation = ParkingReservationSerializer(data=reservation_json)

        if serialized_reservation.is_valid():
            serialized_reservation.save()
        else:
            print('Serialization is not valid')

        return Response(self.r, status=status.HTTP_200_OK)
