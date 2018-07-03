from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ParkingSpace, ParkingReservation
from .serializers import ParkingSpaceSerializer, ParkingReservationSerializer
from .converters import ReservationConverter

from datetime import datetime

import rest_framework.status as status


class ParkingSpaceView(APIView):
    r = {
        "error": {},
        "message": 'success',
        "status": "OK",
    }

    def get(self, request, parking_lot_id, from_time, to_time):
        allstuff = ParkingSpace.objects.all()
        return Response(self.r, status=status.HTTP_200_OK)


class ObjectsView(APIView):
    service_object_descriptor = {
        "adapter-id": "vas-hits-uc1",
        "thing-descriptions": [
            {
                "oid": "ae66d461-7545-42b6-8951-5ea593156bd8",
                "name": "HITS - VAS Adapter",
                "type": "core:Service",
                "version": "0.1b",
                "keywords": [],
                "properties": [],
                "events": [],
                "actions": []
            }
        ]
    }

    def get(self, request):
        return Response(self.service_object_descriptor, status=status.HTTP_200_OK)


class StatusView(APIView):
    r = {
        "error": {},
        "message": 'success',
        "status": "OK",
    }

    def get(self, request):
        return Response(self.r, status=status.HTTP_200_OK)


class ParkingReservationView(APIView):

    r = {
        "error": False,
        "message": 'success',
        "status": status.HTTP_200_OK,
    }

    @csrf_exempt
    def post(self, request, parking_slot_id):
        try:
            parking_space = ParkingSpace.objects.get(parking_space_id=parking_slot_id)
        except ParkingSpace.DoesNotExist:
            self.r["error"] = True
            self.r["message"] = 'Invalid parking id'
            self.r["status"] = status.HTTP_404_NOT_FOUND
            return Response(self.r, status=status.HTTP_404_NOT_FOUND)

        from_time = ReservationConverter.seconds_to_time(request.data['from'])
        to_time = ReservationConverter.seconds_to_time(request.data['to'])

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