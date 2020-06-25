from django.core.management.base import BaseCommand, CommandError
from halalmas.api.service.elasticsearch.es_index.branch import ESIndexBranch

class Command(BaseCommand):
    help = 'Branch Listing re index for elasticsearch'

    def add_arguments(self, parser):
        parser.add_argument('-m', '--mode',
        type=str, help='input mode: -m=[reindex/update/happyhour] | default = update')


    def handle(self, *args, **options):
        mode = options['mode']
        if mode == 'update':
            ESIndexBranch().main(update=True)
        elif mode == 'reindex':    
            ESIndexBranch().main()
        elif mode == 'happyhour':    
            ESIndexBranch().main(
                update=True, 
                is_happy_hour=True)
        else:
            ESIndexBranch().main(update=True)

