from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.contrib import messages


from django.db.models import Q

from ocean_station.models import Station
from ocean_station.definitions import Region, ContentFlag, PhotoFlag
from ocean_station.forms import StationUpdateForm

# Create your views here.


class OceanStationsView(ListView):
    model = Station
    template_name = 'ocean_station/all.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(OceanStationsView, self).get_context_data(object_list=None, **kwargs)
        context['stations'] = Station.objects.order_by('region')
        context['regions'] = [[_.value[0], _.value[1], _.value[2]] for _ in Region.__members__.values()][1:]
        return context


class RegionStationsView(ListView):
    model = Station
    template_name = 'ocean_station/regions.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RegionStationsView, self).get_context_data(object_list=None, **kwargs)
        region_code = [_.value[1] for _ in Region.__members__.values()].index(self.kwargs.get('region'))
        context['region_code'] = region_code
        context['stations'] = Station.objects.filter(region=region_code)
        context['regions'] = [[_.value[0], _.value[1], _.value[2]] for _ in Region.__members__.values()][1:]
        return context


class StationInfoView(DetailView):
    model = Station
    template_name = 'ocean_station/info.html'

    def get_context_data(self, **kwargs):
        context = super(StationInfoView, self).get_context_data(**kwargs)
        try:
            context['overviews'] = self.get_object(). \
                introductions.filter(content_flag=ContentFlag.Overview.value[0]).order_by('sequence', 'id')
        except ObjectDoesNotExist:
            context['overviews'] = None
        try:
            filter_criteria = Q(photo_flag=PhotoFlag.Main.value[0]) | Q(photo_flag=PhotoFlag.Display.value[0])
            context['album'] = self.get_object().\
                album.filter(filter_criteria)
        except ValueError:
            context['album'] = None
        try:
            context['contents'] = self.get_object().\
                introductions.filter(content_flag=ContentFlag.Content.value[0]).order_by('sequence', 'id')
        except ObjectDoesNotExist:
            context['contents'] = None
        try:
            context['traffic_info'] = self.get_object().\
                introductions.filter(content_flag=ContentFlag.TrafficInfo.value[0])
        except ObjectDoesNotExist:
            context['traffic_info'] = None
        try:
            context['cautions'] = self.get_object().\
                introductions.filter(content_flag=ContentFlag.Cautions.value[0])
        except ObjectDoesNotExist:
            context['cautions'] = None
        try:
            context['others'] = self.get_object().\
                introductions.filter(content_flag=ContentFlag.Other.value[0])
        except ObjectDoesNotExist:
            context['others'] = None
        try:
            context['region_stations'] = Station.objects.\
                filter(region=self.get_object().region).\
                exclude(slug=self.get_object().slug)
        except ObjectDoesNotExist:
            context['region_stations'] = None
        return context

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        station = Station.objects.get(slug=slug)
        return station


@method_decorator(login_required, name='dispatch')
class StationUpdateView(UpdateView):
    model = Station
    template_name = 'ocean_station/manager/update.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user == self.get_object().manager or request.user.is_superuser:
            return super(StationUpdateView, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_form_class(self):
        return StationUpdateForm

    def form_valid(self, form):
        messages.success(self.request, "Updated successfully.")
        return super(StationUpdateView, self).form_valid(form)

    def get_success_url(self):
        station = self.get_object()
        region = [_.value[1] for _ in Region.__members__.values()]
        return reverse_lazy('station_update', kwargs={'slug': station.slug})
