# from __future__ import absolute_import, unicode_literals

# from django.db import transaction  # SomeError,

# from celery import shared_task
# from celery import task
# from celery.schedules import crontab
# from celery.task import periodic_task
# from celery.utils.log import get_task_logger

# from tempatdotcom.core.utils.currency_scraper import CurrencyScrappingFromBI
# from .currencies.models import Currency

# logger = get_task_logger(__name__)

# URL_BI_CURRENCY_PAGE = 'https://www.bi.go.id/en/moneter/informasi-kurs/transaksi-bi/Default.aspx'
# CSV_PATH_TO_SAVE = '/Users/sky/xwork/xwork-django-gis/app/src'


# @shared_task
# def add_here_1(x, y):
#     return x + y


# def str_to_float(str_in):
#     return float(str_in) if str_in else 0


# def clean_val_price(price_in):
#     return str_to_float(str(price_in).strip().replace(",", ""))


# # @periodic_task(name='currency-periodic-update',
# #                run_every=crontab(minute=0, hour='6,18'), # run it at 6 AM and 6 PM (1800)
# #                #    run_every=crontab(minute='*/5'),
# #                #    queue='automation-ai-01', options={'queue': 'automation-ai-01'}
# #                )
# @shared_task
# def currency_periodic_update():
#     logger.info('currency_periodic_update')

#     clsScrapping = CurrencyScrappingFromBI(URL_BI_CURRENCY_PAGE)
#     currency_data = clsScrapping.get_currency_list()
#     logger.info("currency_data: {}".format(currency_data))

#     if currency_data:
#         # ret_output = clsScrapping.parse_to_csv(currency_data,
#         #                                        CSV_PATH_TO_SAVE)
#         for currency_item in currency_data:
#             # {'code': 'AUD', 'value': '1.00', 'sale': '10,091.22', 'buy': '9,988.72'}
#             # curr_name, curr_value , rate_sale, rate_buy
#             obj, created = Currency.objects.update_or_create(
#                 curr_name=str(
#                     currency_item['code']).strip(),
#                 defaults={'curr_value': clean_val_price(currency_item['value']),
#                           'rate_sale': clean_val_price(currency_item['sale']),
#                           'rate_buy': clean_val_price(currency_item['buy'])},
#             )
#             logger.info("data: {}".format(currency_item))
#             logger.info("CR OR UPD: {}-{}".format(obj, created))
#     return True

#     # """
#     # Goes through every unpaid payment for loan active and by comparing its due date and
#     # today's date, apply late fee as the rule
#     # """
#     # unpaid_payments = Payment.objects.not_paid_active()

#     # for unpaid_payment in unpaid_payments:
#     #     product_line_code = unpaid_payment.loan.application.product_line.product_line_code
#     #     with transaction.atomic():
#     #         update_late_fee_amount(unpaid_payment, product_line_code)
