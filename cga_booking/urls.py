from django.urls import path, include

from cga_booking.views import HotelsView, HotelInfoView, HotelUpdateView, \
    RoomAddView,\
    hotel_attraction_add

urlpatterns = [
    path('hotel/', include([
        path('all', HotelsView.as_view(), name='hotels'),
        path('<slug:slug>/', include([
            path('info', HotelInfoView.as_view(), name='hotel_info'),
            path('update', HotelUpdateView.as_view(), name='hotel_update'),

            path('room/', include([
                path('add', RoomAddView.as_view(), name='room_add'),
            ])),

            path('attraction/', include([
                path('add', hotel_attraction_add, name='hotel_attraction_add'),
            ]))
        ]))
    ])),
]