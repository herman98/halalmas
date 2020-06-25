from django.contrib.gis import admin
from django import forms

from halalmas.core.forms import AutocompleteWidget
from .models import (Building, PublicTransport, 
    BuildingCategory, Location, PopularMall)


class BuildingCategoryAdmin(admin.OSMGeoAdmin):
    """ Building Category Criteria"""

    list_display = ['name', 'description', ]
    search_fields = ['name', 'description']

    list_filter = ['name']
    fieldsets = (
        ('Data Field', {
            'fields': ('name', 'description', ),
        }),
        ('Timestamp', {
            'classes': ('collapse',),  # collapse
            'fields': ('delstatus', 'deldate', 'cdate', 'udate'),
        }),
    )
    readonly_fields = ('cdate', 'udate')


class BuildingModelForm(forms.ModelForm):
    slug = forms.CharField(widget=forms.Textarea(
        attrs={'rows': '2', 'cols': '150'}), required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)
    description_id = forms.CharField(widget=forms.Textarea, required=False)
    building_access_id = forms.CharField(widget=forms.Textarea, required=False)

    is_desc_id = forms.BooleanField(widget=forms.CheckboxInput, required=False)
    is_building_access_id = forms.BooleanField(
        widget=forms.CheckboxInput, required=False)
    is_facilities_id = forms.BooleanField(
        widget=forms.CheckboxInput, required=False)

    description_en = forms.CharField(widget=forms.Textarea, required=False)
    building_access_en = forms.CharField(widget=forms.Textarea, required=False)

    is_desc_en = forms.BooleanField(widget=forms.CheckboxInput, required=False)
    is_building_access_en = forms.BooleanField(
        widget=forms.CheckboxInput, required=False)
    is_facilities_en = forms.BooleanField(
        widget=forms.CheckboxInput, required=False)

    image_url = forms.CharField(widget=forms.URLInput(
        attrs={'size': '150'}), required=False, )
    operational_hour_per_day = forms.CharField(
        widget=forms.NumberInput, required=False)
    operational_day_per_week = forms.CharField(
        widget=forms.NumberInput, required=False)
    operational_day_per_month = forms.CharField(
        widget=forms.NumberInput, required=False)

    class Meta:
        model = Building
        exclude = ('cdate', 'udate',)
        widgets = {
            'building_category': AutocompleteWidget(url='building:building-category-autocomplete'),
        }


class BuildingAdmin(admin.OSMGeoAdmin):
    """ Buildings Master Data in indonesia"""
    form = BuildingModelForm

    list_display = ['name','slug', 'address',
                    'building_category', 'coord_google', 'coord_osm', 'xwork_pk', 'delstatus', 'cdate']
    search_fields = ['name', 'address', 'kodepos']

    list_filter = ['building_category', 'delstatus', ]

    fieldsets = (
        ('Foreign Key', {
            'fields': ('building_category', 'public_transport', ),
        }),
        ('Data Field', {
            'fields': ('name', 'slug', 'address', 'kodepos', 'latitude', 'longitude', ),
        }),
        ('Descriptions Field', {
            'fields': ('description_id', 'building_access_id', 'facilities_id',
                       'description_en', 'building_access_en', 'facilities_en',),
        }),
        ('Complementary Field', {
            'fields': ('operational_hour_per_day',
                       'operational_day_per_week', 'operational_day_per_month',
                       'image_url', 'xwork_pk',),
        }),
        ('Map Field', {
            'classes': ('collapse',),  # collapse
            'fields': ('coord_google', 'coord_osm', ),
        }),
        ('Timestamp', {
            'classes': ('collapse',),  # collapse
            'fields': ('delstatus', 'deldate', 'cdate', 'udate',
                       'is_desc_id', 'is_building_access_id',
                       'is_facilities_id',
                       'is_desc_en',
                       'is_building_access_en',
                       'is_facilities_en', ),
        }),
    )
    readonly_fields = ('cdate', 'udate', )


class PublicTransportModelForm(forms.ModelForm):
    description_id = forms.CharField(widget=forms.Textarea, required=False)
    is_desc_id = forms.BooleanField(widget=forms.CheckboxInput, required=False)
    description_en = forms.CharField(widget=forms.Textarea, required=False)
    is_desc_en = forms.BooleanField(
        widget=forms.CheckboxInput, required=False)

    class Meta:
        model = PublicTransport
        exclude = ('cdate', 'udate',)
        widgets = {
            # 'building_category': AutocompleteWidget(url='building:bank-autocomplete'),
        }


class PublicTransportAdmin(admin.OSMGeoAdmin):
    """ Public transport near building """
    form = PublicTransportModelForm

    list_display = ['name', 'transport_type',
                    'description_id', 'is_desc_id']
    search_fields = ['name', 'description_id']

    list_filter = ['name']
    fieldsets = (
        ('Data Field', {
            'fields': ('name', 'transport_type', 'description_id', 'description_en',),
        }),
        ('Timestamp', {
            'classes': ('collapse',),  # collapse
            'fields': ('delstatus', 'deldate', 'cdate', 'udate', 'is_desc_id', 'is_desc_en',),
        }),
    )
    readonly_fields = ('cdate', 'udate')


class LocationAdmin(admin.OSMGeoAdmin):
    """ Location Data using latitude and longitude"""
    list_display = ['name', 'coord_google', 'coord_osm', ]
    search_fields = ['name',]

    list_filter = ['delstatus']

    fieldsets = (
        ('Data Field', {
            'fields': ('name', 'latitude', 'longitude', ),
        }),
        ('Map Field', {
            'classes': ('collapse',),  # collapse
            'fields': ('coord_google', 'coord_osm', ),
        }),
        ('Timestamp', {
            'classes': ('collapse',),  # collapse
            'fields': ('delstatus', 'deldate', 'cdate', 'udate',
                      ),
        }),
    )
    readonly_fields = ('cdate', 'udate', )


class PopularMallModelForm(forms.ModelForm):
    sequence = forms.CharField(
        widget=forms.NumberInput, required=False)

    class Meta:
        model = PopularMall
        exclude = ('cdate', 'udate',)
        widgets = {
            'building': AutocompleteWidget(url='building:building-autocomplete'),
        }

class PopularMallAdmin(admin.ModelAdmin):
    form = PopularMallModelForm

    list_per_page = 50
    search_fields = ('building__name', 'pk',)
    list_display = ('building', 'pk', 'sequence',)
    # list_filter = ()
    fieldsets = (
        ('Foreignkey Field', {
            'fields': ('building', ),
        }),
        ('Field', {
            'fields': ('sequence',),
        }),
        ('Timestamp', {
            'classes': ('collapse',),  # collapse
            'fields': ('delstatus', 'deldate', 'cdate', 'udate'),
        }),
    )
    readonly_fields = ('cdate', 'udate')
    save_on_top = True

    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

admin.site.register(Location, LocationAdmin)
admin.site.register(BuildingCategory, BuildingCategoryAdmin)
admin.site.register(Building, BuildingAdmin)
# admin.site.register(PublicTransport, PublicTransportAdmin)
admin.site.register(PopularMall, PopularMallAdmin)
