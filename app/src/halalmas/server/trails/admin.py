from __future__ import unicode_literals

from django import forms
from django.contrib.gis import admin

from dal import autocomplete

from .forms import AuditTrailModelForm
from .models import AuditTrail


class AuditTrailAdmin(admin.OSMGeoAdmin):
    """ Customer User Data """
    form = AuditTrailModelForm

    list_display = ['obj_model', 'message', 'server',  'remote_address', 'ref_type', 'ref_value', 'is_alert',
                    'cdate', 'creator', 'delstatus',]
    search_fields = ['message', 'creator__username',
                     'obj_model', 'server', 'remote_address', 'ref_type',]

    list_filter = ['is_alert', 'delstatus']

    fieldsets = (
        ('Foreign Key', {
            'fields': ('creator',),
        }),
        ('Data Field', {
            'fields': ('obj_model', 'message', 'server',  'remote_address', 'ref_type', 'ref_value', 'is_alert',),
        }),
        ('Timestamp', {
            'classes': ('collapse',),  # collapse
            'fields': ('delstatus', 'deldate', 'cdate', 'udate'),
        }),
    )
    readonly_fields = ('cdate', 'udate', 'creator',)

admin.site.register(AuditTrail, AuditTrailAdmin)