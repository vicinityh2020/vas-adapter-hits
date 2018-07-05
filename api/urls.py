from django.urls import path

from . import views

urlpatterns = [
    path('objects', views.ObjectsView.as_view(), name='objects_view'),
    path('status', views.StatusView.as_view(), name='status_view'),
    path('view/parking-slots/<int:parking_slot_id>', views.view_parking_space,
         name='parking_space_view'),
    path('reserve/parking-slots/<int:parking_slot_id>',
         views.reserve_parking, name='parking_reservation_view'),
    path('cancel/parking-res/<res_id>',
         views.cancel_reservation, name='parking_reservation_cancel')
]
