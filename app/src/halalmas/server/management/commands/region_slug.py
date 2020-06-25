import logging

from django.utils.text import slugify
from django.core.management.base import BaseCommand, CommandError

from halalmas.server.objects.indonesia.models import ( KelurahanBorder,
    KecamatanBorder, ProvinsiBorder, KabupatenBorder)
# from halalmas.server.objects.world.models import WorldBorder


class SlugifyFieldGenerator(object):
    def __init__(self, mod_select=None):
        self.mod_select = mod_select if mod_select else 'all'	

    def kelurahan(self):
        kelurahan_obj = KelurahanBorder.objects.filter(delstatus=False)
        if kelurahan_obj.count() >= 1:
            for idx, item in enumerate(kelurahan_obj):
                item.slug_0 = slugify(item.name_0) if item.name_0 else ''
                item.slug_1 = slugify(item.name_1) if item.name_1 else ''
                item.slug_2 = slugify(item.name_2) if item.name_2 else ''
                item.slug_3 = slugify(item.name_3) if item.name_3 else ''
                item.slug_4 = slugify(item.name_4) if item.name_4 else ''
                item.save()
                print(f'#{idx} {item.name_4}')
        else:
            print(f'-no data found-')


    def kecamatan(self):
        data_obj = KecamatanBorder.objects.filter(delstatus=False)
        if data_obj.count() >= 1:
            for idx, item in enumerate(data_obj):
                item.slug_0 = slugify(item.name_0) if item.name_0 else ''
                item.slug_1 = slugify(item.name_1) if item.name_1 else ''
                item.slug_2 = slugify(item.name_2) if item.name_2 else ''
                item.slug_3 = slugify(item.name_3) if item.name_3 else ''
                item.save()
                print(f'#{idx} {item.name_3}')
        else:
            print(f'-no data found-')

    def city(self):
        data_obj = KabupatenBorder.objects.filter(delstatus=False)
        if data_obj.count() >= 1:
            for idx, item in enumerate(data_obj):
                item.slug_0 = slugify(item.name_0) if item.name_0 else ''
                item.slug_1 = slugify(item.name_1) if item.name_1 else ''
                item.slug_2 = slugify(item.name_2) if item.name_2 else ''
                item.save()
                print(f'#{idx} {item.name_2}')
        else:
            print(f'-no data found-')

    def province(self):
        data_obj = ProvinsiBorder.objects.filter(delstatus=False)
        if data_obj.count() >= 1:
            for idx, item in enumerate(data_obj):
                item.slug_0 = slugify(item.name_0) if item.name_0 else ''
                item.slug_1 = slugify(item.name_1) if item.name_1 else ''
                item.save()
                print(f'#{idx} {item.name_1}')
        else:
            print(f'-no data found-')
    
    def country(self):
        # data_obj = WorldBorder.objects.filter(delstatus=False)
        # if data_obj.count() >= 1:
        #     for idx, item in enumerate(data_obj):
        #         item.slug = slugify(item.name) if item.name else ''
        #         item.save()
        #         print(f'#{idx} {item.name}')
        # else:
        #     print(f'-no data found-')
        return "OK"


    def convert(self):
        if self.mod_select == 'all':
            self.country()
            self.province()
            self.city()
            self.kecamatan()
            self.kelurahan()
        elif self.mod_select == 'kelurahan':
            self.kelurahan()
        elif self.mod_select == 'kecamatan':
            self.kecamatan()
        elif self.mod_select == 'city':
            self.city()
        elif self.mod_select == 'province':
            self.province()
        elif self.mod_select == 'country':
            self.country()
        

class Command(BaseCommand):
    help = 'slugify region province, city, kecamatan and kelurahan'

    def add_arguments(self, parser):
        # parser.add_argument('to', nargs='+', type=str,
        #                     help='tech@tempat.com', )
        parser.add_argument('-m', '--mod', type=str,
                            help='all, country, province, city, kecamatan or kelurahan', )

    def handle(self, *args, **options):
        print("slugify is in progress please wait...")
        module_selected = options['mod'] 
       
        log_str = "Starting command... {}".format(module_selected)
        logging.info(log_str)
        print(log_str)

        #execute to convert
        SlugifyFieldGenerator(module_selected).convert()

        print("End of command... {}".format(module_selected))
        logging.info("Success Slugify Region models {}")
