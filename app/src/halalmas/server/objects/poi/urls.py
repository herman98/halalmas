from __future__ import unicode_literals
from __future__ import absolute_import

from django.urls import path
from django.conf.urls import url

from .lookups import PointOfInterestAutocomplete
# from . import views

urlpatterns = [

    # auto-complete
    url(r'^gis-poi-autocomplete/$', PointOfInterestAutocomplete.as_view(),
        name='gis-poi-autocomplete',
        ),

]
