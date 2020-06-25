from django.conf.urls import url
from django.urls import include, path

from rest_framework import routers

from django.conf import settings

from . import views

import django.views.static

router = routers.DefaultRouter()

urlpatterns = [
    url(r'^', include(router.urls)),

    path('auth/', include('rest_framework_social_oauth2.urls')),
    url(r'^user-token/', views.ObtainToken),
    url(r'^user-token-check/', views.CheckTokenExpired),
]
