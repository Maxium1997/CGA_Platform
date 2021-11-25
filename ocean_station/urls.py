from django.urls import path, include

from ocean_station.views import OceanStationsView, RegionStationsView, StationInfoView

urlpatterns = [
    path('ocean_station/', include([
        path('all', OceanStationsView.as_view(), name='ocean_stations'),
        path('<str:region>', RegionStationsView.as_view(), name='region_stations'),
        path('<slug:slug>/', include([
            path('info', StationInfoView.as_view(), name='station_info'),
        ]))
    ])),
]
