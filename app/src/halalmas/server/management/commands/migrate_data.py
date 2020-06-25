import logging
from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Point

from xwork.models import Buildings, BuildingCategories, RatingMaster
from tempatdotcom.server.objects.buildings.models import Building as tmpt_Buildings
from tempatdotcom.server.objects.buildings.models import BuildingCategory as tmpt_BuildingsCat
from tempatdotcom.server.features.ratings_and_reviews.models import RatingReviewMasters as tmpt_RatingReviewMasters

from tempatdotcom.core.utils.xwork_data_migrations import HostDataMigrations


class MigrationData(object):
    def __init__(self, selection=None, mode=None):
        self.selection = selection
        self.mode = mode

    def migrate_data(self):
        print("self.selection: {}".format(self.selection))
        if self.selection == 'buildings':
            self.migrate_buildings()
        elif self.selection == 'building_categories':
            self.migrate_building_categories()
        elif self.selection == 'rating_master':
            self.migrate_m_rnr_master()
        elif self.selection in ['brands', 'rooms', 'cms_users']:
            HostDataMigrations(0, self.selection).run()
        else:
            print("no migrations selected")

    def migrate_building_categories(self):
        if self.mode > 0:
            # means with limit
            print("mode with limit {} seletected.".format(self.mode))
        else:
            # means all records
            print("START migrating Building Category")
            xwork_data_cat = BuildingCategories.objects.all()
            for item_cat in xwork_data_cat:
                obj_cat_save = tmpt_BuildingsCat(name=item_cat.name)
                obj_cat_save.save()
            print("DONE migrate Building Category")

    def migrate_buildings(self):
        if self.mode > 0:
            # means with limit
            print("mode with limit {} seletected.".format(self.mode))
        else:
            # means all records
            print("START migrating Buildings")
            xwork_data = Buildings.objects.filter(deleted_at__isnull=True)
            for idx, item_data in enumerate(xwork_data):
                print("#{} building id:{} name:{} {}".format(idx,
                                                             item_data.pk, item_data.name,
                                                             item_data.building_category))
                if item_data.building_category:
                    obj_cat_migrate = tmpt_BuildingsCat.objects.filter(
                        name=item_data.building_category.name)
                else:
                    obj_cat_migrate = tmpt_BuildingsCat.objects.filter(
                        pk=1)

                # Point(longitude, latitude)
                obj_save = tmpt_Buildings(
                    xwork_pk=item_data.pk,
                    name=item_data.name,
                    address=item_data.address,
                    latitude=item_data.lat,
                    longitude=item_data.lon,
                    # coord_google=Point(
                    #     item_data.lon, item_data.lat),
                    image_url=item_data.picture,
                    building_category=obj_cat_migrate[0],
                    description_id=item_data.description,
                    building_access_id=item_data.cara_akses,
                    is_facilities_id=item_data.fasilitas_tersedia,
                )
                obj_save.save()
            print("DONE migrate Buildings")

    def migrate_m_rnr_master(self):
        # means all records
        print("START migrating Rating Review Master")
        xwork_data = RatingMaster.objects.filter(deleted_at__isnull=True)
        for idx, item_data in enumerate(xwork_data):
            print("#{} rating-master id:{} rating_name:{}".format(idx,
                                                                  item_data.pk, item_data.rating_name))
            # Point(longitude, latitude)
            obj_save = tmpt_RatingReviewMasters(
                rating_name=item_data.rating_name,
                is_active=item_data.is_active,
            )
            obj_save.save()
        print("DONE migrate Rating Review Master")


class Command(BaseCommand):
    help = 'migrate data from xwork mysql into tempatdotcom postgresql'

    def add_arguments(self, parser):
        # parser.add_argument('mode', nargs='+', type=str)
        # parser.add_argument('mode', type=str, help='Indicates the number of users to be created')
        parser.add_argument('-select', '--selection', type=str,
                            help='migrate data, -select=buildings for migrate building data, others (building_categories, rating_master, rooms, cms_users)', )
        parser.add_argument('-m', '--mode', type=int,
                            help='Define a mode to exececute ex: -m=0 is all, -m=10 for ten records only', )

    def handle(self, *args, **options):
        # mode = options.get('mode')
        mode = options['mode'] if options['mode'] else 0
        selection = options['selection']
        print("mode selected: {}, {}".format(mode, selection))

        MigrationData(selection, mode).migrate_data()
