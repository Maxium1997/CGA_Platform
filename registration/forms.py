from django import forms
from django.contrib.auth.views import AuthenticationForm

from registration.models import User


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'] = forms.CharField(required=True,
                                                  widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                'placeholder': 'Username'}))
        self.fields['password'] = forms.CharField(required=True,
                                                  widget=forms.TextInput(attrs={'type': 'password',
                                                                                'class': 'form-control',
                                                                                'placeholder': 'Password'}))
