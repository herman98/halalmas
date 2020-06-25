from django.urls import path
from django.conf import settings
from django.utils.translation import ugettext_lazy
from django.conf.urls import include, url

from .lookups import WebScrapperAutocomplete, WebScrapperDetailAutocomplete

urlpatterns = [
    # autocomplete
    url(r'^scrapper-autocomplete/$', WebScrapperAutocomplete.as_view(),
        name='scrapper-autocomplete',
        ),
    url(r'^scrapper-detail-autocomplete/$', WebScrapperDetailAutocomplete.as_view(),
        name='scrapper-detail-autocomplete',
        ),

    path('pergikuiner/', include(('tempatdotcom.scrappers.pergikuliner.urls', 'pergikuliner'),
                                 namespace='pergikuliner')),

]
