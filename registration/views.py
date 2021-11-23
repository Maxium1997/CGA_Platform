from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView

from registration.forms import LoginForm

# Create your views here.


class Index(TemplateView):
    template_name = 'index.html'


class Login(LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'


class Logout(LogoutView):
    template_name = 'registration/logout.html'
