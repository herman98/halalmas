from __future__ import unicode_literals

from datetime import datetime, timedelta

from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from django import forms
from django.forms.widgets import HiddenInput, TextInput
from django.forms.widgets import DateInput, RadioSelect, Select
from django.forms import ModelForm
from django.conf import settings


STATUS_CHOICE = (
    ('-empty-', _('-Pilih-')), 
    ('pending', _('Pending')), 
    ('active', _('Active')),
    ('complete', _('Complete')),
    ('cancel', _('Cancel')),
    ('expired', _('Expired'))
    )
STATUS_ORDER = (
    ('-empty-', _('-Pilih-')), 
    ('newest', _('Newest')), 
    ('oldest', _('Oldest')),
    ('order_date', _('Order Date')),
    ('use_date', _('Use Date'))
    )

STATUS_REDEEM = (
    ('-empty-', _('-All-')), 
    ('yes', _('YES')), 
    ('no', _('NO'))
    )

PAYMENT_METHOD = (
    ('-empty-', _('-All-')), 
    ('ONTHESPOT',('ON THE SPOT')),
    ('BANKTRANSFER', ('BANK TRANSFER')),
    ('CREDITCARD', ('CREDIT CARD')),
    ('OVO', ('OVO')),
    ('GOPAY', ('GOPAY')),
    ('VIRTUALACCOUNT', ('VIRTUAL ACCOUNT')),
    ('INSTALLMENT', ('INSTALLMENT')),
    ('OTHERS', ('OTHERS')) 
)
# YES_NO_CHOICES = ((True, _('YES')), (False, _('NO')))
PERIODE_CHOICES = ((True, _('Hari ini')), (False, _('Bebas')))


class HappyDealSearchForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(HappyDealSearchForm, self).__init__(*args, **kwargs)

    # date with time DateTimeWidget
    datetime_range = forms.CharField(required=False,
                                     widget=TextInput(attrs={
                                         'class': 'form-control input-daterange-timepicker',
                                         'name': "daterange"})
                                     )
    search_branch = forms.CharField(required=False,
                               widget=TextInput(attrs={'class': 'form-control',
                                                       'placeholder': 'Merchant'})
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
    status_pick = forms.ChoiceField(required=False,
                                choices=STATUS_REDEEM,
                                widget=Select(attrs={
                                    'class': 'form-control',
                                })
                            )
    payment_method = forms.ChoiceField(required=False,
                                choices=PAYMENT_METHOD,
                                widget=Select(attrs={
                                    'class': 'form-control',
                                })
                            ) 
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
