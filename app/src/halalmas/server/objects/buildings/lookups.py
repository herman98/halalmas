import operator

from django.contrib.auth.models import User
from django.utils.html import escape
from django.db.models import Q

from dal import autocomplete
from dal.autocomplete import Select2QuerySetView

from .models import Building, BuildingCategory, Location


class BuildingAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Building.objects.none()

        qs = Building.objects.all()
        if self.q:
            qs = qs.filter(
                Q(name__icontains=self.q) |
                Q(address__icontains=self.q) |
                Q(description_id__icontains=self.q)).order_by(
                '-cdate')[:50]
        return qs


class BuildingCategoryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return BuildingCategory.objects.none()

        qs = BuildingCategory.objects.is_active()
        if self.q:
            qs = qs.filter(
                Q(name__icontains=self.q)).order_by(
                'name')[:50]
        return qs

class LocationAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Location.objects.none()

        qs = Location.objects.all()
        if self.q:
            qs = qs.filter(
                Q(name__icontains=self.q) |
                Q(latitude__icontains=self.q)|
                Q(longitude__icontains=self.q)).order_by(
                '-cdate')[:50]
        return qs