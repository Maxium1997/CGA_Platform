from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import auth
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.views import LoginView, LogoutView

from registration.models import User
from registration.forms import LoginForm, RegisterForm

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
