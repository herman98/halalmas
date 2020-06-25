from django.core.management.base import BaseCommand, CommandError
# from tempatdotcom.api.service.compressor.image import ImageCompressor
from tempatdotcom.core.utils.branch_img_compress import compress_s3_image_from_url

class Command(BaseCommand):
	def handle(self, *args, **options):
		static_url = 'https://tempatdotcom.s3-ap-southeast-1.amazonaws.com/server/media/branch/10000/picture-1472399114.jpg'		
		compress_s3_image_from_url(static_url)