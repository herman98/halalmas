from django.urls import path
from django.conf import settings
from django.utils.translation import ugettext_lazy
from django.conf.urls import include, url

urlpatterns = [
    path('user-profiles/', include(('halalmas.server.members.profiles.urls', 'user-profiles'),
                                   namespace='user-profiles')),

]
