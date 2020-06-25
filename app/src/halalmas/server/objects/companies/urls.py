from __future__ import absolute_import
from __future__ import unicode_literals

from django.conf.urls import url
from django.urls import path

from .lookups import CompanyAutocomplete
from . import views

urlpatterns = [

    # auto-complete
    url(r'^company-autocomplete/$', CompanyAutocomplete.as_view(),
        name='company-autocomplete',
        ),

]
