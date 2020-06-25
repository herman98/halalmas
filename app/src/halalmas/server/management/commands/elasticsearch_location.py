from django.core.management.base import BaseCommand, CommandError
from halalmas.api.service.elasticsearch.es_index.location import Location

class Command(BaseCommand):
    help = 'Auto complete re index for elasticsearch'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        Location().main()