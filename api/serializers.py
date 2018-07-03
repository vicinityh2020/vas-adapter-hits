from rest_framework import serializers
from .models import ParkingSpace, ParkingLot, ParkingReservation


class ParkingSpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSpace
        fields = '__all__'
        read_only_fields = ('date_created', 'date_modified',)


class ParkingLotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingLot
        fields = '__all__'
        read_only_fields = ('date_created', 'date_modified',)


class ParkingReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingReservation
        fields = '__all__'
        read_only_fields = ('date_created', 'date_modified',)
