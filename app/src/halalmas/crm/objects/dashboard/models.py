from __future__ import absolute_import
from __future__ import unicode_literals


import hashlib
import random
import datetime
import logging

# from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User
from halalmas.server.models import TimeStampedModel

logger = logging.getLogger(__name__)


class CRMSetting(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role_select = models.CharField(max_length=60, null=True, blank=True)
    role_default = models.CharField(max_length=60, null=True, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = "crm_settings"
        verbose_name_plural = u'CRM Settings'

    def save(self, *args, **kwargs):
        # Calling Parent save() function
        super(CRMSetting, self).save(*args, **kwargs)
