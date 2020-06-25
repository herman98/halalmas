from __future__ import unicode_literals

import json
from django.db import models

class TimeStampedModel(models.Model):
    """
    This class as timestamp class models for each modeling in this project
    """

    class Meta(object):
        """
        this class set as abstractions
        """
        abstract = True

    cdate = models.DateTimeField(auto_now_add=True)
    udate = models.DateTimeField(auto_now=True)

    delstatus = models.BooleanField(default=False)
    deldate = models.DateTimeField(blank=True, null=True)


class JSONModel:
    def toJSON(self):
        self.cdate = self.cdate.strftime('%d-%m-%Y %H:%M')
        self.udate = self.udate.strftime('%d-%m-%Y %H:%M')
        rs = json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)
        rs = json.loads(rs)
        return rs


class TSQuerySet(models.QuerySet):
    def is_deleted(self):
        return self.filter(delstatus=True)
    
    def is_active(self):
        return self.filter(delstatus=False)

    def search_with_pk(self, id_here):
        return self.filter(pk=id_here)

    def active_with_pk(self, id_here):
        return self.is_active().filter(pk=id_here)
