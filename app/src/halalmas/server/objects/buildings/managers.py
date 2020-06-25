from django.db import models

from halalmas.server.models import TSQuerySet


class BuildingQuerySet(TSQuerySet):
    pass

class BuildingManager(models.Manager):
    def get_queryset(self):
        return BuildingQuerySet(self.model, using=self._db)
    
    def is_deleted(self):
        return self.get_queryset().is_deleted()
    
    def is_active(self):
        return self.get_queryset().is_active()

    def active_with_pk(self, id_here):
        return self.get_queryset().active_with_pk(id_here)
    
    def search_with_pk(self, id_here):
        return self.get_queryset().search_with_pk(id_here)


class BuildingategoryQuerySet(TSQuerySet):
    pass

class BuildingCategoryManager(models.Manager):
    def get_queryset(self):
        return BuildingategoryQuerySet(self.model, using=self._db)
    
    def is_deleted(self):
        return self.get_queryset().is_deleted()
    
    def is_active(self):
        return self.get_queryset().is_active()

    def active_with_pk(self, id_here):
        return self.get_queryset().active_with_pk(id_here)
    
    def search_with_pk(self, id_here):
        return self.get_queryset().search_with_pk(id_here)