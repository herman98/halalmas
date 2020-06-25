import moment
import json
import logging
import datetime
import pandas as pd

from datetime import date, timedelta
from dateutil.relativedelta import *

from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from halalmas.core.ajax import ajax_response, ajax_response_dump
from .functions import (user_roles_data, create_or_update_role,
                        get_selected_defaultrole, get_selected_role)

from halalmas.crm import (tmptlogin_required,
                              tmptlogin_required_group,
                              tmptlogin_required_multigroup)

from .constants import TMPUserRoles
from .forms import DefaultRoleForm
from .models import CRMSetting
from .functions import admin_dashboard_data

logger = logging.getLogger(__name__)

PROJECT_URL = getattr(settings, 'PROJECT_URL')


def index(request):
    # print "Dashboard PAGE"
    user = request.user
    # print(dir(user))
    print(user)
    print("user.is_authenticated: {}".format(user.is_authenticated))
    if user.is_authenticated:
        # print "USER IS AUTHENTICATE : ", request.user
        default_role = get_selected_defaultrole(request.user)
        print("default_role: {}".format(default_role))

        if(default_role):
            return select_active_role(request, default_role)
        else:
            groups = request.user.groups.all()
            # print "groups: ", groups
            for group in groups:
                return select_active_role(request, group.name)

        # if there is no groups/roles for this user
        return no_dashboard_view(request)

    # render to home page
    return render(request, 'main/welcome.html')


def select_active_role(request, role_selected):
    if TMPUserRoles.ADMIN in role_selected:
        return dashboard_admin(request)
    elif TMPUserRoles.CRA_TEAM in role_selected:
        return dashboard_cra_team(request)
    elif TMPUserRoles.HOST_TEAM in role_selected:
        return dashboard_host_team(request)
    elif TMPUserRoles.FINANCE in role_selected:
        return dashboard_finance(request)
    elif TMPUserRoles.MARKETING in role_selected:
        return dashboard_marketing(request)
    else:
        return dashboard_guests(request)


def no_dashboard_view(request):
    return render(request, 'error/no_dashboard.html')


@tmptlogin_required
@tmptlogin_required_group('admin')
def dashboard_admin(request):
    role_name = TMPUserRoles.ADMIN
    create_or_update_role(request.user, role_name)
    # print "ADMIN PAGE"
    return render(request,
                  'object/dashboard/admin.html',
                  {
                      'PROJECT_URL': PROJECT_URL,
                      'data': admin_dashboard_data(),
                  }
                  )


def range_month(date_1, date_2):
    # dt_now = datetime.datetime.now()
    # date_1 = dt_now+relativedelta(months=-11)
    # date_2 = dt_now

    month_list = [[i.strftime("%b"), int(i.strftime("%m")), int(i.strftime("%Y"))]
                  for i in pd.date_range(start=date_1, end=date_2, freq='MS')]
    return month_list


@tmptlogin_required
@tmptlogin_required_group('cra_team')
def dashboard_cra_team(request):
    role_name = TMPUserRoles.CRA_TEAM
    create_or_update_role(request.user, role_name)
    print("CRA_TEAM PAGE")
    # print('dashboard_cra_team: {}'.format(role_name))
    dt_now = datetime.datetime.now()
    dt_now_min_12 = dt_now+relativedelta(months=-12)
    year_now = dt_now.year

    return render(request, 'object/dashboard/cra_team.html',
                  {
                      'PROJECT_URL': PROJECT_URL,

                  }
                  )


@tmptlogin_required
@tmptlogin_required_group('host_team')
def dashboard_host_team(request):
    role_name = TMPUserRoles.HOST_TEAM
    create_or_update_role(request.user, role_name)
    print("HOST_TEAM PAGE")
    print('dashboard_host_team: {}'.format(role_name))
    return render(request, 'object/dashboard/host_team.html',
                  {
                      'PROJECT_URL': PROJECT_URL,
                      'data': admin_dashboard_data(),
                  }
                  )


@tmptlogin_required
@tmptlogin_required_group('finance')
def dashboard_finance(request):
    role_name = TMPUserRoles.FINANCE
    create_or_update_role(request.user, role_name)
    print("FINANCE PAGE")
    print('dashboard_finance: {}'.format(role_name))
    context = {
        'PROJECT_URL': PROJECT_URL,
    }

    return render(
        request,
        'object/dashboard/finance.html',
        context
    )


@tmptlogin_required
@tmptlogin_required_group('marketing')
def dashboard_marketing(request):
    role_name = TMPUserRoles.MARKETING
    create_or_update_role(request.user, role_name)
    print("MARKETING PAGE")
    print('dashboard_marketing: {}'.format(role_name))

    return render(request, 'object/dashboard/marketing.html',
                  {
                      'PROJECT_URL': PROJECT_URL,
                  }
                  )


def dashboard_guests(request):
    role_name = TMPUserRoles.GUESTS
    create_or_update_role(request.user, role_name)
    print("GUESTS PAGE")
    print('dashboard_guests: {}'.format(role_name))
    return render(request, 'object/dashboard/guests.html',
                  {
                      'PROJECT_URL': PROJECT_URL,
                  }
                  )


@tmptlogin_required
def update_default_role(request):
    # #print "update_default_role Inside"
    try:
        obj_default_role = CRMSetting.objects.get(user=request.user)
    except CRMSetting.DoesNotExists:
        obj_default_role = CRMSetting(user=request.user)

    if request.method == 'POST':
        form = DefaultRoleForm(request.user, request.POST)
        if form.is_valid():
            # #print form.cleaned_data['role_default']
            current_role = form.cleaned_data['role_default']
            form.save()

            return render(request,
                          'object/dashboard/create_defaultrole.html',
                          {'form': form, 'current_role': current_role, 'msg_title': 'Sukses '})
    else:
        form = DefaultRoleForm(request.user)

    return render(request,
                  'object/dashboard/create_defaultrole.html',
                  {'form': form, 'current_role': obj_default_role.role_default, 'msg_title': 'Konfirmasi '})


# -----------------------------   AJAX   START  -----------------------------------------


# @csrf_protect
# def oustanding_bill(request):
#     """
#     """
#     print("f(x): oustanding_bill was HERE")

#     if request.method == 'GET':
#         # print("f(x): oustanding_bill :: GET {}", dir(request))
#         logger.info({
#             'status': 'ajax - oustanding_bill order_no',
#         })

#         current_user = request.user
#         response_data = {}
#         if(current_user):
#             try:
#                 logger.info({
#                     'status': 'ajax - oustanding_bill {} success',
#                 })
#                 response_data['result'] = 'successful!'
#                 response_data['output'] = WithdrawRequests.objects.sum_outstanding()
#                 response_data['reason'] = "ALL OKE"
#                 return ajax_response_dump(response_data)
#             except Exception as e:
#                 logger.warning({
#                     'status': 'ajax - oustanding_bill',
#                     'exception': e,
#                 })
#                 return ajax_response("exception on oustanding_bill, please contact Tech Team...",
#                                      "nok")

#     return ajax_response("this isn't happening")

# -----------------------------   AJAX   END  -----------------------------------------
