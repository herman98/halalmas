import operator

from django.utils.html import escape
from django.db.models import Q

from dal import autocomplete
from dal.autocomplete import Select2QuerySetView

from .models import WebScrapper, WebScrapperDetail


class WebScrapperAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return WebScrapper.objects.none()

        qs = WebScrapper.objects.all()
        if self.q:
            qs = qs.filter(
                Q(domain_name__icontains=self.q) |
                Q(location__icontains=self.q)).order_by(
                'domain_name', 'location')[:50]
        return qs


class WebScrapperDetailAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return WebScrapperDetail.objects.none()

        qs = WebScrapperDetail.objects.all()
        if self.q:
            qs = qs.filter(
                Q(urls_detail__icontains=self.q)).order_by(
                'urls_detail')[:50]
        return qs
