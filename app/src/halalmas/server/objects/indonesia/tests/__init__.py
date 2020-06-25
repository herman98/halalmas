"""
Notes:
Administrative area refer to Provinsi|Kabupaten|Kecamatan|Kelurahan

TODO:
1. Create unit test for every function in utils.py
2. Create unit test for every interface in interfaces.py

3. Test how long it takes to get buildings in Administrative area.
4. Test if the building is located in the correct Administrative area.
5. Test if the coordinate is outside Indonesia


./manage.py test halalmas.server.objects.indonesia.tests
Preserving the test database¶
The test --keepdb option preserves the test database between test runs. It skips the create and destroy actions which can greatly decrease the time to run tests.
"""

import os
import json

from django.test import TestCase
from django.contrib.gis.geos import Point
from django.contrib.gis.geos import MultiPolygon

from halalmas.core import typing as typ
from halalmas.core.exceptions import DataNotFound

from halalmas.server.objects.indonesia.models import KelurahanBorder
from halalmas.server.objects.indonesia import load
from halalmas.server.objects.indonesia.utils import to_OSM_coordinate
from halalmas.server.objects.buildings.models import Buildings

from .dataset import building_ds as data

# Administrative Area Name
JAKARTA = "Jakarta Raya"
SLIPI = "Slipi"
PALMERAH = "Palmerah"
KEMANGGISAN = "Kemanggisan"
JAKARTA_BARAT = "Jakarta Barat"

# Building
WISMA76 = "Wisma 76"

# TODO: Edit this to configure the dataset
# '/Users/sky/halalmas/server/data'
abs_path_data = os.path.dirname(__file__)

# Shapefile path
kelurahan_json = os.path.abspath(
    os.path.join(
        abs_path_data,
        'dataset', 'kelurahan_jakarta.json'
    ),
)

config = {
    "KELURAHAN_DATA": kelurahan_json,
    "BUILDING_DATA": data.BUILDING_JAKBAR
}

buildings = config['BUILDING_DATA']


def insert_kelurahan():
    json_data = open(config['KELURAHAN_DATA'])
    json_load = json.load(json_data)
    kelurahan_jakarta = json_load['jakarta']

    kelurahan_bulk = []
    for kelurahan in kelurahan_jakarta:
        kelurahan_bulk.append(
            KelurahanBorder(
                gid_0=kelurahan['gid_0'],
                name_0=kelurahan['name_0'],
                gid_1=kelurahan['gid_1'],
                name_1=kelurahan['name_1'],
                gid_2=kelurahan['gid_2'],
                name_2=kelurahan['name_2'],
                gid_3=kelurahan['gid_3'],
                name_3=kelurahan['name_3'],
                gid_4=kelurahan['gid_4'],
                name_4=kelurahan['name_4'],
                varname_4=kelurahan['varname_4'],
                type_4=kelurahan['type_4'],
                engtype_4=kelurahan['engtype_4'],
                cc_4=kelurahan['cc_4'],
                geom=kelurahan['geom'],
            )
        )

    KelurahanBorder.objects.bulk_create(kelurahan_bulk)


def insert_building():
    building_bulk = []

    for building in buildings:
        b = Buildings(
            name=building['name'],
            address=building['address'],
            coord_google=building['coord_google']
        )
        b.set_coord_osm()
        building_bulk.append(b)

    Buildings.objects.bulk_create(building_bulk)


def get_building(name) -> typ.Building:
    buildings = Buildings.objects.filter(name__icontains=name)
    if not buildings:
        raise DataNotFound("<Building {}> not found".format(name))
    wisma76 = buildings[0]

    return wisma76


def get_kelurahan_by_building_name(name) -> typ.KelurahanBorder:
    kelurahan = KelurahanBorder.objects.filter(name_4__icontains=name)
    if not kelurahan:
        raise DataNotFound("<KelurahanBorder {}> not found".format(name))

    return kelurahan[0]


def get_list_kelurahan_by_building_name(name) -> typ.KelurahanBorder:
    kelurahan = KelurahanBorder.objects.filter(name_4__icontains=name)
    if kelurahan.count() == 0:
        raise DataNotFound("<KelurahanBorder {}> not found".format(name))

    return kelurahan


