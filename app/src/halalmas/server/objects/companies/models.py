from django.db import models
# from django.utils.safestring import mark_safe
from cuser.fields import CurrentUserField

from halalmas.server.models import TimeStampedModel
from halalmas.server.objects.buildings.models import Location
from .constants import OrganizationType, GroupType

class Company(TimeStampedModel):
    """
    This is master of Company data
    """
    OrganizationType = OrganizationType
    GroupType = GroupType

    name = models.CharField(max_length=125)
    organization_type = models.CharField(max_length=50,
                                         choices=OrganizationType.get_choices(
                                             True),
                                         blank=True, null=True,
                                         default=OrganizationType.PT,
                                         verbose_name="Tipe Organisasi",
                                         help_text="pick one of this organization type.")
    group_type = models.IntegerField(choices=GroupType.get_choices(),
                                     blank=True, null=True,
                                     default=GroupType.HOST,
                                     verbose_name="Tipe Host")
    npwp = models.CharField(max_length=125, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    post_code = models.CharField(max_length=25, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    siup = models.CharField(max_length=125, blank=True, null=True)
    owner_name = models.CharField(max_length=150, blank=True, null=True)

    location = models.ForeignKey(
        Location, models.DO_NOTHING, blank=True, null=True)
    
    kelurahan = models.CharField(max_length=150, blank=True, null=True)
    kecamatan = models.CharField(max_length=150, blank=True, null=True)
    kabupaten = models.CharField(max_length=150, blank=True, null=True)
    propinsi = models.CharField(max_length=150, blank=True, null=True)

    unit = models.CharField(max_length=50, blank=True, null=True)
    floor = models.CharField(max_length=50, blank=True, null=True)

    # user identification
    creator = CurrentUserField(related_name="m_company",
                               verbose_name="createby", on_delete=models.DO_NOTHING)

    # objects = CompanyManager()

    class Meta:
        db_table = "m_company"
        verbose_name_plural = u'Companies'
        ordering = ['name', 'group_type']

    @classmethod
    def create(cls, name, address, phone, post_code=None):
        _address_enc = address = str(address).encode('UTF-8')
        if post_code:
            cls_here = cls(name=name, address=_address_enc, time_start=phone)
        else:
            cls_here = cls(name=name, address=_address_enc, time_start=phone,
                           post_code=post_code)
        cls_here.save()
        return cls_here

    def __str__(self):
        return "{}".format(self.name)

    def save(self, *args, **kwargs):
        if self.location:
            self.kelurahan = self.location.kelurahan
            self.kecamatan = self.location.kecamatan
            self.kabupaten = self.location.kabupaten
            self.propinsi = self.location.propinsi
        super().save(*args, **kwargs)
       