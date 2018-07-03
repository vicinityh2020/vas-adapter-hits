from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ParkingSpace, ParkingReservation
from .serializers import ParkingSpaceSerializer

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
        "error": {},
        "message": 'success',
        "status": "OK",
    }

    @csrf_exempt
    def post(self, request, parking_space_id, res_date, from_time, to_time):
        all_reservations = ParkingReservation.objects.all()
        print('hi')
        return Response(self.r, status=status.HTTP_200_OK)