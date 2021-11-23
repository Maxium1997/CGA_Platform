from django import forms
from django.contrib.auth.views import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm

from registration.models import User


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'] = forms.CharField(required=True,
                                                  widget=forms.TextInput(attrs={'class': 'form-control'}))
        self.fields['password'] = forms.CharField(required=True,
                                                  widget=forms.TextInput(attrs={'type': 'password',
                                                                                'class': 'form-control'}))


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'] = forms.CharField(required=True,
                                                  widget=forms.TextInput(attrs={'class': 'form-control'}))
        self.fields['password1'] = forms.CharField(required=True,
                                                   widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                 'type': 'password'}))
        self.fields['password2'] = forms.CharField(required=True,
                                                   widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                 'type': 'password',
                                                                                 'placeholder': 'Password Confirmation'}))
        self.fields['phone'] = forms.CharField(required=True,
                                               widget=forms.TextInput(attrs={'class': 'form-control'}))
        self.fields['email'] = forms.CharField(required=True,
                                               widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'phone', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user
