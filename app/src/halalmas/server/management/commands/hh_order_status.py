import logging

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from halalmas.core.services.happy_hour.hh_order_status import HappyHourOrderStatus


class Command(BaseCommand):
    help = 'Cron Job command for happy-hour orders status from ACTIVE to COMPLETE, or PENDING to EXPIRED'

    def add_arguments(self, parser):
        # parser.add_argument('mode', nargs='+', type=str)
        # parser.add_argument('mode', type=str, help='Indicates the number of users to be created')
        parser.add_argument('-s', '--status', type=str,
                            help='-status options ACTIVE-COMPLETE or PENDING-EXPIRED', )

    def handle(self, *args, **options):
        # mode = options.get('mode')
        status_change = options['status'] 
        print("Starting command... {}".format(status_change))

        if status_change == 'ACTIVE-COMPLETE':
            print(f'ACTIVE-COMPLETE is here')
            try:
                HappyHourOrderStatus().active_to_complete()
            except Exception as e:
                print("Failed to change status, err:{}".format(e))                

        elif status_change == 'PENDING-EXPIRED':
            print(f'PENDING-EXPIRED is here')
            try:
                HappyHourOrderStatus().pending_to_expired()
            except Exception as e:
                print("Failed to change status, err:{}".format(e))
        
        elif status_change == 'ACTIVE-EXPIRED':
            print(f'ACTIVE-EXPIRED is here')
            try:
                HappyHourOrderStatus().active_to_expired()
            except Exception as e:
                print("Failed to change status, err:{}".format(e))

        logging.info("sukses status {}".format(status_change))
        print("Finished command ...")
