from django.core.management.base import BaseCommand, CommandError
from tempatdotcom.api.service.elasticsearch.es_index.workspace import ESIndexWorkspace
from tempatdotcom.server.hosts.branches.models import Branch, BranchActivity

class Command(BaseCommand):
	help = 'Create or update workspace for elasticsearch'

	def add_arguments(self, parser):
		parser.add_argument('-m', '--mode', 
		type=str, help='input mode: -m=')

	def handle(self, *args, **options):
		es = ESIndexWorkspace()
		try:
			es.main()
		except Exception as e:
			print(f'Error: {e}')

		return None