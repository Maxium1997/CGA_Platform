from django.shortcuts import render
from django.views.generic import ListView, DetailView

from ocean_station.models import Station
from ocean_station.definitions import Region

# Create your views here.


class OceanStationsView(ListView):
    model = Station
    template_name = 'ocean_station/all.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(IndexView, self).get_context_data(object_list=None, **kwargs)
        context['stations'] = Station.objects.order_by('region')
        context['regions'] = Region.__members__.values()
        return context


class RegionStationsView():
    pass


class StationInfoView():
    pass
