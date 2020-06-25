from typing import List, Dict

from django.contrib.gis.db import models

from halalmas.core import typing as typ
from halalmas.server.objects.buildings.models import Building as Buildings
from halalmas.server.models import TimeStampedModel

from .interfaces import IndonesiaAdministrativeArea, AreaPropertyInfo, AreaBookingInfo, AreaStatistic
from .managers import BuildingManager


# Model

class KelurahanBorder(TimeStampedModel, IndonesiaAdministrativeArea, AreaPropertyInfo):
    """Kelurahan = Administrative lv 4"""

    gid_0 = models.CharField(max_length=80)
    name_0 = models.CharField(max_length=80, verbose_name='Negara')
    gid_1 = models.CharField(max_length=80)
    name_1 = models.CharField(max_length=80, verbose_name='Propinsi')
    gid_2 = models.CharField(max_length=80)
    name_2 = models.CharField(max_length=80, verbose_name='Kabupaten')
    gid_3 = models.CharField(max_length=80)
    name_3 = models.CharField(max_length=80, verbose_name='Kecamatan')
    gid_4 = models.CharField(max_length=80)
    name_4 = models.CharField(max_length=80, verbose_name='Kelurahan')
    varname_4 = models.CharField(max_length=80)
    type_4 = models.CharField(max_length=80)
    engtype_4 = models.CharField(max_length=80)
    cc_4 = models.CharField(max_length=80)

    slug_0 = models.CharField(max_length=255, blank=True, null=True)
    slug_1 = models.CharField(max_length=255, blank=True, null=True)
    slug_2 = models.CharField(max_length=255, blank=True, null=True)
    slug_3 = models.CharField(max_length=255, blank=True, null=True)
    slug_4 = models.CharField(max_length=255, blank=True, null=True)

    geom = models.MultiPolygonField(srid=4326)

    # Manager
    objects = models.Manager()
    building_mgr = BuildingManager()

    class Meta:
        db_table = 'gis_kelurahan'
        verbose_name = "Kelurahan"
        verbose_name_plural = "Kelurahan"
        ordering = ['name_1', 'name_2', 'name_3', 'name_4']

    def __str__(self) -> str:
        return "{}->{}->{}->{}".format(self.name_1, self.name_2,  self.name_3, self.name_4)

    @property
    def adm_lv(self) -> int:
        return 4

    @property
    def negara(self) -> str:
        return self.name_0

    @property
    def provinsi(self) -> str:
        return self.name_1

    @property
    def kabupaten(self) -> str:
        return self.name_2

    @property
    def kecamatan(self) -> str:
        return self.name_3

    @property
    def kelurahan(self) -> str:
        return self.name_4

    @property
    def buildings(self):
        return Buildings.objects.filter(coord_osm__within=self.geom)

    @property  # nearest neear by
    def borders(self):
        return KelurahanBorder.objects.filter(geom__touches=self.geom)

    @property
    def border_buildings(self):
        borders = self.borders
        _border_buildings = []
        for border in borders:
            buildings = Buildings.objects.filter(coord_osm__within=border.geom)
            if buildings:
                for b in buildings:
                    _border_buildings.append(b)

        return _border_buildings

    @staticmethod
    def sample_data(self) -> Dict[str, str]:
        return {
            '_state': '< django.db.models.base.ModelState at 0x113318f60 >',
            'id': 2,
            'gid_0': 'IDN',
            'name_0': 'Indonesia',
            'gid_1': 'IDN.1_1',
            'name_1': 'Aceh',
            'gid_2': 'IDN.1.2_1',
            'name_2': 'Aceh Barat',
            'gid_3': 'IDN.1.2.1_1',
            'name_3': 'Arongan Lambalek',
            'gid_4': 'IDN.1.2.1.2_1',
            'name_4': 'Alue Batee',
            'varname_4': '',
            'type_4': 'Desa',
            'engtype_4': 'Village',
            'cc_4': '1107062027',
            'geom': '< MultiPolygon object at 0x112d46d58 >'
        }


