from inspect import isfunction

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test


class _cbv_decorate(object):
    def __init__(self, dec):
        self.dec = method_decorator(dec)

    def __call__(self, obj):
        obj.dispatch = self.dec(obj.dispatch)
        return obj


def patch_view_decorator(dec):
    def _conditional(view):
        if isfunction(view):
            return dec(view)

        return _cbv_decorate(dec)(view)

    return _conditional


xwlogin_required = patch_view_decorator(login_required)
xwlogin_required_admin = patch_view_decorator(
    user_passes_test(lambda u: u.groups.filter(name='admin').exists()))


def xwlogin_required_group(group_name):
    return patch_view_decorator(
        user_passes_test(lambda u: u.groups.filter(name=group_name).exists()))


"""
    ex: arr_group = ['group1', 'group2']
"""


def xwlogin_required_multigroup(arr_group):
    return patch_view_decorator(
        user_passes_test(lambda u: u.groups.filter(name__in=arr_group).exists()))


def xwlogin_req_group_class(group_name):
    return patch_view_decorator(
        user_passes_test(lambda u: u.groups.filter(name=group_name).exists()))


def xwlogin_req_group(group_name):
    return user_passes_test(lambda u: u.groups.filter(name=group_name).exists())


def xwlogin_req_multigroup(arr_group):
    return user_passes_test(lambda u: u.groups.filter(name__in=arr_group).exists())


def xwlogin_required_exclude(arr_group):
    return patch_view_decorator(
        user_passes_test(lambda u: u.groups.exclude(name__in=arr_group).exists()))
