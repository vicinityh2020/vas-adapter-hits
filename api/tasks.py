# Create your tasks here
from __future__ import absolute_import, unicode_literals

from datetime import timedelta, time, datetime, timezone

from .models import ParkingReservation, ParkingSpace
from celery import shared_task

@shared_task
def pulse_lamp():
    print("Pulsing ...")
    last_update_threshold = 10

    parking_space_queryset = ParkingSpace.objects.all()
    for parking_space in parking_space_queryset:
        # send error signal if status is recalibrating or last update was more than 10 minutes ago
        if parking_space.sensor_status == 'Recalibrating' \
                or datetime.now(timezone.utc) - parking_space.date_modified > timedelta(minutes=last_update_threshold):
            # TODO: push web message ERROR signal
            # TODO: push yellow light color
            print("Houston, we have a problem")
            return True
    return False