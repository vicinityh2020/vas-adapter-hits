from django.contrib import admin
from .models import ParkingSpace, ParkingLot, ParkingReservation

admin.site.register(ParkingSpace)
admin.site.register(ParkingLot)
admin.site.register(ParkingReservation)
