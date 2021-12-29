from django.urls import path, include

from cga_booking.views import HotelsView, HotelInfoView

urlpatterns = [
    path('hotel/', include([
        path('all', HotelsView.as_view(), name='hotels'),
        path('<slug:slug>/', include([
            path('info', HotelInfoView.as_view(), name='hotel_info'),
            # path('update', HotelUpdateView.as_view(), name='hotel_update'),
        ]))
    ])),
]