class KecamatanBorder(TimeStampedModel, IndonesiaAdministrativeArea, AreaPropertyInfo):
    """Kecamatan = Administrative lv 3"""

    gid_0 = models.CharField(max_length=80)
    name_0 = models.CharField(max_length=80, verbose_name='Negara')
    gid_1 = models.CharField(max_length=80)
    name_1 = models.CharField(max_length=80, verbose_name='Propinsi')
    nl_name_1 = models.CharField(max_length=80)
    gid_2 = models.CharField(max_length=80)
    name_2 = models.CharField(max_length=80, verbose_name='Kabupaten')
    nl_name_2 = models.CharField(max_length=80)
    gid_3 = models.CharField(max_length=80)
    name_3 = models.CharField(max_length=80, verbose_name='Kecamatan')
    varname_3 = models.CharField(max_length=80)
    nl_name_3 = models.CharField(max_length=80)
    type_3 = models.CharField(max_length=80)
    engtype_3 = models.CharField(max_length=80)
    cc_3 = models.CharField(max_length=80)
    hasc_3 = models.CharField(max_length=80)
    
    slug_0 = models.CharField(max_length=255, blank=True, null=True)
    slug_1 = models.CharField(max_length=255, blank=True, null=True)
    slug_2 = models.CharField(max_length=255, blank=True, null=True)
    slug_3 = models.CharField(max_length=255, blank=True, null=True)
    
    geom = models.MultiPolygonField(srid=4326)


    class Meta:
        # app_label = 'KabupatenBorder'
        db_table = 'gis_kecamatan'
        verbose_name = "Kecamatan"
        verbose_name_plural = "Kecamatan"
        ordering = ['name_1', 'name_2', 'name_3']

    def __str__(self) -> str:
        return "{}->{}->{}".format(self.name_1, self.name_2,  self.name_3)

    @property
    def negara(self):
        return self.name_0

    @property
    def provinsi(self):
        return self.name_1

    @property
    def kabupaten(self):
        return self.name_2

    @property
    def kecamatan(self):
        return self.name_3

    @property
    def Kelurahan(self):
        return KelurahanBorder.objects.filter(gid_3=self.gid_3)

    @staticmethod
    def sample_data(self):
        return {
            '_state': '< django.db.models.base.ModelState at 0x12c5950b8 >',
            'id': 1,
            'gid_0': 'IDN',
            'name_0': 'Indonesia',
            'gid_1': 'IDN.1_1',
            'name_1': 'Aceh',
            'nl_name_1': '',
            'gid_2': 'IDN.1.2_1',
            'name_2': 'Aceh Barat',
            'nl_name_2': '',
            'gid_3': 'IDN.1.2.1_1',
            'name_3': 'Arongan Lambalek',
            'varname_3': '',
            'nl_name_3': '',
            'type_3': 'Kecamatan',
            'engtype_3': 'Sub-district',
            'cc_3': '1107062',
            'hasc_3': '',
            'geom': '< MultiPolygon object at 0x112cee2b8 >'
        }


