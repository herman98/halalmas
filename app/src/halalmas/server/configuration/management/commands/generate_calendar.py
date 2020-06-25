import pandas
import calendar

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from tempatdotcom.server.configuration.functions import GenerateCalendarDate


class Command(BaseCommand):
    help = 'generate calendar dates using year input'

    def add_arguments(self, parser):
        parser.add_argument('-y', '--year', type=int,
                            help='input year, -y=2017', )

    def handle(self, *args, **options):
        # mode = options.get('mode')
        year_selected = options['year'] if options['year'] else 0
        print("year_selected: {}".format(year_selected))

        GenerateCalendarDate(year_selected).generate()
