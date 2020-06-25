from django.urls import path
from django.conf import settings
from django.utils.translation import ugettext_lazy
from django.conf.urls import include, url


urlpatterns = [
    path('merchant-registration/', include(('halalmas.crm.objects.support.merchant_registration.urls', 'crm-merchant-registration'), 
        namespace='crm-merchant-registration')),
   
]   
