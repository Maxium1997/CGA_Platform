from django import forms

from cga_booking.models import Hotel


class HotelUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(HotelUpdateForm, self).__init__(*args, **kwargs)
        self.fields['name'] = forms.CharField(required=True,
                                              widget=forms.TextInput(attrs={'class': 'form-control border-0'}))
        self.fields['address'] = forms.CharField(required=False,
                                                 widget=forms.TextInput(attrs={'class': 'form-control border-0',
                                                                               'placeholder': "Address"}))
        self.fields['coordinate'] = forms.CharField(required=False,
                                                    widget=forms.TextInput(attrs={'class': 'form-control border-0',
                                                                                  'placeholder': "Coordinate"}))
        self.fields['contact_phone'] = forms.CharField(required=False,
                                                       widget=forms.TextInput(attrs={'class': 'form-control border-0',
                                                                                     'placeholder': "Contact Phone"}))
        self.fields['contact_email'] = forms.CharField(required=False,
                                                       widget=forms.TextInput(attrs={'class': 'form-control border-0',
                                                                                     'placeholder': "Contact Email"}))
        self.fields['website'] = forms.CharField(required=False,
                                                 widget=forms.TextInput(attrs={'class': 'form-control border-0',
                                                                               'placeholder': "Website URL"}))

    class Meta:
        model = Hotel
        fields = ['name', 'address', 'coordinate', 'contact_phone', 'contact_email', 'website']
