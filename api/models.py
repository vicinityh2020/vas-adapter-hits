from .converters import conv
from django.db import models


class ParkingLot(models.Model):

    latitude = models.FloatField(null=False)
    longitude = models.FloatField(null=False)
    lot_id = models.CharField(max_length=255, blank=False, unique=True)
    lot_name = models.CharField(max_length=255, default=None)
    street_address = models.CharField(max_length=512, null=True, default=None)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.lot_name)


class ParkingSpace(models.Model):

    UNKNOWN = 'Unknown'
    VACANT = 'Vacant'
    OCCUPIED = 'Occupied'
    STATUS_CHOICES = (
        (UNKNOWN, 'Unknown'),
        (VACANT, 'Vacant'),
        (OCCUPIED, 'Occupied'),
    )

    oid = models.UUIDField(default=None, editable=True)
    parking_lot = models.ForeignKey(ParkingLot, null=True, on_delete=models.CASCADE)

    mac_address = models.CharField(primary_key=True, default=None, max_length=255)
    parking_space_id = models.CharField(max_length=255, unique=True, default=None)
    car_counter = models.IntegerField(null=True)
    car_presence = models.IntegerField(null=False, default=0)
    sensor_status = models.CharField(max_length=255, choices=STATUS_CHOICES, default=UNKNOWN)

    published = models.BooleanField(default=False, null=False)
    available_from = models.TimeField(null=True)
    available_to = models.TimeField(null=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.parking_space_id)

    def is_vacant_now(self):
        return self.sensor_status == self.VACANT

    def is_available(self, from_time, to_time):
        return self.published and self.__within_time_range(from_time, to_time)

    def __within_time_range(self, from_time, to_time):
        return (from_time >= self.available_from) and (to_time <= self.available_to)


class ParkingReservation(models.Model):

    id = models.BigAutoField(primary_key=True)
    parking_space = models.ForeignKey(ParkingSpace, null=True, on_delete=models.CASCADE)

    reservation_unique = models.CharField(max_length=16, default=conv.generate_unique_res)
    username = models.CharField(max_length=255, default=None)

    date = models.DateField(default=None)

    time_start = models.TimeField(default=None)
    time_expire = models.TimeField(default=None)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.parking_space)
