from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, UpdateView, CreateView, TemplateView
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

from datetime import date, datetime, timedelta

from CGA_Platform.settings import DEBUG
from cga_booking.models import Hotel, Room, RoomReservation
from cga_booking.definitions import ContentFlag, ReservationUsages, ReservationStatus
from cga_booking.forms import HotelUpdateForm, HotelAttractionAddForm
from cga_booking.decorators import reservation_time_validate
from CGA_Platform.email import sent_reservation_info, sent_reservation_mail
from registration.models import User
from registration.definitions import Privilege

# Create your views here.


class HotelsView(ListView):
    model = Hotel
    template_name = 'hotel/all.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HotelsView, self).get_context_data(object_list=None, **kwargs)
        hotels = self.get_queryset()
        hotel_info_links = ['https://cgaplatform.pythonanywhere.com/hotel/{}/info'.format(_.slug) for _ in hotels]
        context['object_list'] = zip(hotel_info_links, hotels)
        return context


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
    if request.user == hotel.manager:
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
        if self.request.user == self.get_object().manager:
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
        if self.request.user == self.get_object().manager:
            return super(RoomAddView, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

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


@method_decorator(login_required, name='dispatch')
class RoomUpdateView(UpdateView):
    model = Room
    template_name = 'hotel/manager/room/update.html'
    fields = ['name', 'price', 'single_bed', 'double_bed']

    def dispatch(self, request, *args, **kwargs):
        if self.request.user == self.get_object().belongs2.manager:
            return super(RoomUpdateView, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super(RoomUpdateView, self).get_context_data(**kwargs)
        context['hotel'] = self.get_object().belongs2
        context['room'] = self.get_object()
        return context

    def form_valid(self, form):
        messages.success(self.request, "Updated successfully.")
        return super(RoomUpdateView, self).form_valid(form)

    def get_success_url(self):
        room = self.get_object()
        hotel = self.get_object().belongs2
        return reverse_lazy('room_update', kwargs={'slug': hotel.slug,
                                                   'pk': room.pk})


@method_decorator(login_required, name='dispatch')
class RoomReservationView(CreateView):
    model = RoomReservation
    template_name = 'reservation.html'
    fields = ['created_by', 'start_time', 'end_time', 'usage']
    valid_message = "Successfully reserved."
    
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.privilege == Privilege.Official.value[0]:
            messages.warning(request, "Official account cannot use this feature: Reserve room")
            return redirect('hotels')
        else:
            return super(RoomReservationView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super(RoomReservationView, self).get_initial()
        initial['created_by'] = self.request.user
        initial['start_time'] = date.today().strftime("%Y-%m-%d")
        initial['end_time'] = (date.today() + timedelta(days=2)).strftime("%Y-%m-%d")
        return initial

    def get_context_data(self, **kwargs):
        context = super(RoomReservationView, self).get_context_data(**kwargs)
        context['hotel'] = Hotel.objects.get(slug=self.kwargs['slug'])
        context['room'] = Hotel.objects.get(slug=self.kwargs['slug']).room_set.get(pk=self.kwargs['pk'])
        context['usages_dict'] = ReservationUsages.__members__.values()

        reservations = Hotel.objects.get(slug=self.kwargs['slug']).room_set.get(pk=self.kwargs['pk']).reservations.all().order_by('start_time')
        context['reservations'] = reservations

        reserved_date_list = []
        for reservation in reservations:
            tmp_date = reservation.start_time
            while tmp_date < reservation.end_time:
                reserved_date_list.append(tmp_date.strftime("%m/%d"))
                tmp_date += timedelta(days=1)
            reserved_date_list.append("/")

        date_operators = []
        for i in range(60):
            tmp_date = (date.today() + timedelta(days=i)).strftime("%m/%d")
            if tmp_date in reserved_date_list:
                tmp = True
            else:
                tmp = False
            date_operators.append(tmp)

        last_60_days = []
        for i in range(60):
            last_60_days.append((date.today() + timedelta(days=i)).strftime("%m/%d"))

        context['last_60_days'] = zip(date_operators, last_60_days)
        return context

    def form_valid(self, form):
        hotel = Hotel.objects.get(slug=self.kwargs['slug'])
        reserved_room = hotel.room_set.get(pk=self.kwargs['pk'])
        form.instance.content_type = ContentType.objects.get_for_model(Room)
        form.instance.object_id = reserved_room.id

        if form.instance.created_by is None:
            messages.warning(self.request,
                             "Customer field cannot blank.")
            return super(RoomReservationView, self).form_invalid(form)
        elif form.instance.created_by != self.request.user:
            messages.warning(self.request,
                             "Your customer field is not yourself, please do not change the field.")
            return super(RoomReservationView, self).form_invalid(form)

        if form.instance.start_time < datetime.now():
            messages.warning(self.request,
                             "Check your check in time whether earlier than now or you have over the check in time.")
            return super(RoomReservationView, self).form_invalid(form)
        elif form.instance.start_time > form.instance.end_time:
            messages.warning(self.request,
                             "Check your check out time whether earlier than check in time.")
            return super(RoomReservationView, self).form_invalid(form)
        else:
            if not reservation_time_validate(reserved_room, form.instance.start_time, form.instance.end_time):
                messages.warning(self.request,
                                 "Your reserved time maybe conflict.")
                return super(RoomReservationView, self).form_invalid(form)
            form.instance.serial_number = (hotel.__str__() + datetime.now().strftime("%Y%m%d%H%M%S")).encode('utf-8').hex()
            c_time = datetime.strptime('1500', "%H%M").time()
            o_time = datetime.strptime('1200', "%H%M").time()
            form.instance.start_time = datetime.combine(form.instance.start_time, c_time)
            form.instance.end_time = datetime.combine(form.instance.end_time, o_time)

        form.instance.status = ReservationStatus.Pending.value[0]
        form.instance.price = reserved_room.price

        form.save()
        sent_reservation_mail(reservation=form.instance, recipient=form.instance.created_by)
        sent_reservation_mail(reservation=form.instance, recipient=reserved_room.belongs2.manager)
        return super(RoomReservationView, self).form_valid(form)

    def form_invalid(self, form):
        return super(RoomReservationView, self).form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('room_reservations', kwargs={'username': self.request.user.username})


@method_decorator(login_required, name='dispatch')
class RoomReservationsView(TemplateView):
    template_name = 'hotel/reservations.html'

    def dispatch(self, request, *args, **kwargs):
        return super(RoomReservationsView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RoomReservationsView, self).get_context_data(**kwargs)
        context['request_user_is_official'] = self.request.user.privilege == Privilege.Official.value[0]
        context['now_time'] = datetime.now()
        if self.request.user.is_superuser:
            context['room_reservations'] = RoomReservation.objects.all()

        elif self.request.user.privilege == Privilege.Official.value[0]:
            hotels = Hotel.objects.filter(manager=self.request.user)
            room_ids = [_.id for _ in Room.objects.filter(belongs2__in=hotels)]
            room_type = ContentType.objects.get(model='room')
            # filter_criteria = Q(content_type=room_type) & Q(object_id__in=room_ids)
            filter_criteria = Q(content_type=room_type) & Q(object_id__in=room_ids)
            room_reservations = RoomReservation.objects.filter(filter_criteria).order_by('start_time', 'end_time')
            context['room_reservations'] = room_reservations
            context['room_ids'] = room_ids

        else:
            context['room_reservations'] = RoomReservation.objects.filter(created_by=self.request.user)
        return context
    
    
@method_decorator(login_required, name='dispatch')
class RoomReservationRelocatingView(ListView):
    model = RoomReservation

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.privilege != Privilege.Official.value[0]:
            raise PermissionDenied
        else:
            return super(RoomReservationRelocatingView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        now_time = datetime.now()
        if self.request.user.is_superuser:
            room_reservations = RoomReservation.objects.all()

        elif self.request.user.privilege == Privilege.Official.value[0]:
            hotels = Hotel.objects.filter(manager=self.request.user)
            room_ids = [_.id for _ in Room.objects.filter(belongs2__in=hotels)]
            room_type = ContentType.objects.get(model='room')
            room_reservations = RoomReservation.objects.filter(content_type=room_type,
                                                               object_id__in=room_ids).order_by('start_time',
                                                                                                'end_time')
            room_reservations = room_reservations

        else:
            room_reservations = RoomReservation.objects.filter(created_by=self.request.user)
        return room_reservations


@method_decorator(login_required, name='dispatch')
class RoomReservationInfoView(DetailView):
    model = RoomReservation
    template_name = 'hotel/user/reservation/info.html'

    def dispatch(self, request, *args, **kwargs):
        serial_number = self.kwargs.get('serial_number')
        room_reservation = RoomReservation.objects.get(serial_number=serial_number)
        if self.request.user.is_superuser or \
                (self.request.user == room_reservation.created_by) or \
                (self.request.user == room_reservation.content_object.belongs2.manager):
            return super(RoomReservationInfoView, self).dispatch(request, *args, **kwargs)
        elif not room_reservation.created_by == self.request.user:
            raise PermissionDenied

    def get_object(self, queryset=None):
        serial_number = self.kwargs.get('serial_number')
        room_reservation = RoomReservation.objects.get(serial_number=serial_number)
        return room_reservation

    def get_context_data(self, **kwargs):
        context = super(RoomReservationInfoView, self).get_context_data(**kwargs)
        context['reservation'] = self.get_object()
        if DEBUG:
            context['room_reservation_features_link'] = '127.0.0.1:8000/{}/reservations/{}/features'.format(
                self.request.user.username,
                self.get_object().serial_number)
        else:
            context[
                'room_reservation_features_link'] = 'https://cgaplatform.pythonanywhere.com/{}/reservations/{}/features'.format(
                self.request.user.username,
                self.get_object().serial_number)

        return context


@method_decorator(login_required, name='dispatch')
class RoomReservationPassedView(UpdateView):
    model = RoomReservation

    def get_object(self, queryset=None):
        serial_number = self.kwargs.get('serial_number')
        room_reservation = RoomReservation.objects.get(serial_number=serial_number)
        return room_reservation


@method_decorator(login_required, name='dispatch')
class RoomReservationRejectedView(UpdateView):
    model = RoomReservation

    def get_object(self, queryset=None):
        serial_number = self.kwargs.get('serial_number')
        room_reservation = RoomReservation.objects.get(serial_number=serial_number)
        return room_reservation


@method_decorator(login_required, name='dispatch')
class RoomReservationCanceledView(UpdateView):
    model = RoomReservation
    fields = ['status']

    def get_object(self, queryset=None):
        serial_number = self.kwargs.get('serial_number')
        room_reservation = RoomReservation.objects.get(serial_number=serial_number)
        return room_reservation
    
    def dispatch(self, request, *args, **kwargs):
        if self.request.user != self.get_object().created_by:
            raise PermissionDenied
        else:
            return super(RoomReservationCanceledView, self).dispatch(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class RoomReservationCheckInView(UpdateView):
    model = RoomReservation

    def get_object(self, queryset=None):
        serial_number = self.kwargs.get('serial_number')
        room_reservation = RoomReservation.objects.get(serial_number=serial_number)
        return room_reservation


@method_decorator(login_required, name='dispatch')
class RoomReservationNoShowView(UpdateView):
    model = RoomReservation

    def get_object(self, queryset=None):
        serial_number = self.kwargs.get('serial_number')
        room_reservation = RoomReservation.objects.get(serial_number=serial_number)
        return room_reservation


@method_decorator(login_required, name='dispatch')
class RoomReservationCheckOutView(UpdateView):
    model = RoomReservation

    def get_object(self, queryset=None):
        serial_number = self.kwargs.get('serial_number')
        room_reservation = RoomReservation.objects.get(serial_number=serial_number)
        return room_reservation
