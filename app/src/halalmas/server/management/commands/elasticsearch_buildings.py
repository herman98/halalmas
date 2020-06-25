from django.core.management.base import BaseCommand, CommandError
from halalmas.api.service.elasticsearch.es_index.buildings import ESIndexBuilding

class Command(BaseCommand, ESIndexBuilding):
    help = 'Auto complete re index for elasticsearch'

    def add_arguments(self, parser):
        parser.add_argument('-m', '--mode', 
        type=str, help='input mode: -m=[reset/all/kel/kec/kab/prov/poi]')

    def handle(self, *args, **options):
        self.main()
    
        
        
        
