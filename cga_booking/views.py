from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType

from cga_booking.models import Hotel, Room
from cga_booking.definitions import ContentFlag
from cga_booking.forms import HotelUpdateForm, HotelAttractionAddForm
# Create your views here.


class HotelsView(ListView):
    model = Hotel
    template_name = 'hotel/all.html'


class HotelInfoView(DetailView):
    model = Hotel
    template_name = 'hotel/info.html'

    def get_context_data(self, **kwargs):
        context = super(HotelInfoView, self).get_context_data(**kwargs)
        context['overviews'] = self.get_object().introductions.filter(content_flag=ContentFlag.Overview.value[0])
        context['cautions'] = self.get_object().introductions.filter(content_flag=ContentFlag.Cautions.value[0])
        context['others'] = self.get_object().introductions.filter(content_flag=ContentFlag.Other.value[0])
        context['hotel_attraction_add_form'] = HotelAttractionAddForm(content_type=ContentType.objects.get_for_model(Hotel),
                                                                      object_id=self.get_object().id)
        return context


@login_required
def hotel_attraction_add(request, slug):
    hotel = get_object_or_404(Hotel, slug=slug)
    if request.user.is_superuser:
        new_attraction = HotelAttractionAddForm(request.POST,
                                                content_type=ContentType.objects.get_for_model(Hotel),
                                                object_id=hotel.id).save()
        messages.success(request, "Added attraction successfully: {}".format(new_attraction))
    else:
        raise PermissionDenied

    return redirect('hotel_info', slug=hotel.slug)


@method_decorator(login_required, name='dispatch')
class HotelUpdateView(UpdateView):
    model = Hotel
    template_name = 'hotel/manager/update.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super(HotelUpdateView, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_form_class(self):
        return HotelUpdateForm

    def form_valid(self, form):
        messages.success(self.request, "Updated successfully.")
        return super(HotelUpdateView, self).form_valid(form)

    def get_success_url(self):
        hotel = self.get_object()
        return reverse_lazy('hotel_update', kwargs={'slug': hotel.slug})


@method_decorator(login_required, name='dispatch')
class RoomAddView(CreateView):
    model = Room
    template_name = 'hotel/manager/room/add.html'
    fields = ['belongs2', 'name', 'price', 'single_bed', 'double_bed']

    def dispatch(self, request, *args, **kwargs):
        return super(RoomAddView, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return get_object_or_404(Hotel, slug=self.kwargs.get('slug'))

    def get_context_data(self, **kwargs):
        context = super(RoomAddView, self).get_context_data(**kwargs)
        context['hotel'] = self.get_object()
        return context

    def get_initial(self):
        initial = super(RoomAddView, self).get_initial()
        initial['belongs2'] = self.get_object()
        return initial

    def form_valid(self, form):
        if form.instance.belongs2 != self.get_object():
            messages.warning(self.request, 'Your belongs2 column value is not your selected hotel, '
                                           'please do not changed.')
            return super(RoomAddView, self).form_invalid(form)
        return super(RoomAddView, self).form_valid(form)

    def get_success_url(self):
        hotel = self.get_object()
        return reverse_lazy('hotel_update', kwargs={'slug': hotel.slug})
