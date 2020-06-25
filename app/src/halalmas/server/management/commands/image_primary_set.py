from django.core.management.base import BaseCommand, CommandError
from halalmas.server.hosts.branches.models import BranchImages

class Command(BaseCommand):
	help = 'Set Primary Images Branch'

	def handle(self, *args, **options):
		minimum = 10
		images = BranchImages.objects.filter(
			# id=26,
			# sequence__lt=minimum,
			sequence__gte=minimum,
			delstatus=False)
		
		print('TOTAL BRANCH IMAGES ==> ', images.count())

		images.update(
			primary_photo=False,
			# primary_photo=True
		)