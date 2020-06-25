from __future__ import absolute_import
from __future__ import unicode_literals

from django.conf.urls import url
from django.urls import path

from .lookups import KelurahanBorderAutocomplete, KecamatanBorderAutocomplete, \
    KabupatenBorderAutocomplete, ProvinsiBorderAutocomplete
# from . import views

urlpatterns = [

    # auto-complete
    url(r'^gis-province-autocomplete/$', ProvinsiBorderAutocomplete.as_view(),
        name='gis-province-autocomplete',
        ),
    url(r'^gis-city-autocomplete/$', KabupatenBorderAutocomplete.as_view(),
        name='gis-city-autocomplete',
        ),
    url(r'^gis-kecamatan-autocomplete/$', KecamatanBorderAutocomplete.as_view(),
        name='gis-kecamatan-autocomplete',
        ),
    url(r'^gis-kelurahan-autocomplete/$', KelurahanBorderAutocomplete.as_view(),
        name='gis-kelurahan-autocomplete',
        ),

]
