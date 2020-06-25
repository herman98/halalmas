from django.core.management.base import BaseCommand, CommandError
from halalmas.api.service.elasticsearch.es_orm.update_happy import UpdateBranch

class Command(BaseCommand):
    help = 'Update elasticsearch'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        lists = [
            446, 15038, 12142, 14405,
            15843, 15114, 12149, 521,
            15947, 13712, 1274, 5850
        ]

        UpdateBranch.update_happy_hour(
            list_branch_id=lists, 
            is_happy_hour=True
        )
