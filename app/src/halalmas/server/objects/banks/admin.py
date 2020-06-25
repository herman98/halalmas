from django.contrib.gis import admin
from django import forms

from dal import autocomplete
from halalmas.core.forms import AutocompleteWidget

from .models import Bank, BankAccount


class BankAccountModelForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        exclude = ('cdate', 'udate',)
        widgets = {
            'bank': AutocompleteWidget(url='bank:bank-autocomplete'),
        }


class BankAdmin(admin.OSMGeoAdmin):
    """ Bank Master Data """

    list_display = ['code', 'name',
                    'country']
    search_fields = ['code', 'name', ]

    list_filter = ['code']

    fieldsets = (
        ('Data Field', {
            'fields': ('code', 'name',
                       'country', ),
        }),
        ('Timestamp', {
            'classes': ('collapse',),  # collapse
            'fields': ('delstatus', 'deldate', 'cdate', 'udate'),
        }),
    )
    readonly_fields = ('cdate', 'udate')


class BankAccountAdmin(admin.OSMGeoAdmin):
    """ Bank Master Data """
    form = BankAccountModelForm

    list_display = ['account_no', 'bank', 'account_name', 'account_type',
                    'bank_branch', 'default_currency', 'creator']
    search_fields = ['account_no', 'account_name',
                     'bank_branch', 'default_currency']

    list_filter = ['account_type', 'bank_branch', ]

    fieldsets = (
        ('Data Field', {
            'fields': ('bank', 'account_no', 'account_name',
                       'bank_branch', 'account_type', 'default_currency', ),
        }),
        ('Timestamp', {
            'classes': ('collapse',),  # collapse
            'fields': ('delstatus', 'deldate', 'cdate', 'udate'),
        }),
    )
    readonly_fields = ('cdate', 'udate')


admin.site.register(Bank, BankAdmin)
admin.site.register(BankAccount, BankAccountAdmin)
