from django.urls import path, include

from cga_booking.views import HotelsView, HotelInfoView, HotelUpdateView, \
    RoomAddView, RoomUpdateView, RoomReservationView, \
    RoomReservationsView, RoomReservationInfoView, RoomReservationFeaturesView,\
    hotel_attraction_add

urlpatterns = [
    path('hotel/', include([
        path('all', HotelsView.as_view(), name='hotels'),
        path('<slug:slug>/', include([
            path('info', HotelInfoView.as_view(), name='hotel_info'),
            path('update', HotelUpdateView.as_view(), name='hotel_update'),

            path('room/', include([
                path('add', RoomAddView.as_view(), name='room_add'),
                path('<pk>', RoomReservationView.as_view(), name='room_reservation'),
                path('<pk>/', include([
                    path('update', RoomUpdateView.as_view(), name='room_update'),
                ]))
            ])),

            path('attraction/', include([
                path('add', hotel_attraction_add, name='hotel_attraction_add'),
            ]))
        ]))
    ])),

    path('<str:username>/', include([
        path('reservations', RoomReservationsView.as_view(), name='room_reservations'),
        path('reservations/', include([
            path('<serial_number>/', include([
                path('info', RoomReservationInfoView.as_view(), name='room_reservation_info'),
                path('features', RoomReservationFeaturesView.as_view(), name='room_reservation_features'),
            ])),
        ])),
    ])),
]
