from django.core.management.base import BaseCommand, CommandError
from tempatdotcom.api.service.elasticsearch.es_orm.seo import SeoNeeded

class Command(BaseCommand):
	help = 'Get from ellastic for SEO'

	def handle(self, *args, **options):
		print('===========')
		a = SeoNeeded()
		a.kab_slug = 'jakarta-utara'
		a.kec_slug = 'kelapa-gading'
		a.tag_slug = 'tutup'
		a.brand_slug = 'hanako-sushi-bar'
		a.building_slug = 'mall-of-indonesia'
		a.activity_slug = 'tempat-makan'

		print(a.get_list_branch_by_seo())
		
		rs = a.fetch()

		print(rs)
		# return rs
