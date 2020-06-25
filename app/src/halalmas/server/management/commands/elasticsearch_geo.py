from django.core.management.base import BaseCommand, CommandError
from halalmas.api.service.elasticsearch.es_index.geom import ESIndexPOI, ESIndexProvinsi, ESIndexKabupaten, ESIndexKecamatan, ESIndexKelurahan

class Command(BaseCommand):
    help = 'Auto complete re index for elasticsearch'

    def add_arguments(self, parser):
        parser.add_argument('-m', '--mode', 
        type=str, help='input mode: -m=[reset/all/kel/kec/kab/prov/poi]')

    def handle(self, *args, **options):
        mode = options['mode']
        if mode == 'reset':
            pass
        if mode == 'all':
            ESIndexPOI().main()
            ESIndexProvinsi().main()
            ESIndexKabupaten().main()
            ESIndexKecamatan().main()
            ESIndexKelurahan().main()
        if mode == 'kel':
            ESIndexKelurahan().main()
        if mode == 'kec':
            ESIndexKecamatan().main()
        if mode == 'kab':
            ESIndexKabupaten().main()
        if mode == 'prov':
            ESIndexProvinsi().main()
        if mode == 'poi':
            ESIndexPOI().main()