from django.urls import path
from django.conf import settings
from django.utils.translation import ugettext_lazy
from django.conf.urls import include, url


urlpatterns = [
    url(r'^v1/', include('tempatdotcom.api.v1.urls')),
    url(r'^v2/', include('tempatdotcom.api.v2.urls')),
    url(r'^v3/', include('tempatdotcom.api.v3.urls')),
]
