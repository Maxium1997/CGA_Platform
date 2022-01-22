from django import forms
from django.contrib.auth.views import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from ocean_station.models import User
from ocean_station.models import Station, Content, TaggedAttraction
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
        fields = ['name', 'manager', 'region', 'address', 'coordinate', 'contact_phone', 'fans_page_url',
                  'introductions']


class ContentEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ContentEditForm, self).__init__(*args, **kwargs)
        self.fields['description'] = forms.CharField(required=True,
                                                     widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Content
        fields = ['content_flag', 'description', 'sequence']


class ContentAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.content_type = kwargs.pop('content_type')
        self.object_id = kwargs.pop('object_id')
        super(ContentAddForm, self).__init__(*args, **kwargs)
        self.fields['description'] = forms.CharField(required=True,
                                                     widget=forms.Textarea(attrs={'class': 'form-control'}))

    def save(self, commit=True):
        content = super(ContentAddForm, self).save(commit=False)
        content.content_type = self.content_type
        content.object_id = self.object_id

        if commit:
            content.save()
        return content

    class Meta:
        model = Content
        fields = ['content_flag', 'description']


class AttractionAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.content_type = kwargs.pop('content_type')
        self.object_id = kwargs.pop('object_id')
        super(AttractionAddForm, self).__init__(*args, **kwargs)
        self.fields['name'] = forms.CharField(required=True,
                                              widget=forms.TextInput(attrs={'class': 'form-control border-0',
                                                                            'placeholder': "Enter tag name"}))
        self.fields['tag'] = forms.CharField(required=True,
                                             widget=forms.TextInput(attrs={'class': 'form-control border-0',
                                                                           'placeholder':
                                                                               'Use \'-\' to instead space'
                                                                               ' between the letter'}))

    def save(self, commit=True):
        content = super(AttractionAddForm, self).save(commit=False)
        content.content_type = self.content_type
        content.object_id = self.object_id

        if commit:
            content.save()
        return content

    class Meta:
        model = TaggedAttraction
        fields = ['name', 'tag']
