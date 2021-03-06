from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType


from django.db.models import Q

from ocean_station.models import Station, Content
from ocean_station.definitions import Region, ContentFlag, PhotoFlag
from ocean_station.forms import StationUpdateForm, ContentEditForm, ContentAddForm, AttractionAddForm

# Create your views here.


class OceanStationsView(ListView):
    model = Station
    template_name = 'ocean_station/all.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(OceanStationsView, self).get_context_data(object_list=None, **kwargs)
        stations = Station.objects.all().order_by('region')
        station_info_links = ['https://cgaplatform.pythonanywhere.com/ocean_station/{}/info'.format(_.slug) for _ in stations]
        context['stations'] = zip(station_info_links, stations)
        context['regions'] = [[_.value[0], _.value[1], _.value[2]] for _ in Region.__members__.values()][1:]

        # stations = Station.objects.all()
        # contents = ""
        # for station in stations:
        #     tmp = ""
        #     station_contents = Content.objects.filter(object_id=station.id).\
        #         exclude(Q(content_flag=ContentFlag.Overview.value[0])|Q(content_flag=ContentFlag.TrafficInfo.value[0]))
        #     for content in station_contents:
        #         tmp += content.description+"\n"
        #     station.introductions = tmp
        #     station.save()
        #     contents += tmp + "\n\n"
        #
        # for station in stations:
        #     try:
        #         station_overview = Content.objects.get(Q(object_id=station.id)&Q(content_flag=ContentFlag.Overview.value[0]))
        #         station.overview = station_overview.description
        #         station.save()
        #     except ObjectDoesNotExist:
        #         pass

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
            filter_criteria = Q(photo_flag=PhotoFlag.Main.value[0]) | Q(photo_flag=PhotoFlag.Display.value[0])
            context['album'] = self.get_object().\
                album.filter(filter_criteria)
        except ValueError:
            context['album'] = None

        try:
            context['region_stations'] = Station.objects.\
                filter(region=self.get_object().region).\
                exclude(slug=self.get_object().slug)
        except ObjectDoesNotExist:
            context['region_stations'] = None

        context['attraction_add_form'] = AttractionAddForm(content_type=ContentType.objects.get_for_model(Station),
                                                           object_id=self.get_object().id)

        return context

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        station = Station.objects.get(slug=slug)
        return station


@login_required
def attraction_add(request, slug):
    station = get_object_or_404(Station, slug=slug)
    if request.user == station.manager or request.user.is_superuser:
        new_attraction = AttractionAddForm(request.POST,
                                           content_type=ContentType.objects.get_for_model(Station),
                                           object_id=station.id).save()
        messages.success(request, "Added attraction successfully: {}".format(new_attraction))
    else:
        raise PermissionDenied

    return redirect('station_info', slug=station.slug)


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
        return reverse_lazy('station_update', kwargs={'slug': station.slug})


@method_decorator(login_required, name='dispatch')
class StationContentView(ListView):
    template_name = 'ocean_station/manager/contents.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user == self.get_object().manager or request.user.is_superuser:
            return super(StationContentView, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_object(self):
        return Station.objects.get(slug=self.kwargs.get('slug'))

    def get_queryset(self):
        return self.get_object().introductions.all().order_by('content_flag').order_by('sequence')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(StationContentView, self).get_context_data(**kwargs)
        context['station'] = self.get_object()
        context['content_add_form'] = ContentAddForm(content_type=ContentType.objects.get_for_model(Station),
                                                     object_id=self.get_object())
        return context


@login_required
def content_add(request, slug):
    station = get_object_or_404(Station, slug=slug)
    if request.user == station.manager or request.user.is_superuser:
        ContentAddForm(request.POST,
                       content_type=ContentType.objects.get_for_model(Station),
                       object_id=station.id).save()
    else:
        raise PermissionDenied

    return redirect('station_contents', slug=station.slug)


@method_decorator(login_required, name='dispatch')
class StationContentUpdateView(UpdateView):
    model = Station
    template_name = 'ocean_station/manager/content_edit.html'

    def dispatch(self, request, *args, **kwargs):
        station = get_object_or_404(Station, slug=kwargs.get('slug'))
        if request.user == station.manager or request.user.is_superuser:
            return super(StationContentUpdateView, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_object(self, queryset=None):
        return Content.objects.get(id=self.kwargs.get('id'))

    def get_context_data(self, **kwargs):
        context = super(StationContentUpdateView, self).get_context_data(**kwargs)
        context['station'] = self.get_object().content_object
        context['contents'] = self.get_object().content_object.introductions.filter(content_flag=self.get_object().content_flag).\
            order_by('sequence')
        return context

    def get_form_class(self):
        return ContentEditForm

    def get_success_url(self):
        return reverse_lazy('station_contents', kwargs={'slug': self.get_object().content_object.slug})


@method_decorator(login_required, name='dispatch')
class StationContentDelView(DeleteView):
    model = Station
    template_name = 'ocean_station/manager/content_delete.html'

    def dispatch(self, request, *args, **kwargs):
        station = get_object_or_404(Station, slug=kwargs.get('slug'))
        if request.user == station.manager or request.user.is_superuser:
            return super(StationContentDelView, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_object(self, queryset=None):
        return Content.objects.get(id=self.kwargs.get('id'))

    def get_context_data(self, **kwargs):
        context = super(StationContentDelView, self).get_context_data(**kwargs)
        context['station'] = self.get_object().content_object
        return context

    def get_success_url(self):
        return reverse_lazy('station_contents', kwargs={'slug': self.get_object().content_object.slug})
