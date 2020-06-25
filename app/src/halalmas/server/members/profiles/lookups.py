import operator

from django.contrib.auth.models import User
from django.utils.html import escape
from django.db.models import Q

from dal import autocomplete
from dal.autocomplete import Select2QuerySetView

from .models import CustomerUserProfile


class UserProfileAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return CustomerUserProfile.objects.none()

        qs = CustomerUserProfile.objects.all()
        if self.q:
            qs = qs.filter(
                Q(user__username__icontains=self.q) |
                Q(user__email__icontains=self.q)).order_by(
                '-cdate')[:50]
        return qs


class UserAuthAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return User.objects.none()

        qs = User.objects.all()
        if self.q:
            qs = qs.filter(
                Q(username__icontains=self.q) |
                Q(email__icontains=self.q)).order_by(
                'username')[:50]
        return qs
