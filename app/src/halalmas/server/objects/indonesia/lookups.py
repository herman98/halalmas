from dal.autocomplete import Select2QuerySetView
import operator

from django.utils.html import escape
from django.db.models import Q

from dal import autocomplete

from .models import KelurahanBorder, KecamatanBorder, \
    KabupatenBorder, ProvinsiBorder


class KelurahanBorderAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return KelurahanBorder.objects.none()

        qs = KelurahanBorder.objects.all()
        if self.q:
            qs = qs.filter(
                Q(name_4__icontains=self.q) |
                Q(name_3__icontains=self.q) |
                Q(name_2__icontains=self.q) |
                Q(name_1__icontains=self.q) |
                Q(name_0__icontains=self.q)).order_by(
                'name_1', 'name_2', 'name_3', 'name_4')[:50]
        return qs


class KecamatanBorderAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return KecamatanBorder.objects.none()

        qs = KecamatanBorder.objects.all()
        if self.q:
            qs = qs.filter(
                Q(name_3__icontains=self.q) |
                Q(name_2__icontains=self.q) |
                Q(name_1__icontains=self.q) |
                Q(name_0__icontains=self.q)).order_by(
                'name_1', 'name_2', 'name_3')[:50]
        return qs


class KabupatenBorderAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return KabupatenBorder.objects.none()

        qs = KabupatenBorder.objects.all()
        if self.q:
            qs = qs.filter(
                Q(name_2__icontains=self.q) |
                Q(name_1__icontains=self.q) |
                Q(name_0__icontains=self.q)).order_by(
                'name_1', 'name_2',)[:50]
        return qs


class ProvinsiBorderAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return ProvinsiBorder.objects.none()

        qs = ProvinsiBorder.objects.all()
        if self.q:
            qs = qs.filter(
                Q(name_1__icontains=self.q) |
                Q(name_0__icontains=self.q)).order_by(
                'name_0', 'name_1', )[:50]
        return qs
