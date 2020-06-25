from django.core.management.base import BaseCommand, CommandError
from tempatdotcom.api.service.elasticsearch.es_index.autocomplete import ESIndexAutocomplete

class Command(BaseCommand):
    help = 'Auto complete re index for elasticsearch'

    def add_arguments(self, parser):
        parser.add_argument('-m', '--mode', 
        type=str, help='input mode: -m=[reset/all/kel/kec/kab/prov/poi/building]')

    def handle(self, *args, **options):
        mode = options['mode']
        if mode == 'reset':
            ESIndexAutocomplete().remove_all()
        if mode == 'all':
            ESIndexAutocomplete().reindex_autocomplete()
        if mode == 'kel':
            ESIndexAutocomplete().kelurahan_autocomplete()
        if mode == 'kec':
            ESIndexAutocomplete().kecamatan_autocomplete()
        if mode == 'kab':
            ESIndexAutocomplete().kabupaten_autocomplete()
        if mode == 'prov':
            ESIndexAutocomplete().provinsi_autocomplete()
        if mode == 'poi':
            ESIndexAutocomplete().poi_autocomplete()
        if mode == 'building':
            ESIndexAutocomplete().building_autocomplete()            