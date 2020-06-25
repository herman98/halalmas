import logging

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from tempatdotcom.api.service.email.send_mail_controller import MailController

from tempatdotcom.server.orders.day_use.models import OrderDayUse
from tempatdotcom.server.orders.happy_hour.models import OrderHappyHourGroup, OrderHappyHour

class Command(BaseCommand):
	def handle(self, *args, **options):
		# day use ======================
		# order_detail = OrderDayUse.objects.filter(order_no='TDU-20191028-1')
		# order = order_detail.first().order_group
		# branch = order_detail.first().space_product.space_grp_activity.space.branch
		# user :Dict= order.user_profile
		# =============================== 


		# happy hour ====================
		order_detail = OrderHappyHour.objects.filter(order_no='THH-20191008-21')
		order = order_detail.first().order_group
		branch = order_detail.first().hh_product.branch
		user :Dict= order.user_profile
		# ===============================	 


		# a = MailController.send_booking_confirmation_day_use_for_merchant(
		# 	branch=branch,
		# 	user=user,
		# 	order=order,
		# 	order_detail=order_detail.first(),
		# )

		a = MailController.send_booking_confirmation_happy_hour_for_merchant(
			branch=branch,
			user=user,
			order=order,
			order_detail=order_detail,
		)

		# a = MailController.send_payment_bill_day_use(
		# 	branch=branch,
		# 	user=user,
		# 	order=order,
		# 	order_detail=order_detail,
		# )
		
		# a = MailController.send_thanks_rnr(52583, 'Ganang', 'gananggww@gmail.com')

		print("hehehehe", a)