import logging
# import random
from datetime import datetime

from django.conf import settings
from django.utils.text import slugify
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import User, Group


class HostFuncTools(object):
    def __init__(self):
        self.default_passwd = "!!tempatdotcom12354!!"

    def create_random_password(self):
        # pwd_suffix = '%x' % random.getrandbits(16*2)
        pwd_suffix = BaseUserManager().make_random_password(10)
        return "{}-{}".format(self.default_passwd, pwd_suffix)

    def create_django_user(self, username_here, group_here=None):
        # set group as 'client_as_host'
        print("CREATE django user")
        # check username
        user_obj = User.objects.filter(username=username_here)
        if user_obj.count() >= 1:
            user_obj = user_obj[0]
            random_passwd = "HAS-BEEN-SET"
        else:
            random_passwd = self.create_random_password()

            user_obj = User()
            user_obj.username = username_here
            user_obj.email = username_here
            user_obj.set_password(random_passwd)
            user_obj.is_staff = True
            user_obj.is_active = True
            user_obj.save()

            # groups
            if group_here is None:
                group_here = 'client_as_host'

            group = Group.objects.filter(name=group_here)
            if group.count() >= 1:
                user_obj.groups.add(group[0])
                user_obj.save()
            else:
                obj_group = Group(name=group_here)
                obj_group.save()
                user_obj.groups.add(obj_group)
                user_obj.save()

        print("CREATE django user DONE {}".format(user_obj))
        return user_obj, random_passwd


def url_img_changer(url_s3_image, prefix=None):
    # prefix = 'img/sm_'
    _logo = url_s3_image
    if prefix is None:
        prefix = ''
    # print(f"_logo: {_logo}")
    filename_here = _logo.split('/')[-1]
    base_url = _logo.replace(filename_here,'')
    if filename_here:
        filename_here = filename_here.split("?")[0]
    new_url = "{}{}{}".format(base_url, prefix, filename_here)
    # print(f"new_url: {new_url}")
    return new_url