from django.urls import path
from django.conf import settings
from django.utils.translation import ugettext_lazy
from django.conf.urls import include, url


urlpatterns = [
    # path('merchant/', include(('halalmas.crm.objects.merchant.urls'))),
    path('buildings/', include(('halalmas.crm.objects.building.urls', 'crm-buildings'), namespace='crm-buildings')),
    path('company/', include(('halalmas.crm.objects.company.urls', 'crm-company'), namespace='crm-company')),

    # path('booking/', include(('halalmas.crm.objects.booking.urls'))),
    # path('support/', include(('halalmas.crm.objects.support.urls'))),
]