from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.utils.safestring import mark_safe

from cuser.fields import CurrentUserField
from simple_history.models import HistoricalRecords

from halalmas.core import typing as typ
from halalmas.server.models import TimeStampedModel, JSONModel
from halalmas.server.objects.indonesia import utils as iu

from .constants import TransportationType
from .managers import BuildingManager, BuildingCategoryManager


COORDINATE = Point(0, 0)
JAKARTA = Point(-5.7759362, 106.1174984)
JAKARTA = 'POINT(-5.7773029 106.1175071)'

LONGITUDE_DIFF = 0.002200


class BuildingCategory(TimeStampedModel, JSONModel):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000, null=True, blank=True)

    objects = BuildingCategoryManager()

    class Meta:
        db_table = 'm_building_categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class PublicTransport(TimeStampedModel, JSONModel):
    TransportationType = TransportationType

    name = models.CharField(max_length=255)

    description_id = models.CharField(max_length=5000, blank=True, null=True)
    is_desc_id = models.BooleanField(default=False, blank=True, null=True)

    description_en = models.CharField(max_length=5000, blank=True, null=True)
    is_desc_en = models.BooleanField(default=False, blank=True, null=True)

    transport_type = models.IntegerField(choices=TransportationType.get_choices(True),
                                         default=TransportationType.BUS,
                                         blank=True, null=True)

    class Meta:
        db_table = 'm_public_transports'
        ordering = ['name']
        verbose_name = u'Public Transport'
        verbose_name_plural = u'Public Transports'

    def __str__(self):
        return "[{}]-{}".format(self.get_transport_type_display(), self.name, )


class Location(TimeStampedModel, JSONModel):
    
    name = models.CharField(max_length=125)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    coord_google = models.PointField(default=COORDINATE,
        blank=True, null=True)
    coord_osm = models.PointField(default=COORDINATE,
        blank=True, null=True)

    class Meta:
        db_table = 'm_locations'
        ordering = ['name']

    def set_coord_google(self):
        self.coord_google = Point(self.longitude, self.latitude)

    def extract_coord_to_lat_lon(self):
        self.longitude = self.coord_google.x
        self.latitude = self.coord_google.y

    def set_coord_osm(self):
        lon_google = self.coord_google.x
        lat_google = self.coord_google.y

        lon_osm = lon_google + LONGITUDE_DIFF
        self.coord_osm = Point(lon_osm, lat_google)

    @property
    def coordinate(self):
        return self.coord_osm

    def save(self, *args, **kwargs):
        if self.longitude and self.latitude:
            self.set_coord_google()

        if self.coord_google:
            # self.extract_coord_to_lat_lon()
            self.set_coord_osm()
        
        super().save(*args, **kwargs)

    def gis_location(self) -> typ.KelurahanBorder:
        if self.latitude and self.longitude:
            kelurahan = iu.get_kelurahan_by_coordinate(self.coord_osm)
            return kelurahan
        else:
            return None

    @property
    def kelurahan(self):
        if self.gis_location():
            kelurahan = self.gis_location().name_4
            return kelurahan
        else:
            return ''
    
    @property
    def kecamatan(self):
        if self.gis_location():
            kecamatan = self.gis_location().name_3
            return kecamatan
        else:
            return ''
    
    @property
    def kabupaten(self):
        if self.gis_location():
            kabupaten = self.gis_location().name_2
            return kabupaten
        else:
            return ''
    
    @property
    def propinsi(self):
        if self.gis_location():
            propinsi = self.gis_location().name_1
            return propinsi
        else:
            return ''

    def __str__(self):
        return self.name

