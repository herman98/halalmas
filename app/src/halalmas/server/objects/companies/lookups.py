from dal.autocomplete import Select2QuerySetView
import operator

from django.utils.html import escape
from django.db.models import Q

from dal import autocomplete

from .models import Company


class CompanyAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Company.objects.none()

        qs = Company.objects.all()
        if self.q:
            qs = qs.filter(
                Q(name__icontains=self.q) |
                Q(npwp__icontains=self.q) |
                Q(owner_name__icontains=self.q)).order_by(
                '-cdate')[:50]
        return qs
