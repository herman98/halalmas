from django.urls import path
from django.conf import settings
from django.utils.translation import ugettext_lazy
from django.conf.urls import include, url


urlpatterns = [
    path('merchant/', include(('tempatdotcom.crm.objects.merchant.urls'))),
    path('buildings/', include(('tempatdotcom.crm.objects.building.urls', 'crm-buildings'), namespace='crm-buildings')),
    path('company/', include(('tempatdotcom.crm.objects.company.urls', 'crm-company'), namespace='crm-company')),

    path('booking/', include(('tempatdotcom.crm.objects.booking.urls'))),
    path('support/', include(('tempatdotcom.crm.objects.support.urls'))),
]