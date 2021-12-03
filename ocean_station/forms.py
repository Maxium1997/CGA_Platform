from django import forms
from django.contrib.auth.views import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from ocean_station.models import User
from ocean_station.models import Station
from ocean_station.definitions import Region


class StationUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StationUpdateForm, self).__init__(*args, **kwargs)
        region_choices = [(_.value[0], _.value[1]) for _ in Region.__members__.values()]
        self.fields['name'] = forms.CharField(required=True,
                                                  widget=forms.TextInput(attrs={'class': 'form-control border-0'}))
        self.fields['region'] = forms.ChoiceField(required=False,
                                                  choices=region_choices,
                                                  widget=forms.Select(attrs={'class': 'form-control border-0'}))
        self.fields['address'] = forms.CharField(required=False,
                                                 widget=forms.TextInput(attrs={'class': 'form-control border-0',
                                                                               'placeholder': "Address"}))
        self.fields['coordinate'] = forms.CharField(required=False,
                                                    widget=forms.TextInput(attrs={'class': 'form-control border-0',
                                                                                  'placeholder': "Coordinate"}))
        self.fields['contact_phone'] = forms.CharField(required=False,
                                                       widget=forms.TextInput(attrs={'class': 'form-control border-0',
                                                                                     'placeholder': "Contact Phone"}))
        self.fields['fans_page_url'] = forms.CharField(required=False,
                                                       widget=forms.TextInput(attrs={'class': 'form-control border-0',
                                                                                     'placeholder': "Fans Page URL"}))

    class Meta:
        model = Station
        fields = ['name', 'manager', 'region', 'address', 'coordinate', 'contact_phone', 'fans_page_url']