class KabupatenBorder(TimeStampedModel, IndonesiaAdministrativeArea, AreaPropertyInfo):
    """Kabupaten = Administrative lv 2"""

    gid_0 = models.CharField(max_length=80)
    name_0 = models.CharField(max_length=80, verbose_name='Negara')
    gid_1 = models.CharField(max_length=80)
    name_1 = models.CharField(max_length=80, verbose_name='Propinsi')
    nl_name_1 = models.CharField(max_length=80)
    gid_2 = models.CharField(max_length=80)
    name_2 = models.CharField(max_length=80, verbose_name='Kabupaten/Kota')
    varname_2 = models.CharField(max_length=80)
    nl_name_2 = models.CharField(max_length=80)
    type_2 = models.CharField(max_length=80)
    engtype_2 = models.CharField(max_length=80)
    cc_2 = models.CharField(max_length=80)
    hasc_2 = models.CharField(max_length=80)

    slug_0 = models.CharField(max_length=255, blank=True, null=True)
    slug_1 = models.CharField(max_length=255, blank=True, null=True)
    slug_2 = models.CharField(max_length=255, blank=True, null=True)
    
    geom = models.MultiPolygonField(srid=4326)

    class Meta:
        # app_label = 'KabupatenBorder'
        db_table = 'gis_kabupaten'
        verbose_name = "Kabupaten / Kota"
        verbose_name_plural = "Kabupaten / Kota"
        ordering = ['name_1', 'name_2']

    def __str__(self) -> str:
        return "{}->{}".format(self.name_1, self.name_2)

    @property
    def negara(self):
        return self.name_0

    @property
    def provinsi(self):
        return self.name_1

    @property
    def kabupaten(self):
        return self.name_2

    @property
    def kecamatan(self):
        return KecamatanBorder.objects.filter(gid_2=self.gid_2)

    @property
    def kelurahan(self):
        return KelurahanBorder.objects.filter(gid_2=self.gid_2)

    @staticmethod
    def sample_data(self):
        return {
            '_state': '< django.db.models.base.ModelState at 0x12c0e1a90 >',
            'id': 1,
            'gid_0': 'IDN',
            'name_0': 'Indonesia',
            'gid_1': 'IDN.1_1',
            'name_1': 'Aceh',
            'nl_name_1': '',
            'gid_2': 'IDN.1.2_1',
            'name_2': 'Aceh Barat',
            'varname_2': '',
            'nl_name_2': '',
            'type_2': 'Kabupaten',
            'engtype_2': 'Regency',
            'cc_2': '1107',
            'hasc_2': 'ID.AC.AB',
            'geom': '< MultiPolygon object at 0x112cee1a8 >'
        }


class ProvinsiBorder(TimeStampedModel, IndonesiaAdministrativeArea, AreaPropertyInfo):
    """Provinsi = Administrative lv 1"""

    gid_0 = models.CharField(max_length=80)
    name_0 = models.CharField(max_length=80, verbose_name='Negara')
    gid_1 = models.CharField(max_length=80)
    name_1 = models.CharField(max_length=80, verbose_name='Propinsi')
    varname_1 = models.CharField(max_length=80)
    nl_name_1 = models.CharField(max_length=80)
    type_1 = models.CharField(max_length=80)
    engtype_1 = models.CharField(max_length=80)
    cc_1 = models.CharField(max_length=80)
    hasc_1 = models.CharField(max_length=80)

    slug_0 = models.CharField(max_length=255, blank=True, null=True)
    slug_1 = models.CharField(max_length=255, blank=True, null=True)

    geom = models.MultiPolygonField(srid=4326)

    class Meta:
        db_table = 'gis_propinsi'
        verbose_name = "Propinsi"
        verbose_name_plural = "Propinsi"
        ordering = ['name_1']

    # def __str__(self) -> str:
    #     return "{}->{}".format(self.name_0, self.name_1)

    @property
    def negara(self):
        return self.name_0

    @property
    def provinsi(self):
        return self.name_1

    @property
    def kabupaten(self):
        return KabupatenBorder.objects.filter(gid_1=self.gid_1)

    @property
    def kecamatan(self):
        return KecamatanBorder.objects.filter(gid_1=self.gid_1)

    @property
    def kelurahan(self):
        return KelurahanBorder.objects.filter(gid_1=self.gid_1)

    @property
    def buildings(self):
        """
        Select all building in this region self.gid_1

        """
        # TODO: connect to building object
        # provinsiBuilding = ProvinsiBuilding.objects.filter(gid_1=self.gid_1)
        # building_ids = [pb.building_id for pb in provinsiBuilding]
        # buildings = Buildings.objects.get(id__in=building_ids)

        # return buildings

    @staticmethod
    def sample_data(self):
        return {
            '_state': '< django.db.models.base.ModelState at 0x12c0e1320 >',
            'id': 1,
            'gid_0': 'IDN',
            'name_0': 'Indonesia',
            'gid_1': 'IDN.1_1',
            'name_1': 'Aceh',
            'varname_1': '',
            'nl_name_1': '',
            'type_1': 'Propinisi',
            'engtype_1': 'Province',
            'cc_1': '11',
            'hasc_1': 'ID.AC',
            'geom': '< MultiPolygon object at 0x112cee560 >'
        }
