from django.contrib.gis import admin
from django import forms

from halalmas.core.forms import AutocompleteWidget
from .models import Company


# 
class CompanyModelForm(forms.ModelForm):
    # address = forms.CharField(widget=forms.Textarea, required=False)
    # building_access_en = forms.CharField(widget=forms.Textarea, required=False)
    # is_desc_en = forms.BooleanField(widget=forms.CheckboxInput, required=False)
    # image_url = forms.CharField(widget=forms.URLInput(
    #     attrs={'size': '150'}), required=False, )

    class Meta:
        model = Company
        exclude = ('cdate', 'udate',)
        widgets = {
            'location': AutocompleteWidget(url='building:location-autocomplete'),
        }

class CompanyAdmin(admin.OSMGeoAdmin):
    """ Indonesia Region using Kelurahan Border with description on it """
    form = CompanyModelForm

    list_display = ['name', 'organization_type',
                    'group_type', 'npwp', 'address', 'post_code', 'phone', 'siup', 'owner_name', 'creator']
    search_fields = ['name', 'address', 'phone', 'siup', 'owner_name',
                     'npwp', 'post_code']

    list_filter = ['group_type', 'organization_type']

    fieldsets = (
        ('Data Field', {
            'fields': ('name', 'organization_type',
                       'group_type', 'npwp', 'address', 'location', 'post_code', 'phone', 'siup', 'owner_name', ),
        }),
        ('Timestamp', {
            'classes': ('collapse',),  # collapse
            'fields': ('delstatus', 'deldate', 'cdate', 'udate'),
        }),
    )
    readonly_fields = ('cdate', 'udate')


admin.site.register(Company, CompanyAdmin)
