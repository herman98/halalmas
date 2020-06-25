from django.db import models
# from django.utils.safestring import mark_safe
from cuser.fields import CurrentUserField
from simple_history.models import HistoricalRecords

from halalmas.server.models import TimeStampedModel

from .constants import CalendarDateType


class CalendarDimension(TimeStampedModel):
    """
    This is master of Calendar Dimension
    """
    year = models.IntegerField(verbose_name="Year")
    month = models.IntegerField(verbose_name="Month")

    class Meta:
        db_table = "m_calendar_dimension"
        verbose_name_plural = u'Calendar Dimensions'
        ordering = ['year', 'month']
        unique_together = ['year', 'month']

    def __str__(self):
        return "{}-{}".format(self.year, self.month)


class CalendarDate(TimeStampedModel):
    """
    This is master of Calendar Date
    """
    CalendarDateType = CalendarDateType
    dimension = models.ForeignKey(
        CalendarDimension, on_delete=models.DO_NOTHING)
    calendar_date = models.DateField(verbose_name="Calendar Date")
    status = models.CharField(max_length=50,
                              choices=CalendarDateType.get_choices(True),
                              blank=True, null=True,
                              default=CalendarDateType.WEEKDAY,
                              verbose_name="Status Date",
                              help_text="set categories for this date.")

    class Meta:
        db_table = "m_calendar_date"
        verbose_name_plural = u'Calendar Dates'
        ordering = ['dimension__year', 'dimension__month', 'calendar_date']

    def __str__(self):
        return "{}".format(self.calendar_date)


class ServerConfiguration(TimeStampedModel):
    """
    This is Backend Server Configuration
    """
    config_name = models.CharField(
        max_length=100, verbose_name="Configuration Name")
    config_value_int = models.FloatField(
        null=True, blank=True, verbose_name="Value in Number")
    config_value_str = models.CharField(null=True, blank=True,
                                        max_length=250, verbose_name="Value in String")
    config_status = models.BooleanField(
        default=False, verbose_name="Value in Boolean")

    description = models.CharField(max_length=1000, blank=True, null=True)

    is_active = models.BooleanField(
        default=True, blank=True, null=True)

    # History
    history = HistoricalRecords(table_name='m_server_configuration_history')

    class Meta:
        db_table = "m_server_configuration"
        verbose_name_plural = u'Server Configuration'
        ordering = ['config_name', ]

    def __str__(self):
        return "{}".format(self.config_name)
