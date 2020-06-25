from __future__ import absolute_import
from __future__ import unicode_literals

from django.conf.urls import url
from django.urls import path

from .lookups import BankAccountAutocomplete, BankAutocomplete
# from . import views

urlpatterns = [

    # auto-complete
    url(r'^bank-autocomplete/$', BankAutocomplete.as_view(),
        name='bank-autocomplete',
        ),
    url(r'^bank-account-autocomplete/$', BankAccountAutocomplete.as_view(),
        name='bank-account-autocomplete',
        ),

]
