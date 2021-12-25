from django.shortcuts import render
from django.views.generic import ListView, DetailView

from cga_booking.models import Hotel
# Create your views here.


class HotelsView(ListView):
    model = Hotel
    template_name = 'hotel/all.html'


class HotelInfoView(DetailView):
    model = Hotel
    template_name = 'hotel/info.html'
