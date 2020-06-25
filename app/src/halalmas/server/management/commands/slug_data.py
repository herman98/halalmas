import logging

from django.utils.text import slugify
from django.core.management.base import BaseCommand, CommandError

from tempatdotcom.server.objects.tags.models import ( Tag, TagGroup)
from tempatdotcom.server.objects.buildings.models import ( Building )
from tempatdotcom.server.objects.facilities.models import ( Facility )


class SlugifyFieldGenerator(object):
    def __init__(self, mod_select=None):
        self.mod_select = mod_select if mod_select else 'all'	

    def tag(self):
        tag_obj = Tag.objects.filter(delstatus=False)
        if tag_obj.count() >= 1:
            for idx, item in enumerate(tag_obj):
                item.slug_id = slugify(item.tag) if item.tag else ''
                item.slug_en = slugify(item.tag_en) if item.tag_en else ''
                item.save()
                print(f'#{idx} {item.tag}')
        else:
            print(f'-no data found-')


    def group_tag(self):
        data_obj = TagGroup.objects.filter(delstatus=False)
        if data_obj.count() >= 1:
            for idx, item in enumerate(data_obj):
                item.slug = slugify(item.name) if item.name else ''
                item.save()
                print(f'#{idx} {item.name}')
        else:
            print(f'-no data found-')

    def building(self):
        data_obj = Building.objects.filter(delstatus=False)
        if data_obj.count() >= 1:
            for idx, item in enumerate(data_obj):
                item.slug = slugify(item.name) if item.name else ''
                item.save()
                print(f'#{idx} {item.name}')
        else:
            print(f'-no data found-')
    
    def facility(self):
        data_obj = Facility.objects.filter(delstatus=False)
        if data_obj.count() >= 1:
            for idx, item in enumerate(data_obj):
                item.slug = slugify(item.name) if item.name else ''
                item.save()
                print(f'#{idx} {item.name}')
        else:
            print(f'-no data found-')

    def convert(self):
        if self.mod_select == 'all':
            self.tag()
            self.group_tag()
            self.building()
            self.facility()
        elif self.mod_select == 'tag':
            self.tag()
        elif self.mod_select == 'group_tag':
            self.group_tag()
        elif self.mod_select == 'building':
            self.building()
        elif self.mod_select == 'facility':
            self.facility()
        else:
            print(f'mod_select {self.mod_select} not supported yet')
        

class Command(BaseCommand):
    help = 'slugify region province, city, kecamatan and kelurahan'

    def add_arguments(self, parser):
        # parser.add_argument('to', nargs='+', type=str,
        #                     help='tech@tempat.com', )
        parser.add_argument('-m', '--mod', type=str,
                            help='all, tag, group_tag, building, facility', )

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
