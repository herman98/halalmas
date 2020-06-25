import logging

from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe

from storages.backends.s3boto3 import S3Boto3Storage
from cuser.fields import CurrentUserField

from halalmas.server.models import TimeStampedModel


logger = logging.getLogger(__name__)


class AuditTrail(TimeStampedModel):

    obj_model = models.CharField(
        max_length=500, verbose_name='Object Model',
                                      blank=True, null=True)
    server = models.CharField(max_length=50, verbose_name='Server',
                                      blank=True, null=True)
    remote_address = models.CharField(max_length=50,
                                      blank=True, null=True)
    ref_type = models.CharField(max_length=50, verbose_name='Ref Type',
                                      blank=True, null=True)
    ref_value = models.IntegerField(verbose_name='Ref Value(INT)',
                                      blank=True, null=True)
    message = models.TextField(verbose_name='Message',
                                      blank=True, null=True)
    is_alert = models.BooleanField(default=False)

    # user identification
    creator = CurrentUserField(related_name="m_audit_trail",
                               verbose_name="createby", on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "m_audit_trail"
        verbose_name = u'Audit Trail'
        verbose_name_plural = u'Audit Trails'

    def __str__(self):
        return "{}".format(self.obj_model)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
       

    
