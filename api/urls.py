from django.urls import path

from . import views

urlpatterns = [
    path('objects', views.ObjectsView.as_view(), name='objects_view'),
    path('status', views.StatusView.as_view(), name='status_view'),
    path('parking-lots/<parking_lot_id>/from/<int:from_time>/to/<int:to_time>', views.ParkingSpaceView.as_view(),
         name='parking_space_view'),
]