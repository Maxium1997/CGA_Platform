from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.contrib import messages

from cga_booking.models import Hotel
from cga_booking.definitions import ContentFlag
from cga_booking.forms import HotelUpdateForm
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
        return context


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
