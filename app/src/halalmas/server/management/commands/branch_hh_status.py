import logging

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from halalmas.core.services.happy_hour.branch_hh_status import BranchHappyHourStatus


class Command(BaseCommand):
    help = 'Cron Job command for disable is-happy-hour on branch status from Header Slot'

    # def add_arguments(self, parser):
    #     parser.add_argument('-s', '--status', type=str,
    #                         help='-status options HAPPLYDEALS or DAYUSE', )

    def handle(self, *args, **options):
        # status_change = options['status'] 
        print("Starting command... update is_happy_hour status")
        try:
            BranchHappyHourStatus().happyhour_disable_status()
        except Exception as e:
            print("Failed to change status, err:{}".format(e))                

        logging.info("sukses DONE")
        print("Finished command ...")
