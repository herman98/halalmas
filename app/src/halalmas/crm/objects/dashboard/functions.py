from __future__ import unicode_literals

from django.urls import reverse

# from halalmas.server.hosts.happy_hour.models import (
#     BranchSaleProduct,
#     BranchHappyHourSlotHeader,
# )
# from halalmas.server.hosts.branches.models import (
#     Branch,
# )
# from halalmas.server.members.profiles.models import (
#     CustomerUserProfile,
# )
# from halalmas.server.hosts.profile.models import (
#     HostUserProfile,
# )
from halalmas.server.objects.buildings.models import Building
# from halalmas.server.orders.happy_hour.models import OrderHappyHourGroup

from .constants import TMPUserRoles
from .models import CRMSetting


def set_roles_url(role_name):
    ret_url = "dashboard:guests"
    if role_name == TMPUserRoles.ADMIN:
        ret_url = "dashboard:admin"
    elif role_name == TMPUserRoles.CRA_TEAM:
        ret_url = "dashboard:cra_team"
    elif role_name == TMPUserRoles.HOST_TEAM:
        ret_url = "dashboard:host_team"
    elif role_name == TMPUserRoles.FINANCE:
        ret_url = "dashboard:finance"
    elif role_name == TMPUserRoles.MARKETING:
        ret_url = "dashboard:marketing"
    else:
        ret_url = "dashboard:guests"

    return reverse(ret_url)  # , kwargs={'app_label': 'auth'})


def user_roles_data(request):
    ret_group_list = []
    user = request.user
    if user.is_authenticated:
        groups = request.user.groups.values_list('name', flat=True)
        for role in groups:
            ret_group_list.append(
                {
                    'role': role,
                    'url': set_roles_url(role)
                })
    return ret_group_list


def create_or_update_role(user_instance, role_name):
    objselect, created = CRMSetting.objects.get_or_create(user=user_instance)
    objselect.role_select = role_name
    objselect.save()


def get_selected_role(user_instance):
    try:
        objselect = CRMSetting.objects.get(user=user_instance)
        return objselect.role_select
    except CRMSetting.DoesNotExist:
        return 'no-role-selected'


def create_or_update_defaultrole(user_instance, role_name):
    objselect, created = CRMSetting.objects.get_or_create(user=user_instance)
    objselect.role_default = role_name
    objselect.save()


def get_selected_defaultrole(user_instance):
    try:
        objselect = CRMSetting.objects.get(user=user_instance)
        return objselect.role_default
    except CRMSetting.DoesNotExist:
        return None


def admin_dashboard_data():
    payload = {}
    # payload['merchant_cnt'] = Branch.objects.filter(delstatus=False).count()
    payload['bulding_cnt'] = Building.objects.filter(delstatus=False).count()
    # payload['host_cnt'] = HostUserProfile.objects.filter(
    #     delstatus=False).count()
    # payload['customer_cnt'] = CustomerUserProfile.objects.filter(
    #     delstatus=False).count()
    # payload['merchant_w_happy_hour'] = Branch.objects.filter(
    #     delstatus=False, is_happy_hour=True).order_by('-cdate')[:20]
    # payload['hh_order_pending'] = OrderHappyHourGroup.objects.filter(
    #     delstatus=False, order_status=OrderHappyHourGroup.OrderStatus.PENDING).count()
    # payload['hh_order_active'] = OrderHappyHourGroup.objects.filter(
    #     delstatus=False, order_status=OrderHappyHourGroup.OrderStatus.ACTIVE).count()
    # payload['hh_order_complete'] = OrderHappyHourGroup.objects.filter(
    #     delstatus=False, order_status=OrderHappyHourGroup.OrderStatus.COMPLETE).count()
    # payload['hh_order_canceled'] = OrderHappyHourGroup.objects.filter(
    #     delstatus=False, order_status=OrderHappyHourGroup.OrderStatus.CANCELED).count()
    # payload['hh_order_expired'] = OrderHappyHourGroup.objects.filter(
    #     delstatus=False, order_status=OrderHappyHourGroup.OrderStatus.EXPIRED).count()

    return payload
