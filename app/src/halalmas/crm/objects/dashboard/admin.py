# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.gis import admin

from .forms import CRMSettingModelForm
from .models import CRMSetting


class CRMSettingAdmin(admin.OSMGeoAdmin):
    form = CRMSettingModelForm

    list_per_page = 50
    list_display = ('user', 'role_select', 'role_default', 'cdate', 'udate')
    search_fields = ('user__username', 'role_select', 'role_default', )

    # list_filter = ['']

    fieldsets = (
        ('Foreign Key', {
            'fields': ('user', ),
        }),
        ('Data Field', {
            'fields': ('role_select', 'role_default',),
        }),
        ('Timestamp', {
            'classes': ('collapse',),  # collapse
            'fields': ('delstatus', 'deldate', 'cdate', 'udate'),
        }),
    )
    readonly_fields = ('cdate', 'udate',)


admin.site.register(CRMSetting, CRMSettingAdmin)
