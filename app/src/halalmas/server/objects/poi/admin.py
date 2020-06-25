from django.contrib.gis import admin
from django import forms
from django.contrib.gis.geos import Point

from halalmas.core.forms import AutocompleteWidget
from .models import PointOfInterest, PointOfInterestCoverage

LONGITUDE_DIFF = 0.002200


class PointOfInterestModelForm(forms.ModelForm):
    """
        https://nominatim.openstreetmap.org/details.php?place_id=199179860&polygon_geojson=1&format=json
        and install chrome ext: jsonview

    """
    radius = forms.CharField(
        widget=forms.NumberInput, required=False,
        help_text='filled 0.01 for 1km')
    json_multipolygon = forms.CharField(widget=forms.Textarea(
        attrs={'rows': '5', 'cols': '150'}), required=False,
        help_text='see https://www.keene.edu/campus/maps/tool/ or https://nominatim.openstreetmap.org/details.php?place_id=199179860&polygon_geojson=1&format=json for draw polygon')

    class Meta:
        model = PointOfInterest
        exclude = ('cdate', 'udate',)
        widgets = {
            # 'building_category': AutocompleteWidget(url='building:bank-autocomplete'),
        }


class PointOfInterestAdmin(admin.OSMGeoAdmin):
    """ OSMGeoAdmin = Open Street Map for Point of Interest """
    form = PointOfInterestModelForm

    list_display = ['poi_name', 'radius', 'latitude', 'longitude', 'json_multipolygon',
                    'geom_point_google', 'geom_point_osm', 'is_active', 'creator']
    search_fields = ['poi_name', ]

    list_filter = ['is_radius']
    fieldsets = (
        ('Data Field', {
            'fields': ('poi_name', 'radius', 'latitude', 'longitude', 'json_multipolygon', ),
        }),
        ('Map Field', {
            'classes': ('collapse',),  # collapse
            'fields': ('geom_point_google', 'geom_point_osm', 'geom_multipolygon', ),
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

    # def get_readonly_fields(self, request, obj=None):
    #     if obj:
    #         return self.readonly_fields + ('delstatus')
    #     return self.readonly_fields

    # def save_model(self, request, obj, form, change):
    #     print("HOHOHO#1")
    #     print(change)
    #     _lat = form.cleaned_data['latitude']
    #     _lon = form.cleaned_data['longitude']
    #     if _lat and _lon:
    #         print("HOHOHO#2", _lon, _lat)
    #         obj.geom_point_google = Point(_lon, _lat)
    #         lon_osm = _lon + LONGITUDE_DIFF
    #         obj.geom_point_osm = Point(lon_osm, _lat)
    #         obj.save()
    #     super(PointOfInterestAdmin, self).save_model(
    #         request, obj, form, change)


class PointOfInterestCoverageModelForm(forms.ModelForm):

    class Meta:
        model = PointOfInterest
        exclude = ('cdate', 'udate',)
        widgets = {
            'poi': AutocompleteWidget(url='gis-poi:gis-poi-autocomplete'),
            'coverage': AutocompleteWidget(url='gis-indonesia:gis-kelurahan-autocomplete'),
        }


class PointOfInterestCoverageAdmin(admin.OSMGeoAdmin):
    form = PointOfInterestCoverageModelForm
    """ Point of Interest Coverage :  """

    list_display = ['pk', 'poi', 'coverage']
    search_fields = ['poi__poi_name', ]
    fieldsets = (
        ('Data Field', {
            'fields': ('poi', 'coverage', ),
        }),
        ('Timestamp', {
            'classes': ('collapse',),  # collapse
            'fields': ('delstatus', 'deldate', 'cdate', 'udate',),
        }),
    )
    readonly_fields = ('cdate', 'udate', )


admin.site.register(PointOfInterest, PointOfInterestAdmin)
# admin.site.register(PointOfInterestCoverage, PointOfInterestCoverageAdmin)
