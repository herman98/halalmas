from django.urls import path
from django.conf import settings
from django.utils.translation import ugettext_lazy
from django.conf.urls import include, url


urlpatterns = [
    path('company/', include(('halalmas.server.objects.companies.urls', 'company'),
                             namespace='company')),
    path('bank/', include(('halalmas.server.objects.banks.urls', 'bank'),
                          namespace='bank')),
    path('indonesia/', include(('halalmas.server.objects.indonesia.urls', 'gis-indonesia'),
                               namespace='gis-indonesia')),
    path('poi/', include(('halalmas.server.objects.poi.urls', 'gis-poi'),
                         namespace='gis-poi')),
    path('building/', include(('halalmas.server.objects.buildings.urls', 'building'),
                              namespace='building')),
    # path('world/', include(('halalmas.server.objects.world.urls', 'gis-world'),
    #                        namespace='gis-world')),
    # path('facility/', include(('halalmas.server.objects.facilities.urls', 'facility'),
    #                           namespace='facility')),
    # path('product/', include(('halalmas.server.objects.products.urls', 'product'),
    #                          namespace='product')),
    # path('space-setup/', include(('halalmas.server.objects.space_setups.urls', 'space-setup'),
    #                              namespace='space-setup')),
    # path('supports/', include(('halalmas.server.objects.supports.urls', 'supports'),
    #                              namespace='supports')),
#     path('branch_registration/', include(('halalmas.server.objects.supports.branch_registration.urls', 'branch_registration'),
#                              namespace='branch_registration')),
#     path('tags/', include(('halalmas.server.objects.tags.urls', 'tags'),
#                              namespace='tags')),
]
