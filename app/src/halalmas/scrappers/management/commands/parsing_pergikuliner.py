import logging
from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Point

from halalmas.core.utils.pergikuliner_parsing import PergikulinerParsetoTempat


class ParsingPergikulinerData(object):
    def __init__(self, selection=None, count=None, charstart=None):
        self.selection = selection
        self.count = count
        self.charstart = charstart

    def parsing_data(self):
        print("self.selection: {}".format(self.selection))
        if self.selection == 'branch':
            self.run_parsing_branch()
        elif self.selection == 'reviews':
            self.run_parsing_reviews()
        elif self.selection == 'operatinghour':
            self.run_parsing_operating_hour()
        elif self.selection == 'tags':
            self.run_parsing_tags()
        elif self.selection == 'update_building':
            self.run_update_branch_building()
        elif self.selection == 'update_price':
            self.run_update_branch_price()
        elif self.selection == 'update_image':
            self.run_compress_branch_images()
        elif self.selection == 'compress_review_image':
            self.run_compress_branch_review_images()
        elif self.selection == 'compress_review_avatar':
            self.run_compress_branch_review_avatar()
        elif self.selection == 'update_group_activity':
            self.run_parse_branch_group_activity()
        else:
            print("no scrapping selected")

    def run_parsing_branch(self):
        PergikulinerParsetoTempat().parse_pergikuliner(self.count)

    def run_parsing_reviews(self):
        PergikulinerParsetoTempat().parse_pergikuliner_reviews(self.count)

    def run_parsing_operating_hour(self):
        PergikulinerParsetoTempat().parse_branch_operating_hour(self.count)

    def run_parsing_tags(self):
        PergikulinerParsetoTempat().parse_branch_tags(self.count)

    def run_update_branch_building(self):
        PergikulinerParsetoTempat().update_branch_building(self.count)

    def run_update_branch_price(self):
        PergikulinerParsetoTempat().update_branch_price(self.count)

    def run_compress_branch_images(self):
        PergikulinerParsetoTempat().compress_branch_images(self.count, self.charstart)

    def run_compress_branch_review_images(self):
        PergikulinerParsetoTempat().compress_branch_review_images(self.count)

    def run_compress_branch_review_avatar(self):
        PergikulinerParsetoTempat().compress_branch_review_avatar(self.count)

    def run_parse_branch_group_activity(self):
        PergikulinerParsetoTempat().parse_branch_group_activity(self.count)


class Command(BaseCommand):
    help = 'parsing pergikuliner scrap into halalmas DB'

    def add_arguments(self, parser):
        # parser.add_argument('mode', nargs='+', type=str)
        # parser.add_argument('mode', type=str, help='Indicates the number of users to be created')
        parser.add_argument('-select', '--selection', type=str,
                            help='parsing_pergikuliner, -select=parsing selections :(branch, reviews, operatinghour, tags, update_building, update_price, update_image, compress_review_image, compress_review_avatar, update_group_activity)', )
        parser.add_argument('-c', '--count', type=int,
                            help='Define a count to exececute ex: -c=100 for ten records only', )
        parser.add_argument('-cstart', '--charstart', type=str,
                            help='char branch start -cstart=a or b', )

    def handle(self, *args, **options):
        # mode = options.get('mode')
        count = options['count'] if options['count'] else 0
        selection = options['selection']
        charstart = options['charstart']
        print("mode selected: {}, {}".format(count, selection, charstart))

        ParsingPergikulinerData(selection, count, charstart).parsing_data()
