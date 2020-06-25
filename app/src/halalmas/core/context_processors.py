# coding=utf-8
# from os.path import abspath, dirname, join
# from re import match, search
import datetime
import calendar

from django.conf import settings
from .functions import display_name
from tempatdotcom.crm.objects.dashboard.functions \
    import user_roles_data, get_selected_role
# from tempatdotcom.xwork.functions import \
#     raw_building_no_region, get_count_data
# from tempatdotcom.crm.object.inquiry.functions import count_booking_duration, cra_pic_nav
# from tempatdotcom.xwork.models import WithdrawRequests, Orders

from django.db.models import Q


DATABASE_DEFAULT = getattr(settings, 'DATABASE_DEFAULT', 'default')
PROJECT_URL = getattr(settings, 'PROJECT_URL', 'http://localhost:8000')
# DATABASES = getattr(settings, 'DATABASES', {})
INSTALLED_APPS = getattr(settings, 'INSTALLED_APPS', tuple())
TEMPATDOTCOM_URL = getattr(settings, 'XWORK_URL', 'https://tempat.com')


def tempatdotcom(request):
    if request.user.is_authenticated:
        tempatdotcom_current_role = get_selected_role(request.user)
    else:
        tempatdotcom_current_role = request.user

    no_logo = u'<img src="/static/images/profile/no-logo-1.png" alt="company-logo" width="36" class="img-circle"/>'
    ret_dict_out = {'PROJECT_URL': PROJECT_URL,
                    'tempatdotcom_roles': user_roles_data(request),
                    'tempatdotcom_current_role':  tempatdotcom_current_role,
                    'nav_profile_logo': no_logo,
                    'tempatdotcom_URL': TEMPATDOTCOM_URL,
                    }
    return ret_dict_out


def app(request):
    return {'INSTALLED_APPS': INSTALLED_APPS}


def today():
    date_now = datetime.datetime.now().date()
    start_date = '{} 00:00'.format(date_now)
    end_date = '{} 23:59'.format(date_now)
    # return Orders.objects.filter(order_status='PENDING', updated_at__range=[start_date, end_date]).exclude(payment__btproof_image=None).count()


def week():
    date_now = datetime.datetime.now().date()
    dt = datetime.datetime.strptime(str(date_now), '%Y-%m-%d')
    start = dt - datetime.timedelta(days=dt.weekday())
    end = start + datetime.timedelta(days=6)

    start_date = '{} 00:00'.format(start.strftime('%Y-%m-%d'))
    end_date = '{} 23:59'.format(end.strftime('%Y-%m-%d'))
    # return Orders.objects.filter(order_status='PENDING', updated_at__range=[start_date, end_date]).exclude(payment__btproof_image=None).count()


def month():
    month = datetime.datetime.now().month
    year = datetime.datetime.now().year
    last_date = calendar.monthrange(year, month)[1]

    start_date = '{}-{}-01 00:00'.format(year, month)
    end_date = '{}-{}-{} 23:59'.format(year, month, last_date)
    # return Orders.objects.filter(order_status='PENDING', updated_at__range=[start_date, end_date]).exclude(payment__btproof_image=None).count()


# def crm_dashboard(request):
#     data_building_no_region = raw_building_no_region()
#     count_building_no_region = len(list(data_building_no_region))
#     count_data = get_count_data()
#     return {
#         'HELLO': 'Hello Xwork CRM',
#         'data_building_no_region': data_building_no_region,
#         'count_building_no_region': count_building_no_region,

#         'bulding_cnt': count_data['bulding_cnt'],
#         'room_cnt': count_data['room_cnt'],
#         'appuser_cnt': count_data['appuser_cnt'],
#         'count_duration': count_booking_duration(),
#         'cra_pic_nav': cra_pic_nav(),

#         'invoice': {
#             'waiting': WithdrawRequests.objects.total_waiting(),
#             'paid': WithdrawRequests.objects.total_paid(),
#         },
#         'orders': {
#             'today': today(),
#             'week': week(),
#             'month': month(),
#         }
#         # .count(),

#     }
