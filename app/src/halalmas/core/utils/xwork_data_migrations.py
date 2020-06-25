import logging
# import random
from datetime import datetime

from django.conf import settings
from django.utils.text import slugify
from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Point
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import User, Group

from xwork.models import (Rooms, CmsUsers, Roles, UserRoles,
                          Brands, CmsUserRooms)

from halalmas.server.hosts.brands.models import Brand as tmp_Brand
from halalmas.server.hosts.branches.models import Branch
from halalmas.server.hosts.spaces.models import Spaces
from halalmas.server.hosts.profile.models import HostUserProfile, HostUser, HostUserRole

from halalmas.server.objects.companies.models import Company
from halalmas.server.objects.buildings.models import Building

from .host_fuctions import HostFuncTools


class HostDataMigrations(object):
    def __init__(self, mode, selection):
        self.mode = mode
        self.selection = selection

    def run(self):
        print("selection {}".format(self.selection))
        if self.selection == 'rooms':
            self.migrate_spaces()
        elif self.selection == 'cms_users':
            self.migrate_cms_users()
        elif self.selection == 'brands':
            self.migrate_brands()
        else:
            pass

    def migrate_brands(self):
        print("START migrating Brands")
        cnt_brands = Brands.objects.all().count()
        cnt_tmpt_brand = tmp_Brand.objects.all().count()
        if cnt_brands > cnt_tmpt_brand:
            # import all roles
            xwork_brands = Brands.objects.all().order_by('pk')
            for idx, item_data in enumerate(xwork_brands):
                print("#{} roles id:{} name:{}".format(
                    idx,
                    item_data.pk, item_data.brand_name))
                # Point(longitude, latitude)
                obj_save = tmp_Brand(
                    slug=slugify(item_data.brand_name),
                    brand_name=item_data.brand_name,
                    description_id=item_data.description,
                    logo=item_data.logo,
                    xwork_pk=item_data.pk
                )
                obj_save.save()
                print("DONE migrating Brands")
        else:
            print("Brands has been Migrated")

    def migrate_host_user_roles(self):
        print("START migrating Host User Roles")
        cnt_roles = Roles.objects.all().count()
        cnt_host_roles = HostUserRole.objects.all().count()
        if cnt_roles > cnt_host_roles:
            # import all roles
            xwork_user_roles = Roles.objects.all().order_by('pk')
            for idx, item_data in enumerate(xwork_user_roles):
                print("#{} roles id:{} name:{}".format(
                    idx,
                    item_data.pk, item_data.name))
                # Point(longitude, latitude)
                obj_save = HostUserRole(
                    role_name=item_data.name
                )
                obj_save.save()
        print("DONE migrate Host User Roles")

    def migrate_cms_users(self):
        print("START migrating CMS Users to Host Profile")
        if self.mode > 0:
            pass
        else:
            # migrate user roles
            self.migrate_host_user_roles()

            xwork_cms_user = CmsUsers.objects.all().order_by('pk')
            for idx, item_data in enumerate(xwork_cms_user):
                print("#{} roles id:{} name:{}".format(
                    idx,
                    item_data.pk, item_data.username))

                # create branch from company name cms users
                # create user
                obj_profile_save = None
                host_profile_status = False
                django_user, user_pre_pwd = HostFuncTools().create_django_user(item_data.username)
                if user_pre_pwd == "HAS-BEEN-SET":
                    print("user {} has been added".format(item_data.username))
                    obj_profile_save = HostUserProfile.objects.filter(
                        user=django_user)
                    if obj_profile_save.count() >= 1:
                        obj_profile_save = obj_profile_save[0]
                        host_profile_status = True

                if host_profile_status is False:
                    obj_profile_save = HostUserProfile(
                        user=django_user,
                        salt=item_data.salt,
                        first_name=item_data.name,
                        phone="{} {}".format(item_data.phone_number_1 if item_data.phone_number_1 else item_data.phone_number_1,
                                             ", {}".format(item_data.phone_number_2) if item_data.phone_number_2 else ''),
                        pre_generate_passwd=user_pre_pwd,)
                    obj_profile_save.save()

                # insert company as branch
                obj_branch = Branch.objects.filter(
                    branch_name=item_data.company_name)
                if obj_branch.count() >= 1:
                    obj_branch = obj_branch[0]
                else:
                    if item_data.company_name:
                        obj_branch = Branch(
                            branch_name=item_data.company_name)
                        obj_branch.save()
                    else:
                        obj_branch_1 = Branch.objects.filter(
                            branch_name='-no-branch-')
                        if obj_branch_1.count() >= 1:
                            obj_branch = obj_branch_1[0]
                        else:
                            obj_branch = Branch(
                                branch_name='-no-branch-')
                            obj_branch.save()

                # insert branch users
                xwork_user_roles = UserRoles.objects.filter(user=item_data)
                if xwork_user_roles.count() >= 1:
                    for user_role_item in xwork_user_roles:
                        host_user_role = HostUserRole.objects.filter(
                            role_name=user_role_item.role.name)
                        if host_user_role.count() >= 1 and obj_profile_save:
                            host_user_role_obj = host_user_role[0]
                            host_user_obj = HostUser(profile=obj_profile_save,
                                                     branch=obj_branch)
                            host_user_obj.save()

                            # add role on profile
                            obj_profile_save.role.add(host_user_role_obj)
                            obj_profile_save.save()
        print("DONE migrating CMS Users to Host Profile")

    def migrate_spaces(self):
        if self.mode > 0:
            # means with limit
            print("mode with limit {} seletected.".format(self.mode))
        else:
            # means all records
            print("START migrating Rooms")
            cnt_rooms = Rooms.objects.filter(deleted_at__isnull=True).count()
            print("Count rooms {}".format(cnt_rooms))
            if cnt_rooms == 0:
                print("No Rooms Data, data count {}".format(cnt_rooms))
                return -1

            xwork_room_data = Rooms.objects.filter(deleted_at__isnull=True)
            for idx, item_data in enumerate(xwork_room_data):
                print("#{} rooms id:{} name:{}".format(idx,
                                                       item_data.pk, item_data.name))
                # get branch obj
                cms_user_obj = CmsUserRooms.objects.filter(room=item_data)
                branch_obj = None
                _company_name = None
                if cms_user_obj.count() >= 1:
                    for here_item in cms_user_obj:
                        if here_item.cms_user.company_name is not None:
                            _company_name = here_item.cms_user.company_name
                            branch_obj = Branch.objects.filter(
                                branch_name=_company_name)
                            if branch_obj.count() >= 1:
                                branch_obj = branch_obj[0]
                # save space object
                if branch_obj:
                    obj_save = Spaces(
                        branch=branch_obj,
                        xwork_pk=item_data.pk,
                        space_name=item_data.name,
                        slug=slugify(item_data.name),
                        max_capacity=item_data.capacity,
                        description_id=item_data.description,
                        room_access_id=item_data.room_access,
                        room_size=item_data.room_size,
                        regulation=item_data.regulation,
                        is_hourly=item_data.is_hourly,
                        is_daily=item_data.is_daily,
                        is_monthly=item_data.is_monthly,
                        is_verified=item_data.is_verified,
                        is_food_allowed=item_data.is_food_allowed,
                        ratings=item_data.ratings,
                        total_score=item_data.total_score,
                        is_published=item_data.is_published,
                    )
                    obj_save.save()

                    # check building
                    if branch_obj.building is None:
                        # get building id
                        building_obj = Building.objects.filter(
                            xwork_pk=item_data.id_building.pk)
                        if building_obj.count() >= 1:
                            building_obj = building_obj[0]
                            # update building id in branch
                            branch_obj.building = building_obj
                            branch_obj.save()
                else:
                    print("Branch {} not found".format(_company_name))
            print("DONE migrating Rooms to Spaces")
