from django.urls import path, include

from ocean_station.views import OceanStationsView, RegionStationsView, StationInfoView, \
    StationUpdateView, StationContentView, StationContentUpdateView, StationContentDelView, \
    content_add, attraction_add

urlpatterns = [
    path('ocean_station', OceanStationsView.as_view(), name='ocean_stations'),
    path('ocean_station/', include([
        path('<str:region>', RegionStationsView.as_view(), name='region_stations'),
        path('<slug:slug>/', include([
            path('info', StationInfoView.as_view(), name='station_info'),
            path('update', StationUpdateView.as_view(), name='station_update'),
            path('content/', include([
                path('list', StationContentView.as_view(), name='station_contents'),
                path('add', content_add, name='content_add'),
                path('<id>/', include([
                    path('edit', StationContentUpdateView.as_view(), name='content_edit'),
                    path('delete', StationContentDelView.as_view(), name='content_del'),
                ])),
            ])),
            path('attraction/', include([
                path('add', attraction_add, name='attraction_add'),
            ]))
        ]))
    ])),
]
