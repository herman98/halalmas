from __future__ import absolute_import
from __future__ import unicode_literals

from django.conf.urls import url
from django.urls import path

from .lookups import (BuildingAutocomplete, 
    BuildingCategoryAutocomplete,
    LocationAutocomplete)
from . import views

urlpatterns = [

    # auto-complete
    url(r'^building-autocomplete/$', BuildingAutocomplete.as_view(),
        name='building-autocomplete',
        ),

    url(r'^building-category-autocomplete/$', BuildingCategoryAutocomplete.as_view(),
        name='building-category-autocomplete',
        ),
    url(r'^location-autocomplete/$', LocationAutocomplete.as_view(),
        name='location-autocomplete',
        ),
]
