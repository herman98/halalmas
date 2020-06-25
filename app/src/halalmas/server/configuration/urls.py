from __future__ import unicode_literals
from __future__ import absolute_import

from django.urls import path
from django.conf.urls import url

from .lookups import CalendarDimensionAutocomplete
# from . import views

urlpatterns = [

    # auto-complete
    url(r'^calendar-dimension-autocomplete/$', CalendarDimensionAutocomplete.as_view(),
        name='calendar-dimension-autocomplete',
        ),

]
