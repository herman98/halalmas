"""tempat.com backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.conf import settings
from django.utils.translation import ugettext_lazy
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib import admin

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


HALALMAS_PROJ = getattr(settings, 'HALALMAS_PROJ', 'WEB_SERVER')
OBJECT_APPS = getattr(settings, 'OBJECT_APPS', tuple())
DEBUG = getattr(settings, 'DEBUG')
MEDIA_URL = getattr(settings, 'MEDIA_URL')
MEDIA_ROOT = getattr(settings, 'MEDIA_ROOT')
PROJECT_URL = getattr(settings, 'PROJECT_URL')
OPEN_API_URL = getattr(settings, 'OPEN_API_URL', False)

admin.autodiscover()


schema_view = get_schema_view(
   openapi.Info(
      title="halalmas API",
      default_version='v1',
      description="API's for halalmas.marikoding dot com web and mobile app",
      terms_of_service="https://halalmas.marikoding.com/policies/terms/",
      contact=openapi.Contact(email="budi.hermansyah@marikoding.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # core app urls
    # path('oauth2/', include('rest_framework_social_oauth2.urls')),

    # path('api/', include('halalmas.api.urls')),
    path('objects/', include('halalmas.server.objects.urls')),
    path('members/', include('halalmas.server.members.urls')),
    path('configuration/', include(('halalmas.server.configuration.urls', 'server-configuration'),
                                   namespace='server-configuration')),
    # path('hosts/', include('halalmas.server.hosts.urls')),
    # path('features/', include('halalmas.server.features.urls')),

    # path('orders/', include('halalmas.server.orders.urls')),
    # path('payments/', include('halalmas.server.payments.urls')),

    path('scrappers/', include('halalmas.scrappers.urls')),

    # admin URL
    path('admin/', admin.site.urls, name='admin'),
    # Authentication URL
    path('accounts/', include('django.contrib.auth.urls'), name='accounts'),

    # Dashboard
    path('dashboard/', include(('halalmas.crm.objects.dashboard.urls', 'dashboards'),
                               namespace='dashboard')),

    # social oauth
    # path('oauth/', include('social_django.urls', namespace='social')),
    path('oauth2_provider/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    
    # robots.txt
    # url(r'^robots.txt$', TemplateView.as_view(template_name="robots.txt",
    #                                           content_type="text/plain"), name="robots_file"),

]

if OPEN_API_URL == True:
    open_api_pattern = [
        # Route TemplateView to serve Swagger UI template.
        #   * Provide `extra_context` with view name of `SchemaView`.
        url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    ]
    urlpatterns = urlpatterns + open_api_pattern

if HALALMAS_PROJ == 'CRM':
    from .crm.views import (welcome, empty, logout_view,
                            login_view, index_page)
    crm_pattern = [

        # Default URL
        path('', welcome, name='index'),
        path('welcome', welcome, name='welcome'),
        path('empty', empty, name='empty'),

        # CRM url
        path('crm/', include('halalmas.crm.urls'), name='crm'),
    ]
    urlpatterns = urlpatterns + crm_pattern
else:
    from .server.views import welcome, empty
    addon_pattern = [

        # Default URL
        path('', welcome, name='index'),
        path('welcome', welcome, name='welcome'),
        path('empty', empty, name='empty'),

    ]
    urlpatterns = urlpatterns + addon_pattern


if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)

# Text to put at the end of each page's <title>.
admin.site.site_title = ugettext_lazy('TEMPAT DOT COM CRM')
# Text to put in each page's <h1> (and above login form).
admin.site.site_header = ugettext_lazy('halalmas-crm')
# Text to put at the top of the admin index page.
admin.site.index_title = ugettext_lazy('halalmas-crm administration')
