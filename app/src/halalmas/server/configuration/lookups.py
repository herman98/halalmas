from dal.autocomplete import Select2QuerySetView
import operator

from django.utils.html import escape
from django.db.models import Q

from dal import autocomplete

from .models import CalendarDimension


class CalendarDimensionAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return CalendarDimension.objects.none()

        qs = CalendarDimension.objects.all()
        if self.q:
            qs = qs.filter(
                Q(year__icontains=self.q) |
                Q(month__icontains=self.q)).order_by(
                'year', 'month')[:50]
        return qs