class Wisma76TestCase(TestCase):

    def setUp(self):
        insert_kelurahan()
        insert_building()

    def test_total_building_inserted(self):
        """Check total building inserted"""

        total_building = Buildings.objects.count()
        # print("TOTAL Building: %d" % total_building)
        self.assertEqual(total_building, len(buildings))

    def test_if_wisma_76_in_slipi_palmerah_jakarta(self):
        wisma76 = get_building(WISMA76)

        # FIXME: coordinate hack
        # wisma76.coordinate = to_OSM_coordinate(wisma76.coordinate)
        kelurahan_wisma76 = wisma76.kelurahan

        self.assertEqual(kelurahan_wisma76.name_1, JAKARTA)
        self.assertEqual(kelurahan_wisma76.name_2, JAKARTA_BARAT)
        self.assertEqual(kelurahan_wisma76.name_3, PALMERAH)
        self.assertEqual(kelurahan_wisma76.name_4, SLIPI)


class AdmLv4TestCase(TestCase):

    def setUp(self):
        insert_kelurahan()
        insert_building()

    def test_total_building_inserted(self):
        """Check total building inserted"""

        total_building = Buildings.objects.count()
        # print("TOTAL Building: %d" % total_building)
        self.assertEqual(total_building, len(buildings))

    def test_building_in_kelurahan(self):
        for kel in data.KELURAHAN:
            print("Kelurahan: {}".format(kel))
            kelurahan = get_kelurahan_by_building_name(kel)
            building_in_kelurahan = kelurahan.buildings

            # print("Buliding in Slipi: {}".format(building_in_kelurahan))
            self.assertEqual(len(building_in_kelurahan),
                             len(data.kelurahan_buildings[kel]))

    def test_get_kemanggisan_border(self):
        should_be = {'tanjung duren selatan', 'tomang', 'kebon jeruk',
                     'jati pulo', 'kota bambu utara', 'kota bambu selatan',
                     'slipi', 'palmerah'}

        kemanggisan = get_kelurahan_by_building_name(KEMANGGISAN)
        kemanggisan_borders = kemanggisan.borders

        self.assertEqual(len(should_be), len(kemanggisan_borders))
        kemanggisan_borders_set = {kel.name_4.lower()
                                   for kel in kemanggisan_borders}

        is_should_be = kemanggisan_borders_set.issubset(should_be)
        self.assertEqual(is_should_be, True)

    def test_if_coordinate_outside_jakarta(self):
        MALAYSIA = Point(105.1210572, 4.1279304)
        LOMBOK = Point(115.9928062, -8.5830144)

        outside_jakarta = [LOMBOK, MALAYSIA]

        for pnt_wkt in outside_jakarta:
            kelurahan = KelurahanBorder.objects.filter(geom__contains=pnt_wkt)
            self.assertEqual(len(kelurahan), 0)

    def test_if_coordinate_inside_jakarta(self):
        REVENUE_TOWER = Point(106.804747, -6.2271981)
        DUFAN = Point(106.8297751, -6.1235476)

        outside_jakarta = [REVENUE_TOWER, DUFAN]

        for pnt_wkt in outside_jakarta:
            kelurahan = KelurahanBorder.objects.filter(geom__contains=pnt_wkt)
            self.assertNotEqual(len(kelurahan), 0)

    def test_points_inside_border(self):
        # 'https://stackoverflow.com/questions/37166891/geodjango-query-all-point-that-are-contained-into-a-multi-polygon'
        # list_poly = [
        #     kelurahan.geom for kelurahan in get_list_kelurahan_by_building_name(KEMANGGISAN)]
        # multipolygon = MultiPolygon(list_poly)
        kelurahan = get_kelurahan_by_building_name(KEMANGGISAN)
        if kelurahan:
            list_examples = Buildings.objects.filter(
                coord_osm__within=kelurahan)
            print("list_examples: {}".format(list_examples))
            self.assertEqual(len(list_examples), len(list_examples))
        self.assertEqual(True, False)
