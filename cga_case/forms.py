from django import forms

from cga_case.models import CaseCategory, CaseSection, Case


class CaseSearchForm(forms.Form):
    search_field = forms.CharField(required=True,
                                   widget=forms.TextInput(attrs={'class': 'form-control',
                                                                 'placeholder':
                                                                     'Enter the keyword to search case'}))
