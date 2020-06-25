from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='default'),

    url(r'^admin$', views.dashboard_admin, name='admin'),
    # path('cra_team', views.dashboard_cra_team, name='cra_team'),
    # path('host_team', views.dashboard_host_team, name='host_team'),
    # path('finance', views.dashboard_finance, name='finance'),
    path('guests', views.dashboard_guests, name='guests'),
    # path('marketing', views.dashboard_marketing, name='marketing'),

    url(r'^update_default_role$', views.update_default_role,
        name='update_default_role'),

    # # ajax for oustanding bills finance
    # path('oustanding_bill', views.oustanding_bill, name='oustanding_bill'),
]