class Building(TimeStampedModel, JSONModel):
    building_category = models.ForeignKey(
        BuildingCategory, models.DO_NOTHING, blank=True, null=True)

    public_transport = models.ManyToManyField(
        PublicTransport)

    name = models.CharField(max_length=125)
    slug = models.SlugField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=1500, blank=True, null=True)
    kodepos = models.CharField(max_length=10, blank=True, null=True)

    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    coord_google = models.PointField(default=COORDINATE)
    coord_osm = models.PointField(default=COORDINATE)

    description_id = models.CharField(max_length=5000, blank=True, null=True)
    building_access_id = models.CharField(
        max_length=5000, blank=True, null=True)
    facilities_id = models.CharField(
        max_length=5000, blank=True, null=True)
    is_desc_id = models.BooleanField(default=False, blank=True, null=True)
    is_building_access_id = models.BooleanField(
        default=False, blank=True, null=True)
    is_facilities_id = models.BooleanField(
        default=False, blank=True, null=True)

    description_en = models.CharField(max_length=5000, blank=True, null=True)
    building_access_en = models.CharField(
        max_length=5000, blank=True, null=True)
    facilities_en = models.CharField(
        max_length=5000, blank=True, null=True)
    is_desc_en = models.BooleanField(default=False, blank=True, null=True)
    is_building_access_en = models.BooleanField(
        default=False, blank=True, null=True)
    is_facilities_en = models.BooleanField(
        default=False, blank=True, null=True)

    operational_hour_per_day = models.IntegerField(blank=True, null=True)
    operational_day_per_week = models.IntegerField(blank=True, null=True)
    operational_day_per_month = models.IntegerField(blank=True, null=True)
    image_url = models.CharField(max_length=255, blank=True, null=True)

    xwork_pk = models.IntegerField(null=True, blank=True)

    # user identification
    creator = CurrentUserField(related_name="m_buildings",
                               verbose_name="createby", on_delete=models.DO_NOTHING)

    # History
    history = HistoricalRecords(table_name='m_buildings_history')

    objects = BuildingManager()
    
    class Meta:
        db_table = 'm_buildings'
        ordering = ['name']

    def set_coord_google(self):
        self.coord_google = Point(self.longitude, self.latitude)

    def extract_coord_to_lat_lon(self):
        self.longitude = self.coord_google.x
        self.latitude = self.coord_google.y

    def set_coord_osm(self):
        lon_google = self.coord_google.x
        lat_google = self.coord_google.y

        lon_osm = lon_google + LONGITUDE_DIFF
        self.coord_osm = Point(lon_osm, lat_google)

    def set_status_desc(self):
        self.is_desc_id = True if self.description_id else False
        self.is_building_access_id = True if self.building_access_id else False
        self.is_facilities_id = True if self.facilities_id else False

        self.is_desc_en = True if self.description_en else False
        self.is_building_access_en = True if self.building_access_en else False
        self.is_facilities_en = True if self.facilities_en else False

    @property
    def coordinate(self):
        return self.coord_osm

    def save(self, *args, **kwargs):
        if self.longitude and self.latitude:
            self.set_coord_google()

        if self.coord_google:
            # self.extract_coord_to_lat_lon()
            self.set_coord_osm()
        # set status automation
        self.set_status_desc()
        super().save(*args, **kwargs)

    @property
    def kelurahan(self) -> typ.KelurahanBorder:
        # print(f"kelurahan {self.pk} {self.latitude} and {self.longitude} and {self.coord_osm}")
        if self.latitude and self.longitude and self.coord_osm:
            try:
                kelurahan = iu.get_kelurahan_by_coordinate(self.coord_osm)
                return kelurahan
            except Exception as e:
                return None
        else:
            return None

    def __str__(self):
        return self.name
    
    def image(self, width=None, height=None):
        if self.image_url is not None and self.image_url != '':
            prefix = 'img/sm_'
            _image_url = self.image_url
            # print(f"_image_url: {_image_url}")
            filename_here = _image_url.split('/')[-1]
            base_url = _image_url.replace(filename_here,'')
            if filename_here:
                filename_here = filename_here.split("?")[0]
            new_url = "{}{}{}".format(base_url, prefix, filename_here)
            # print(f"new_url: {new_url}")
            return mark_safe('<img src="{url}" width="{width}" height={height} style="border-radius: 5px" />'.format(
                    url=new_url,
                    width=width,
                    height=height,
                )
            )
        else:
            return '-nologo-'

    @property
    def logo_image(self):
        return self.image(160, 160)

    @property
    def logo_image_sm(self):
        return self.image(80, 40)
    
    @property
    def logo_image_md(self):
        return self.image(120, 50)

    @property
    def logo_image_md_width(self):
        return self.image(100)


class PopularMall(TimeStampedModel):
    building = models.ForeignKey(
        Building, models.DO_NOTHING, verbose_name='Building/Mall')

    sequence = models.SmallIntegerField(blank=True, null=True)
    
    class Meta:
        db_table = 'm_popular_mall'
        ordering = ['sequence']
        verbose_name = u'Popular Mall'
        verbose_name_plural = u'Popular Mall'

    def __str__(self):
        return "{}-{}".format(self.building.name, self.sequence)

# class BuildingPublicTransport(TimeStampedModel):
#     """POI -> Point of Interest on Indonesia """

#     building = models.ForeignKey(
#         Buildings, models.DO_NOTHING, verbose_name='Point Of Interest')
#     public_transport = models.CharField(
#         PublicTransport, models.DO_NOTHING, verbose_name='Coverage')

#     class Meta:
#         db_table = 'm_building_public_transport'
#         verbose_name = "Building Public Transport"
#         verbose_name_plural = "Building Public Transports"

#     def __str__(self) -> str:
#         return "{}-{}".format(self.building, self.public_transport)
