from django.contrib.gis import admin
from django import forms

from halalmas.core.forms import AutocompleteWidget
from .models import CalendarDimension, CalendarDate, ServerConfiguration


class ServerConfigurationModelForm(forms.ModelForm):
    config_value_int = forms.CharField(
        widget=forms.NumberInput, required=False,
        help_text='filled with numbers or currency value')
    description = forms.CharField(widget=forms.Textarea(
        attrs={'rows': '5', 'cols': '150'}), required=False)
    is_active = forms.BooleanField(
        widget=forms.CheckboxInput(), required=False, initial=True)

    class Meta:
        model = ServerConfiguration
        exclude = ('cdate', 'udate',)
        widgets = {
            # 'customer': AutocompleteWidget(url='user-profiles:user-profile-autocomplete'),
        }
        # labels = {
        #     'config_value_int': 'Value in Number',
        # }


class ServerConfigurationAdmin(admin.OSMGeoAdmin):
    """ ServerConfiguration  admin """
    form = ServerConfigurationModelForm

    list_display = ['config_name', 'config_value_int', 'config_value_str',
                    'config_status', 'is_active']
    search_fields = ['config_name', ]

    list_filter = ['is_active', ]
    fieldsets = (
        ('Data Field', {
            'fields': ('config_name', 'config_value_int', 'config_value_str',
                       'config_status', 'description', 'is_active', ),
        }),
        ('Timestamp', {
            'classes': ('collapse',),  # collapse
            'fields': ('delstatus', 'deldate', 'cdate', 'udate',),
        }),
    )
    readonly_fields = ('cdate', 'udate', )
    save_on_top = True

    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return True


class CalendarDimensionModelForm(forms.ModelForm):
    month = forms.CharField(
        widget=forms.NumberInput, required=False,
        help_text='filled with 1 to 12')
    year = forms.CharField(
        widget=forms.NumberInput, required=False,
        help_text='filled from 1999 to 2099')

    class Meta:
        model = CalendarDimension
        exclude = ('cdate', 'udate',)
        widgets = {
        }


class CalendarDimensionAdmin(admin.OSMGeoAdmin):
    """ CalendarDimensionAdmin  admin """
    form = CalendarDimensionModelForm

    list_display = ['year', 'month', ]
    search_fields = ['year', ]

    fieldsets = (
        ('Data Field', {
            'fields': ('year', 'month', ),
        }),
        ('Timestamp', {
            'classes': ('collapse',),  # collapse
            'fields': ('delstatus', 'deldate', 'cdate', 'udate',),
        }),
    )
    readonly_fields = ('cdate', 'udate', )
    save_on_top = True

    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return True


class CalendarDateModelForm(forms.ModelForm):
    class Meta:
        model = CalendarDate
        exclude = ('cdate', 'udate',)
        widgets = {
            'dimension': AutocompleteWidget(url='server-configuration:calendar-dimension-autocomplete'),
        }


class CalendarDateAdmin(admin.OSMGeoAdmin):
    """ CalendarDateAdmin  admin """
    form = CalendarDateModelForm

    list_display = ['dimension', 'calendar_date', 'status', ]
    search_fields = ['dimension__year', 'dimension__month']
    list_filter = ['status', ]
    fieldsets = (
        ('Data Field', {
            'fields': ('dimension', 'calendar_date', 'status'),
        }),
        ('Timestamp', {
            'classes': ('collapse',),  # collapse
            'fields': ('delstatus', 'deldate', 'cdate', 'udate',),
        }),
    )
    readonly_fields = ('cdate', 'udate', )
    save_on_top = True

    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return True


admin.site.register(ServerConfiguration, ServerConfigurationAdmin)
admin.site.register(CalendarDimension, CalendarDimensionAdmin)
admin.site.register(CalendarDate, CalendarDateAdmin)
