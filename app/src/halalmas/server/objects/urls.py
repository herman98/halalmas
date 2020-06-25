from django.urls import path
from django.conf import settings
from django.utils.translation import ugettext_lazy
from django.conf.urls import include, url


urlpatterns = [
    path('company/', include(('tempatdotcom.server.objects.companies.urls', 'company'),
                             namespace='company')),
    path('bank/', include(('tempatdotcom.server.objects.banks.urls', 'bank'),
                          namespace='bank')),
    path('indonesia/', include(('tempatdotcom.server.objects.indonesia.urls', 'gis-indonesia'),
                               namespace='gis-indonesia')),
    path('poi/', include(('tempatdotcom.server.objects.poi.urls', 'gis-poi'),
                         namespace='gis-poi')),
    path('world/', include(('tempatdotcom.server.objects.world.urls', 'gis-world'),
                           namespace='gis-world')),
    path('building/', include(('tempatdotcom.server.objects.buildings.urls', 'building'),
                              namespace='building')),
    path('facility/', include(('tempatdotcom.server.objects.facilities.urls', 'facility'),
                              namespace='facility')),
    path('product/', include(('tempatdotcom.server.objects.products.urls', 'product'),
                             namespace='product')),
    path('space-setup/', include(('tempatdotcom.server.objects.space_setups.urls', 'space-setup'),
                                 namespace='space-setup')),
    # path('supports/', include(('tempatdotcom.server.objects.supports.urls', 'supports'),
    #                              namespace='supports')),
    path('branch_registration/', include(('tempatdotcom.server.objects.supports.branch_registration.urls', 'branch_registration'),
                             namespace='branch_registration')),
    path('tags/', include(('tempatdotcom.server.objects.tags.urls', 'tags'),
                             namespace='tags')),
]
