import json
from typing import List, Dict

from django.contrib.gis.db import models
from django.contrib.gis.geos import Point, Polygon, MultiPolygon
from cuser.fields import CurrentUserField

from halalmas.core import typing as typ
from halalmas.server.models import TimeStampedModel

from halalmas.server.objects.indonesia.models import KelurahanBorder


LONGITUDE_DIFF = 0.002200


class PointOfInterest(TimeStampedModel):
    """POI -> Point of Interest on Indonesia """

    poi_name = models.CharField(max_length=80, verbose_name='Name')
    is_radius = models.BooleanField(default=True, blank=True, null=True)

    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    json_multipolygon = models.TextField(blank=True, null=True)

    radius = models.FloatField(blank=True, null=True, verbose_name='Radius')
    geom_point_google = models.PointField(srid=4326, blank=True, null=True)
    geom_point_osm = models.PointField(srid=4326, blank=True, null=True)
    geom_multipolygon = models.MultiPolygonField(
        srid=4326, blank=True, null=True)

    is_active = models.BooleanField(default=True, blank=True, null=True)

    # user identification
    creator = CurrentUserField(related_name="gis_point_of_interests",
                               verbose_name="createby", on_delete=models.DO_NOTHING)
    # Manager

    class Meta:
        db_table = 'gis_point_of_interests'
        verbose_name = "Point Of Interest"
        verbose_name_plural = "Point Of Interests"
        ordering = ['poi_name']

    def set_coord_google(self):
        self.geom_point_google = Point(self.longitude, self.latitude)

    def extract_coord_to_lat_lon(self):
        self.longitude = self.coord_google.x
        self.latitude = self.coord_google.y

    def set_coord_osm(self):
        lon_google = self.longitude
        lat_google = self.latitude

        lon_osm = lon_google + LONGITUDE_DIFF
        self.geom_point_osm = Point(lon_osm, lat_google)

    def set_multipolygon(self):
        # https: // www.keene.edu/campus/maps/tool/
        # try:
        if self.json_multipolygon:
            json_data = json.loads(self.json_multipolygon)
            # print("json_data: {}".format(json_data))x`
            if json_data['type'] == 'Polygon':
                arr_poly = []
                for item in json_data['coordinates']:
                    # print("poly-item: {}".format(item))
                    poly = Polygon(item)
                    arr_poly.append(poly)
                    print("poly: {}".format(poly))
                self.geom_multipolygon = MultiPolygon(arr_poly)
            elif json_data['type'] == 'MultiPolygon':
                arr_poly = []
                for item in json_data['coordinates']:
                    # print("poly-item: {}".format(item))
                    poly = Polygon(item[0])
                    arr_poly.append(poly)
                    print("poly: {}".format(poly))
                self.geom_multipolygon = MultiPolygon(arr_poly)
            else:
                print("Type Geom:{} not supported !!".format(
                    json_data['type']))
        else:
            circle = None
            if self.geom_point_osm and self.radius:
                circle = self.geom_point_osm.buffer(self.radius)
            elif self.geom_point_google and self.radius:
                circle = self.geom_point_osm.buffer(self.radius)
            if circle:
                self.geom_multipolygon = MultiPolygon(circle)
        # except Exception as e:
        #     print("ERR-convert-multipolygon: {}".format(e))

    @property
    def coordinate(self):
        return self.geom_point_osm

    def save(self, *args, **kwargs):
        if self.longitude and self.latitude:
            self.set_coord_google()
        if self.geom_point_google:
            self.set_coord_osm()
        self.set_multipolygon()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.poi_name


class PointOfInterestCoverage(TimeStampedModel):
    """POI -> Point of Interest on Indonesia with Coverage by Indonesia Region """

    poi = models.ForeignKey(
        PointOfInterest, models.DO_NOTHING, verbose_name='Point Of Interest')
    coverage = models.ForeignKey(
        KelurahanBorder, models.DO_NOTHING, verbose_name='Coverage')

    class Meta:
        db_table = 'gis_poi_coverage'
        verbose_name = "Point Of Interest Coverage"
        verbose_name_plural = "Point Of Interests Coverage"
        # ordering = ['poi']

    def __str__(self) -> str:
        return self.poi.poi_name
