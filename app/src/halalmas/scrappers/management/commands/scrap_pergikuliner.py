import logging
from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Point

from halalmas.core.utils.pergikuliner_scrapper import WebScrapping


class ScrappedData(object):
    def __init__(self, selection=None, count=None):
        self.selection = selection
        self.count = count
        self.DOMAIN_NAME_TO_SCRAP = 'https://pergikuliner.com'

    def scrap_data(self):
        print("self.selection: {}".format(self.selection))
        if self.selection == 'group':
            self.run_group()
        elif self.selection == 'detail':
            self.run_detail()
        elif self.selection == 'scraping_detail':
            self.run_scraping_detail()
        elif self.selection == 'scraping_scripts':
            self.run_scrap_scripts()
        else:
            print("no scrapping selected")

    def run_group(self):
        # 'https://pergikuliner.com/restoran/jakarta/?page=1'
        # url_master = ['restoran', ['jakarta', 'depok', 'bogor',
        #                            'tangerang', 'bekasi', 'bandung', 'surabaya']]
        url_master = ['restoran', ['jakarta', 'depok', 'bogor', 'tangerang', 'bekasi', 'bandung', 'surabaya',
                                   'jakarta/jakarta-utara', 'jakarta/jakarta-barat', 'jakarta/jakarta-timur',
                                   'jakarta/jakarta-selatan', 'jakarta/jakarta-pusat', 'tangerang/tangerang', 'tangerang/serpong']
                      ]
        # create scrap group
        for location in url_master[1]:
            print("location: {}".format(location))
            url_scrap_list = "{}/{}/{}/?page={}".format(
                self.DOMAIN_NAME_TO_SCRAP, url_master[0], location, "1")
            print("url_scrap_list: {}".format(url_scrap_list))

            WebScrapping(url_scrap_list, location,
                         self.count).listing_location()

    def run_detail(self):
        result = WebScrapping(1, 2, self.count).get_listing()
        print("result: {}".format(result))

    def run_scraping_detail(self):
        WebScrapping(3, 4, self.count).scrap_detail_page()

    def run_scrap_scripts(self):
        WebScrapping(5, 6, self.count).scrap_scripts()


class Command(BaseCommand):
    help = 'scrap pergikuliner web'

    def add_arguments(self, parser):
        # parser.add_argument('mode', nargs='+', type=str)
        # parser.add_argument('mode', type=str, help='Indicates the number of users to be created')
        parser.add_argument('-select', '--selection', type=str,
                            help='scrap_pergikuliner, -select=scrapping selections :(group, detail, scraping_detail, scraping_scripts)', )
        parser.add_argument('-c', '--count', type=int,
                            help='Define a count to exececute ex: -c=100 for ten records only', )

    def handle(self, *args, **options):
        # mode = options.get('mode')
        count = options['count'] if options['count'] else 0
        selection = options['selection']
        print("mode selected: {}, {}".format(count, selection))

        ScrappedData(selection, count).scrap_data()
