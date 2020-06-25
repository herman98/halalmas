from django.core.management.base import BaseCommand, CommandError
from halalmas.api.service.elasticsearch.es_index.seo_true import SEO
from halalmas.server.hosts.branches.models import (
	Branch)

class Command(BaseCommand):
	help = 'Create or update SEO ES'

	def add_arguments(self, parser):
		parser.add_argument('-m', '--mode', 
		type=str, help='input mode: -m=')

	def handle(self, *args, **options):
		print('STARTING INDEXING SEO')
		branches = Branch.objects.filter(
			delstatus = False,
			is_published = True,
			# id__in=[38763, 66, 52669, 52671] 
		)

		i = branches.count()
		for branch in branches:
			print(f'update SEO : branch = {branch.id} - {branch.branch_name}')
			seo = SEO()
			seo.branch_id = branch.id
			try:
				seo.create_or_update_seo()
			except Exception as e:
				continue
			i -= 1
			print(f'sabar ya tinggal {i} branch lagi')
