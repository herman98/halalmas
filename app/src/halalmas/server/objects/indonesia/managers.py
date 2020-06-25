from django.db import models
from typing import List, Dict


class BuildingQuerySet(models.QuerySet):

    def all_buildings(self):
        return self.buildings.all()


class BuildingManager(models.Manager):

    def get_queryset(self):
        # return BuildingQuerySet(self.model)
        return BuildingQuerySet(self.model)

    def all_buildings(self):
        return self.get_queryset().all_buildings()
