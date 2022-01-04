from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import auth
from django.contrib import messages
from django.views.generic import TemplateView, CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from datetime import date
import base64

from CGA_Platform.email import sent_confirmation_email_to
from registration.models import User
from registration.definitions import Privilege
from registration.forms import LoginForm, RegisterForm, \
    SuperuserProfileForm, ProfileForm
from cga_booking.models import Hotel, Room, RoomReservation

# Create your views here.


class Index(TemplateView):
    template_name = 'index.html'


class Login(LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'


class Logout(LogoutView):
    template_name = 'registration/logout.html'


class Register(CreateView):
    model = User
    template_name = 'registration/register.html'
    form_class = RegisterForm

    def form_valid(self, form):
        # To check out the username whether contains characters other than English letters or numbers
        if not form.cleaned_data['username'].encode('utf-8').isalnum():
            messages.warning(self.request, "Username invalid. Only accept letters and numbers.")
            return super(Register, self).form_invalid(form)
        else:
            user = form.save()
            auth.login(self.request, user)
            return super(Register, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('index')


@method_decorator(login_required, name='dispatch')
class Profile(UpdateView):
    model = User
    template_name = 'registration/profile.html'

    def dispatch(self, request, *args, **kwargs):
        user = User.objects.get(username=self.kwargs['username'])
        if not self.request.user.is_superuser and user != self.request.user:
            raise PermissionDenied
        else:
            return super(Profile, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return User.objects.get(username=self.kwargs['username'])

    def get_form_class(self):
        if self.request.user.is_superuser:
            return SuperuserProfileForm
        else:
            return ProfileForm

    def form_valid(self, form):
        if form.instance.birthday is not None and form.cleaned_data['birthday'] > date.today():
            messages.error(self.request, "Your birthday is in the future, maybe this date you hadn't born.")
            return self.form_invalid(form)
        else:
            if form.instance.ID_Number == "":
                form.instance.ID_Number = None
            if self.request.user.email_is_verify and form.cleaned_data['email'] != self.request.user.email:
                form.instance.email_is_verify = False
                messages.warning(self.request, "Email changed, please reconfirm again.")
            form.save()
            messages.success(self.request, "Updated successfully.")
            return super(Profile, self).form_valid(form)

    def get_success_url(self):
        user = self.get_object()
        return reverse_lazy('profile', kwargs={'username': user.username})

    def get_context_data(self, **kwargs):
        context = super(Profile, self).get_context_data(**kwargs)
        context['user'] = self.get_object()
        return context


@method_decorator(login_required, name='dispatch')
class EmailConfirm(TemplateView):
    template_name = 'email/confirm.html'


@method_decorator(login_required, name='dispatch')
class EmailConfirmSent(TemplateView):
    template_name = 'email/confirm_sent.html'

    def dispatch(self, request, *args, **kwargs):
        sent_confirmation_email_to(user=self.request.user)
        messages.success(request, "Email sent successfully.")
        return super(EmailConfirmSent, self).dispatch(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class EmailConfirmDone(TemplateView):
    template_name = 'email/confirm_done.html'

    def dispatch(self, request, *args, **kwargs):
        base64_bytes_encoded_username = bytes(kwargs.get('username'), 'utf-8')
        encoded_username = base64.b64decode(base64_bytes_encoded_username)
        username = encoded_username.decode('utf-8')
        confirmed_user = User.objects.get(username=username)

        if confirmed_user != self.request.user:
            raise PermissionDenied
        elif confirmed_user.email_is_verify:
            messages.warning(self.request, "Email confirmed.")
            return reverse_lazy('index')
        else:
            confirmed_user.email_is_verify = True
            confirmed_user.save()
            return super(EmailConfirmDone, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EmailConfirmDone, self).get_context_data(**kwargs)
        context['tmp'] = kwargs.get('username')
        return context


@method_decorator(login_required, name='dispatch')
class ReservationsView(TemplateView):
    template_name = 'user/reservations.html'
    
    def dispatch(self, request, *args, **kwargs):
        return super(ReservationsView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ReservationsView, self).get_context_data(**kwargs)
        if self.request.user.privilege == Privilege.Official.value[0]:
            hotels = Hotel.objects.filter(manager=self.request.user)
            rooms = []
            for hotel in hotels:
                rooms.extend(Room.objects.filter(belongs2=hotel))
            room_reservations = []
            for room in rooms:
                room_reservations.extend(room.reservations.all())
            context['room_reservations'] = room_reservations
        else:
            context['room_reservations'] = RoomReservation.objects.filter(created_by=self.request.user)
        return context
