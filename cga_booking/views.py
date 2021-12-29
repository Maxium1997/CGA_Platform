from django.shortcuts import render
from django.views.generic import ListView, DetailView

from cga_booking.models import Hotel
from cga_booking.definitions import ContentFlag
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
