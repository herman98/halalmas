from django.core.management.base import BaseCommand, CommandError
from halalmas.api.celery.task_test_service import ganang_ganteng

class Command(BaseCommand):
    def handle(self, *args, **options):
        hehe = ganang_ganteng.delay(10000, 8098098)

        print(hehe)