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

from registration.models import User
from registration.forms import LoginForm, RegisterForm, \
    SuperuserProfileForm, ProfileForm

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
        if form.instance.birthday is not None and form.instance.birthday > date.today():
            messages.error(self.request, "Your birthday is in the future, maybe this date you hadn't born.")
            return self.form_invalid(form)
        else:
            if form.instance.ID_Number == "":
                form.instance.ID_Number = None
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
