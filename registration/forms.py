from django import forms
from django.contrib.auth.views import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from registration.models import User
from registration.definitions import Gender, Identity, Privilege


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


class SuperuserProfileForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(SuperuserProfileForm, self).__init__(*args, **kwargs)
        self.fields['ID_Number'] = forms.CharField(required=False,
                                                   widget=forms.TextInput(attrs={'class': 'form-control border-0',
                                                                                 'placeholder': "ID Number"}))
        self.fields['first_name'] = forms.CharField(required=False,
                                                    widget=forms.TextInput(attrs={'class': 'form-control border-0',
                                                                                  'placeholder': "First name"}))
        self.fields['last_name'] = forms.CharField(required=False,
                                                   widget=forms.TextInput(attrs={'class': 'form-control border-0',
                                                                                 'placeholder': "Last name"}))
        self.fields['email'] = forms.CharField(required=True,
                                               widget=forms.TextInput(attrs={'class': 'form-control border-0',
                                                                             'placeholder': "Email"}))
        self.fields['phone'] = forms.CharField(required=True,
                                               widget=forms.TextInput(attrs={'class': 'form-control border-0',
                                                                             'placeholder': "Phone"}))
        self.fields['birthday'] = forms.DateField(required=False,
                                                  widget=forms.DateInput(attrs={'class': 'form-control border-0',
                                                                                'placeholder': "Format: yyyy-mm-dd"}))
        gender_choices = [(_.value[0], _.value[1]) for _ in Gender.__members__.values()]
        self.fields['gender'] = forms.ChoiceField(required=False,
                                                  choices=gender_choices,
                                                  widget=forms.Select(attrs={'class': 'form-control border-0'}))
        identity_choices = [(_.value[0], _.value[1]) for _ in Identity.__members__.values()]
        self.fields['identity'] = forms.ChoiceField(required=False,
                                                    choices=identity_choices,
                                                    widget=forms.Select(attrs={'class': 'form-control border-0'}))
        privilege_choices = [(_.value[0], _.value[1]) for _ in Privilege.__members__.values()]
        self.fields['privilege'] = forms.ChoiceField(required=False,
                                                     choices=privilege_choices,
                                                     widget=forms.Select(attrs={'class': 'form-control border-0'}))
        self.fields['introduction'] = forms.CharField(required=False,
                                                      widget=forms.Textarea(attrs={'class': 'form-control border-0',
                                                                                   'placeholder': "Write something about you"}))

    class Meta:
        model = User
        fields = ['ID_Number', 'first_name', 'last_name', 'email', 'phone', 'identity', 'birthday', 'gender', 'privilege', 'introduction']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class ProfileForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['ID_Number'] = forms.CharField(required=False,
                                                   widget=forms.TextInput(attrs={'class': 'form-control border-0',
                                                                                 'placeholder': "ID Number"}))
        self.fields['first_name'] = forms.CharField(required=False,
                                                    widget=forms.TextInput(attrs={'class': 'form-control border-0',
                                                                                  'placeholder': "First name"}))
        self.fields['last_name'] = forms.CharField(required=False,
                                                   widget=forms.TextInput(attrs={'class': 'form-control border-0',
                                                                                 'placeholder': "Last name"}))
        self.fields['email'] = forms.CharField(required=True,
                                               widget=forms.TextInput(attrs={'class': 'form-control border-0',
                                                                             'placeholder': "Email"}))
        self.fields['phone'] = forms.CharField(required=True,
                                               widget=forms.TextInput(attrs={'class': 'form-control border-0',
                                                                             'placeholder': "Phone"}))
        self.fields['birthday'] = forms.DateField(required=False,
                                                  widget=forms.DateInput(attrs={'class': 'form-control border-0',
                                                                                'placeholder': "Format: yyyy-mm-dd"}))
        gender_choices = [(_.value[0], _.value[1]) for _ in Gender.__members__.values()]
        self.fields['gender'] = forms.ChoiceField(required=False,
                                                  choices=gender_choices,
                                                  widget=forms.Select(attrs={'class': 'form-control border-0'}))
        identity_choices = [(_.value[0], _.value[1]) for _ in Identity.__members__.values()]
        self.fields['identity'] = forms.ChoiceField(required=False,
                                                    choices=identity_choices,
                                                    widget=forms.Select(attrs={'class': 'form-control border-0'}))
        self.fields['introduction'] = forms.CharField(required=False,
                                                      widget=forms.Textarea(attrs={'class': 'form-control border-0',
                                                                                   'placeholder': "Write something about you"}))

    class Meta:
        model = User
        fields = ['ID_Number', 'first_name', 'last_name', 'email', 'phone', 'identity', 'birthday', 'gender', 'introduction']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user
