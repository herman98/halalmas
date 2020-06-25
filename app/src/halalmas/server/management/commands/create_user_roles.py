import logging

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Creating initial for user roles using django auth group'

    # def add_arguments(self, parser):
    #     parser.add_argument('roles', nargs='+', type=str)

    def handle(self, *args, **options):
        logging.basicConfig(level=logging.DEBUG, format="%(message)s")
        logging.info("-" * 72)
        user_roles = [
            'admin',
            'host_team',
            'cra_team',
            'guests',
            'finance',
            'marketing',
            'client_as_host',
            'customer',
        ]
        for roles in user_roles:
            new_group, created = Group.objects.get_or_create(name=roles)

        logging.info("creating user roles is quitting.")
        print("Creating User Roles Successfully")
