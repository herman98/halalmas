from dal.autocomplete import Select2QuerySetView
import operator

from django.utils.html import escape
from django.db.models import Q

from dal import autocomplete

from .models import BankAccount, Bank


class BankAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Bank.objects.none()

        qs = Bank.objects.all()
        if self.q:
            qs = qs.filter(
                Q(code__icontains=self.q) |
                Q(name__icontains=self.q) |
                Q(country__icontains=self.q)).order_by(
                'code')[:50]
        return qs


class BankAccountAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return BankAccount.objects.none()

        qs = BankAccount.objects.all()
        if self.q:
            qs = qs.filter(
                Q(account_name__icontains=self.q) |
                Q(bank_branch__icontains=self.q) |
                Q(account_no__icontains=self.q) |
                Q(bank__name__icontains=self.q) |
                Q(bank__code__icontains=self.q)).order_by(
                '-cdate')[:50]
        return qs
