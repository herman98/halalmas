from dal.autocomplete import Select2QuerySetView
import operator

from django.utils.html import escape
from django.db.models import Q

from dal import autocomplete

from .models import PointOfInterest


class PointOfInterestAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return PointOfInterest.objects.none()

        qs = PointOfInterest.objects.all()
        if self.q:
            qs = qs.filter(
                Q(poi_name__icontains=self.q)).order_by(
                'poi_name')[:50]
        return qs
