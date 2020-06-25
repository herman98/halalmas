from django.core.management.base import BaseCommand, CommandError
from halalmas.api.service.elasticsearch.es_orm.update_or_create_branch import UpdateOrCreateBranch

class Command(BaseCommand):
	help = 'Create or updatte branches for elasticsearch'

	def add_arguments(self, parser):
		parser.add_argument('-m', '--mode', 
		type=str, help='input mode: -m=')

	def handle(self, *args, **options):
		ES = UpdateOrCreateBranch()

		ES.update_or_create([38763], msg='index from django command')
		# ES.update_or_create([52625])

		# ES.update_or_create([39125, 22927, 5974]) #Hotel Rega Test 

		return None