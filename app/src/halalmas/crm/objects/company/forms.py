from __future__ import unicode_literals

from datetime import datetime, timedelta

from dal import autocomplete
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from django import forms
from django.forms.widgets import HiddenInput, TextInput
from django.forms.widgets import DateInput, RadioSelect, Select
from django.forms import ModelForm
from django.conf import settings
from halalmas.server.objects.companies.constants import OrganizationType


STATUS_CHOICE = (('-empty-', _('-Pilih-')), ) + OrganizationType.get_choices()
# print(type(STATUS_CHOICE), STATUS_CHOICE)

STATUS_ORDER = (
    ('-empty-', _('-Pilih-')), 
    ('latest', _('Latest')), 
    ('longest', _('Longest')),
    ('name_asc', _('Company ASC')),
    ('name_desc', _('Company DESC'))
    )

YES_NO_CHOICES = ((True, _('YES')), (False, _('NO')))
PERIODE_CHOICES = ((True, _('Hari ini')), (False, _('Bebas')))
SORT_BY = (('ASC', _('ASC')), ('DESC', _('DESC')))

class CompanySearchForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(CompanySearchForm, self).__init__(*args, **kwargs)

    # date with time DateTimeWidget
    datetime_range = forms.CharField(required=False,
                                     widget=TextInput(attrs={
                                         'class': 'form-control input-daterange-timepicker',
                                         'name': "daterange"})
                                     )

    search_q = forms.CharField(required=False,
                               widget=TextInput(attrs={'class': 'form-control',
                                                       'placeholder': 'Pencarian'})
                               )

    status_choice = forms.ChoiceField(required=False,
                                choices=STATUS_CHOICE,
                                widget=Select(attrs={
                                    'class': 'form-control',
                                })
                            )
    # status_pick = forms.ChoiceField(required=False,
    #                             choices=YES_NO_CHOICES,
    #                             widget=Select(attrs={
    #                                 'class': 'form-control',
    #                             })
    #                         )

    status_order = forms.ChoiceField(required=False,
                            choices=STATUS_ORDER,
                            widget=Select(attrs={
                                'class': 'form-control',
                            })
                            )

    status_now = forms.ChoiceField(required=False,
                                   choices=PERIODE_CHOICES,
                                   widget=RadioSelect()
                                   )
