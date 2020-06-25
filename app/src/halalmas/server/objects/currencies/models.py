from typing import List, Dict

from django.contrib.gis.db import models
from django.contrib.gis.geos import Point

from cuser.fields import CurrentUserField
from simple_history.models import HistoricalRecords

from halalmas.server.models import TimeStampedModel


class Currency(TimeStampedModel):
    """Currency list from Bank Indonesia lists """

    curr_name = models.CharField(
        max_length=80, verbose_name='Currency Name')
    curr_value = models.DecimalField(
        blank=True, null=True, max_digits=12, decimal_places=2)

    rate_sale = models.DecimalField(
        blank=True, null=True, max_digits=12, decimal_places=2)
    rate_buy = models.DecimalField(
        blank=True, null=True, max_digits=12, decimal_places=2)

    is_active = models.BooleanField(default=True, blank=True, null=True)

    # user identification
    creator = CurrentUserField(related_name="m_currency",
                               verbose_name="createby", on_delete=models.DO_NOTHING)
    # History
    history = HistoricalRecords(table_name='m_currency_upd_history')

    class Meta:
        db_table = 'm_currency'
        verbose_name = "Currency Rate"
        verbose_name_plural = "Currency Rates"
        ordering = ['curr_name']

    def __str__(self) -> str:
        return self.curr_name


class CurrencyHistory(TimeStampedModel):
    """Currency list from Bank Indonesia lists """

    currency = models.ForeignKey(
        Currency, models.DO_NOTHING, verbose_name='Selected Currency')

    curr_value = models.DecimalField(
        blank=True, null=True, max_digits=12, decimal_places=2)

    rate_sale = models.DecimalField(
        blank=True, null=True, max_digits=12, decimal_places=2)
    rate_buy = models.DecimalField(
        blank=True, null=True, max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'm_currency_history'
        verbose_name = "Currency Rate History"
        verbose_name_plural = "Currency Rate Histories"
        ordering = ['-cdate']

    def __str__(self) -> str:
        return self.currency.curr_name
