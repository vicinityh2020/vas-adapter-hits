from django.contrib import admin
from .models import ParkingSpace, ParkingLot, ParkingReservation


class ParkingReservationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ParkingReservation._meta.get_fields()]


admin.site.register(ParkingSpace)
admin.site.register(ParkingLot)
admin.site.register(ParkingReservation, ParkingReservationAdmin)
