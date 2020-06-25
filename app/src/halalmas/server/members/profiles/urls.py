from __future__ import absolute_import
from __future__ import unicode_literals

from django.conf.urls import url
from django.urls import path

from .lookups import UserProfileAutocomplete, UserAuthAutocomplete
# import views

urlpatterns = [

    # auto-complete
    url(r'^user-auth-autocomplete/$', UserAuthAutocomplete.as_view(),
        name='user-auth-autocomplete',
        ),
    url(r'^user-profile-autocomplete/$', UserProfileAutocomplete.as_view(),
        name='user-profile-autocomplete',
        ),

]

# from django.shortcuts import render_to_response, render
# from django.urls import reverse
# url = reverse('profiles:user-profile-autocomplete')
# redirect(url)
