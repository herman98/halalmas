import csv
import json
import re
import requests
import pprint
# import numpy as np

from datetime import datetime
from time import sleep
from django.utils.text import slugify

from halalmas.core.utils.aws_s3_upload import UploadToS3
from halalmas.scrappers.pergikuliner.models import (
    WebScrapPergiKuliner,
    WebScrapPergiKulinerImage,
    WebScrapPergiKulinerRnR,
    WebScrapPergiKulinerRnRImage)
from halalmas.server.hosts.brands.models import (
    Brand)
from halalmas.server.hosts.branches.models import (
    Branch, BranchTypes,
    BranchFacility,
    BranchImages,
    BranchActivity,
    BranchTags)
from halalmas.server.objects.buildings.models import (
    Building, PublicTransport, BuildingCategory
)
from halalmas.server.features.branch_rnr.models import (
    BranchRatingReviews,
    BranchRatingReviewUserProfiles,
    BranchRatingReviewDetails,
    BranchRatingReviewPhotos
)
from halalmas.server.features.ratings_and_reviews.models import (
    RatingReviewMasters, RatingReviewActivity
)
# from halalmas.server.members.profiles.models import(
#     CustomerUserRole, CustomerUserProfile
# )
from halalmas.server.objects.facilities.models import Facility
from halalmas.server.objects.tags.models import Tag, TagGroup
from halalmas.server.hosts.activities.models import ActivityGroup
from halalmas.server.hosts.operational_hours.models import BranchOperationalHour

from .host_fuctions import HostFuncTools
from .branch_img_compress import BranchImageCompressor

DOMAIN_NAME_TO_SCRAP = 'https://pergikuliner.com'


class PergikulinerParsetoTempat(object):
    def __init__(self):
        self.store_to_db = True
        self.reviews_to_db = True
        self.op_hour_to_db = True

        # this status for update branch only , and set store_to_db to False
        self.branch_save = False

    def string_to_dict(self, str_in):
        dict_out={}
        arr_data = str_in.split(",")
        if arr_data:
            for item in arr_data:
                data_ = item.split(":")
                if len(data_) == 2:
                    dict_out[data_[0].strip().replace('"', '')] = data_[
                        1].strip().replace('"', '')
        return dict_out

    def create_brands(self, brand_name):
        print(f'START create Brands {brand_name}')
        slug_brand = slugify(brand_name)

        obj_brand = None
        if self.store_to_db:
            obj_brands = Brand.objects.filter(slug=slug_brand)
            if obj_brands.count() >= 1:
                obj_brand = obj_brands[0]
            else:
                # Point(longitude, latitude)
                obj_brand = Brand(
                    slug=slug_brand,
                    brand_name=brand_name,
                )
                obj_brand.save()
        return obj_brand
        print('DONE creating Brand')

    def create_building_category(self, cat_name):
        """
            Apartemen	-
            Coffee Shop	-
            Gedung Kampus	-
            Gedung Perkantoran	-
            Hotel	-
            Lapangan Olah Raga	-
            Mall	-
            Restaurant	-
            Ruko/Rukan
        """
        if cat_name.lower().find('apartemen') > -1:
            cat_name_out = 'Apartemen'
        elif cat_name.lower().find('coffe') > -1 or cat_name.lower().find('kopi') > -1:
            cat_name_out = 'Coffee Shop'
        elif cat_name.lower().find('campus') > -1 or cat_name.lower().find('kampus') > -1:
            cat_name_out = 'Gedung Kampus'
        elif cat_name.lower().find('office') > -1 or cat_name.lower().find('kantor') > -1:
            cat_name_out = 'Gedung Perkantoran'
        elif cat_name.lower().find('hotel') > -1:
            cat_name_out = 'Hotel'
        elif cat_name.lower().find('sport') > -1 or cat_name.lower().find('olah raga') > -1:
            cat_name_out = 'Lapangan Olah Raga'
        elif cat_name.lower().find('mall') > -1 or cat_name.lower().find('belanja') > -1:
            cat_name_out = 'Mall'
        elif cat_name.lower().find('restaurant') > -1 or cat_name.lower().find('restauran') > -1:
            cat_name_out = 'Restaurant'
        elif cat_name.lower().find('ruko') > -1 or cat_name.lower().find('rukan') > -1:
            cat_name_out = 'Ruko/Rukan'
        else:
            cat_name_out = "Restaurant" # cat_name.title()

        obj_category = None
        if self.store_to_db:
            obj_category = BuildingCategory.objects.filter(name=cat_name_out)
            if obj_category.count() >= 1:
                obj_category = obj_category[0]
            else:
                obj_category = BuildingCategory(name=cat_name_out)
                obj_category.save()
            print(f'building category: {obj_category}')
        return obj_category

    def create_building(self, obj_pergikuliner):
        print(f'START create Building')

        branch_name = obj_pergikuliner.branch.strip().replace(
            "\n", "").replace("\r", "").replace("]", "").replace(
                "[", " -").replace("  ", "").strip()
        print(f'branch_name: {branch_name}')

        # get address
        address_list = eval(obj_pergikuliner.building)
        # print('address_list: {} with type: {} len: {}'.format(
        #     address_list, type(address_list), len(address_list)))
        if address_list and len(address_list) >= 1:
            building_name = address_list[0]
            if building_name.find("Jl.") > -1 or building_name.find("Jalan") > -1:
                building_name = None
            else:
                building_name = address_list[0].strip()
                if building_name.find(",") > 0:
                    building_name = building_name[:building_name.find(",")]
        address = " ".join(str(x) for x in address_list)
        # print(f'address: {address}')

        # get location
        location = obj_pergikuliner.location.replace(
            '\\xa0', ' ').replace("'", '"')
        # print(f'location: {location}')
        location = json.loads(location)
        print('lat: {} lon: {} infowindow:{}'.format(
            location['lat'], location['lng'], location['infowindow']))
        if building_name is None:
            building_name = branch_name
        print(f'building_name: {building_name}')

        # print(f'info_list_out: {obj_pergikuliner.info_list_out.encode()}')
        # get tipe branch
        pre_dict_list_out = obj_pergikuliner.info_list_out.replace(
            '\\xa0', ' ').replace("'", '"')
        # print(f'pre_dict_list_out: {pre_dict_list_out}')
        try:
            info_data = json.loads(pre_dict_list_out)
        except Exception as e:
            info_data = self.string_to_dict(pre_dict_list_out)
        # print(f'info_data: {info_data}')
        building_access_id = ''
        if 'Stasiun MRT/LRT Terdekat' in info_data:
            building_access_id = "Stasiun MRT/LRT Terdekat: {}".format(
                info_data['Stasiun MRT/LRT Terdekat']
            )
        # print(f'building_access_id: {building_access_id}')
        description_id = ''
        for key_in in info_data:
            description_id = "{}{}:{}, ".format(
                description_id, key_in, info_data[key_in]
            )
        # print(f'description_id: {description_id}')

        facility_id = eval(obj_pergikuliner.arr_facility_checked)
        facility_id = ", ".join(str(x) for x in facility_id)
        # print(f'facility_id: {facility_id}')

        # get building category
        obj_category = self.create_building_category(building_name)
        # TODO: get public_transportation POSTPONE

        building_obj = None
        if self.store_to_db:
            building_obj = Building.objects.filter(name=building_name)
            # check building
            if building_obj.count() >= 1:
                building_obj = building_obj[0]
                building_obj.name = building_name
                building_obj.address = address
                building_obj.latitude = location['lat']
                building_obj.longitude = location['lng']
                building_obj.building_category = obj_category
                building_obj.description_id = description_id
                building_obj.building_access_id = building_access_id
                building_obj.is_facilities_id = facility_id
            else:
                building_obj = Building(
                    name=building_name,
                    address=address,
                    latitude=location['lat'],
                    longitude=location['lng'],
                    # image_url=item_data.picture,
                    building_category=obj_category,
                    description_id=description_id,
                    building_access_id=building_access_id,
                    is_facilities_id=facility_id,
                )
            building_obj.save()
        print('DONE creating Building')
        return building_obj

    def create_branch(self, brand_obj, building_obj, obj_pergikuliner):
        print(f'START create Branch ')  # {obj_pergikuliner.branch.encode()}

        branch_name = obj_pergikuliner.branch.strip().replace(
            "\n", "").replace("\r", "").replace("]", "").replace(
                "[", " -").replace("  ", "").strip()
        print(f'branch_name: {branch_name}')

        # get tipe branch
        pre_dict_list_out = obj_pergikuliner.info_list_out.replace(
            '\\xa0', ' ').replace("'", '"')
        # print(f'pre_dict_list_out: {pre_dict_list_out}')
        try:
            info_data = json.loads(pre_dict_list_out)
        except Exception as e:
            info_data = self.string_to_dict(pre_dict_list_out)
        # print(f'info_data: {info_data}')
        branch_type = ''
        if 'Tipe Kuliner' in info_data:
            branch_type = "Restaurant - {}".format(info_data['Tipe Kuliner'])
        print(f'branch_type: {branch_type}')
        obj_branch_type = BranchTypes.objects.filter(name=branch_type)
        if obj_branch_type.count() >= 1:
            obj_branch_type = obj_branch_type[0]
        else:
            obj_branch_type = BranchTypes(name=branch_type)
            obj_branch_type.save()

        operating_hour = ''
        if 'Jam Buka' in info_data:
            operating_hour = "Jam Buka: {}".format(
                info_data['Jam Buka']
            ).replace("Belum Buka", "").replace("Sudah Tutup", "")
        print(f'operating_hour: {operating_hour}')

        # get pembayaran info
        pembarayan_info = ''
        if 'Pembayaran' in info_data:
            pembarayan_info = "Pembayaran: {}".format(info_data['Pembayaran'])
        print(f'pembarayan_info: {pembarayan_info}')

        # phone
        phone_data = ''
        if obj_pergikuliner.phone_n_open:
            phone_list = eval(obj_pergikuliner.phone_n_open)
            print(f'phone_list: {phone_list}')
            if len(phone_list) >= 3:
                phone_data = phone_list[2]

        # price info
        price_info = obj_pergikuliner.price.strip()

        # facility
        has_facility = False
        if obj_pergikuliner.arr_facility_checked:
            has_facility = True

        # rating
        rating_list = eval(obj_pergikuliner.arr_ratings)
        print(f'rating_list: {rating_list}')
        has_review = False
        rating_score_ = 0
        review_count = 0
        if rating_list:
            has_review = True
            rating_score = rating_list[0]
            print(f'rating_score: {rating_score}')
            rating_score_ = rating_score[0]
            review_count = rating_score[1]
            # rating_detail = rating_list[1]
            # print(f'rating_detail: {rating_detail}')
            review_count = review_count.replace('review', '').strip()

        slug_branch = slugify(branch_name)

        obj_branch = None
        if self.store_to_db or self.branch_save:
            obj_branch = Branch.objects.filter(slug=slug_branch)
            if obj_branch.count() >= 1:
                obj_branch = obj_branch[0]
                obj_branch.branch_name = branch_name
                obj_branch.brand = brand_obj
                obj_branch.building = building_obj
                obj_branch.branch_type = obj_branch_type
                obj_branch.operating_hour = operating_hour
                obj_branch.phone = phone_data
                obj_branch.price_info = price_info
                obj_branch.payment_info = pembarayan_info
                obj_branch.total_reviews = review_count
                obj_branch.rating_score = rating_score_
                obj_branch.has_facility = has_facility
                obj_branch.has_review = has_review
                obj_branch.is_published = True
                obj_branch.source = 'pergikuliner.com'
            else:
                # Point(longitude, latitude)
                obj_branch = Branch(
                    slug=slug_branch,
                    branch_name=branch_name,
                    brand=brand_obj,
                    building=building_obj,
                    branch_type=obj_branch_type,
                    operating_hour=operating_hour,
                    phone=phone_data,
                    price_info=price_info,
                    payment_info=pembarayan_info,
                    total_reviews=review_count,
                    rating_score=rating_score_,
                    has_facility=has_facility,
                    has_review=has_review,
                    is_published=True,
                    source='pergikuliner.com',
                )
            obj_branch.save()
        print('DONE creating Branch')
        return obj_branch

    def create_branch_facility(self, branch_obj, obj_pergikuliner):
        # BranchFacility
        print(f'START create Branch Facility')
        # facility
        facility_check_list = eval(obj_pergikuliner.arr_facility_checked)
        print(f'facility_check_list: {facility_check_list}')
        if facility_check_list:
            for facility_item in facility_check_list:
                print(f'facility_item: {facility_item}')

                if self.store_to_db:
                    facility_obj = Facility.objects.filter(
                        name=facility_item, delstatus=False)
                    if facility_obj.count() >= 1:
                        facility_obj = facility_obj[0]
                    else:
                        facility_obj = Facility(name=facility_item)
                    facility_obj.save()

                    # store to BranchFacility
                    branch_facility_obj = BranchFacility.objects.filter(
                        branch=branch_obj, facility=facility_obj)
                    if branch_facility_obj.count() >= 1:
                        branch_facility_obj = branch_facility_obj[0]
                        branch_facility_obj.is_strike_out = False
                    else:
                        branch_facility_obj = BranchFacility(
                            branch=branch_obj,
                            facility=facility_obj,
                            is_strike_out=False
                        )
                    branch_facility_obj.save()

        facility_uncheck_list = eval(obj_pergikuliner.arr_facility_unchecked)
        print(f'facility_uncheck_list: {facility_uncheck_list}')
        if facility_uncheck_list:
            for facility_item in facility_uncheck_list:
                print(f'facility_item: {facility_item}')

                if self.store_to_db:
                    facility_obj = Facility.objects.filter(
                        name=facility_item, delstatus=False)
                    if facility_obj.count() >= 1:
                        facility_obj = facility_obj[0]
                    else:
                        facility_obj = Facility(name=facility_item)
                    facility_obj.save()

                    # store to BranchFacility
                    branch_facility_obj = BranchFacility.objects.filter(
                        branch=branch_obj, facility=facility_obj)
                    if branch_facility_obj.count() >= 1:
                        branch_facility_obj = branch_facility_obj[0]
                        branch_facility_obj.is_strike_out = True
                    else:
                        branch_facility_obj = BranchFacility(
                            branch=branch_obj,
                            facility=facility_obj,
                            is_strike_out=True
                        )
                    branch_facility_obj.save()
        print(f'END create Facility ')

    def create_branch_image(self, branch_obj, obj_pergikuliner):
        branch_images = WebScrapPergiKulinerImage.objects.filter(
            delstatus=False, done=False,
            web_pergikuliner=obj_pergikuliner)

        if branch_images.count() >= 1:
            cls_aws_S3 = UploadToS3()
            for idx_seq, image_item in enumerate(branch_images):
                print(f'image_item: {image_item.image_url}')

                if self.store_to_db:
                    # store to S3
                    dir_branch_id = "{}{}".format(
                        '/server/media/branch/', branch_obj.pk)
                    url_img_download = image_item.image_url
                    image_url_out = cls_aws_S3.upload_from_url(
                        url_img_download, dir_branch_id)

                    if image_url_out:
                        obj_branch_image = BranchImages.objects.filter(
                            branch=branch_obj,
                            image_url=image_url_out)
                        if obj_branch_image.count() >= 1:
                            obj_branch_image = obj_branch_image[0]
                        else:
                            obj_branch_image = BranchImages(
                                branch=branch_obj,
                                image_url=image_url_out,
                                img_type=image_item.image_category,
                                sequence=idx_seq,
                                img_format=cls_aws_S3.get_file_ext,
                            )
                        obj_branch_image.save()

                    # update done image scrap
                    image_item.done = True
                    image_item.save()

    def parse_pergikuliner(self, count_data=None):
        if self.branch_save:
            done_status = True
        else:
            done_status = False

        if count_data:
            obj_pergikuliner = WebScrapPergiKuliner.objects.filter(
                delstatus=False, done=done_status)[:count_data]
        else:
            obj_pergikuliner = WebScrapPergiKuliner.objects.filter(
                delstatus=False, done=done_status)

        print("obj_pergikuliner count: {}".format(obj_pergikuliner.count()))
        if obj_pergikuliner.count():
            for idx_, item_page in enumerate(obj_pergikuliner):
                print(f'[{idx_}] {item_page.web_url}')

                # add brand
                brand_name = item_page.brand.strip()
                print(f'brand_name {brand_name}')
                obj_brand = self.create_brands(brand_name)

                # add building
                obj_building = self.create_building(item_page)

                # add branch
                obj_branch = self.create_branch(
                    obj_brand, obj_building, item_page)

                # add facility
                self.create_branch_facility(obj_branch, item_page)

                # add branch images
                self.create_branch_image(obj_branch, item_page)

                # save done on web parsing
                if self.store_to_db:
                    item_page.done = True
                    item_page.save()

                # break for root-loop
                # break

    def parse_pergikuliner_reviews(self, count_data=None):
        done_status = False  # , web_pergikuliner=item_page
        if count_data:
            obj_review_list = WebScrapPergiKulinerRnR.objects.filter(
                delstatus=False, done=done_status)[:count_data]
        else:
            obj_review_list = WebScrapPergiKulinerRnR.objects.filter(
                delstatus=False, done=done_status)
        print("obj_review_list count: {}".format(obj_review_list.count()))
        if obj_review_list.count() >= 1:

            # open connection into S3 - AWS
            cls_aws_S3 = UploadToS3()

            # get group activities for this review
            activity_group_obj = ActivityGroup.objects.get(
                group_name='Restoran')

            for idx_rev, item_review in enumerate(obj_review_list):
                print(f'[Review-page {idx_rev}]: {item_review.rnr_url}')

                item_page = item_review.web_pergikuliner
                # get branch object
                branch_name = item_page.branch.strip().replace(
                    "\n", "").replace("\r", "").replace("]", "").replace(
                    "[", " -").replace("  ", "").strip()
                slug_branch = slugify(branch_name)
                obj_branch = None
                obj_branch = Branch.objects.filter(slug=slug_branch)
                if obj_branch.count() >= 1:
                    obj_branch = obj_branch[0]
                else:
                    print(f'Branch Not Found!')
                    continue

                # rating
                if item_page.arr_ratings:
                    rating_list = eval(item_page.arr_ratings)
                    print(f'rating_list: {rating_list}')
                    dict_review_master = rating_list[1]

                    # add rating masters
                    if dict_review_master:
                        print(f'dict_review_master: {dict_review_master}')
                        if self.reviews_to_db:
                            for key_master in dict_review_master:
                                rating_master = key_master.strip()
                                obj_rating_master = RatingReviewMasters.objects.filter(
                                    rating_name=rating_master)
                                if obj_rating_master.count() >= 1:
                                    obj_rating_master = obj_rating_master[0]
                                else:
                                    obj_rating_master = RatingReviewMasters(
                                        rating_name=rating_master,
                                        is_active=True
                                    )
                                    obj_rating_master.save()

                                # save into RatingReviewActivity
                                obj_review_act = RatingReviewActivity.objects.filter(
                                    rating_review_master=obj_rating_master,
                                    activity_group=activity_group_obj)
                                if obj_review_act.count() == 0:
                                    obj_act_save = RatingReviewActivity(
                                        rating_review_master=obj_rating_master,
                                        activity_group=activity_group_obj)
                                    obj_act_save.save()

                if self.reviews_to_db:
                    pesan_menu = ''
                    if item_review.content_bottom_data:
                        pesan_menu = item_review.content_bottom_data[0].strip(
                        )
                    obj_branch_review = BranchRatingReviews.objects.filter(
                        branch=obj_branch,
                        name_reviewer=item_review.reviewer_name.strip())
                    if obj_branch_review.count() >= 1:
                        obj_branch_review = obj_branch_review[0]
                    else:
                        # store avatar to s3
                        url_img_download = item_review.reviewer_pic
                        dir_branch_id = "{}{}".format(
                            '/server/media/reviews/avatar/', obj_branch.pk)
                        avatar_url = cls_aws_S3.upload_from_url(
                            url_img_download, dir_branch_id)

                        print(
                            f'item_review.rating_total: {item_review.rating_total}')
                        total_rating = 0
                        if item_review.rating_total:
                            total_rating = item_review.rating_total

                        obj_branch_review = BranchRatingReviews(
                            branch=obj_branch,
                            rating=total_rating,
                            subject=item_review.review_title_str,
                            review=item_review.review_msg.replace(
                                'pergikuliner.com', '').replace('pergikuliner', ''),
                            name_reviewer=item_review.reviewer_name.strip(),
                            published=True,
                            avatar=avatar_url,
                            # email_reviewer,
                            # phone_number,
                            publish_note='{}, {}'.format(
                                'pergikuliner.com', pesan_menu)
                        )
                        obj_branch_review.save()

                    # get list rating master
                    obj_list_master = RatingReviewActivity.objects.filter(
                        activity_group=activity_group_obj
                    )
                    if obj_list_master.count():
                        # insert rating details
                        for item_rating_master in obj_list_master:
                            obj_detail = BranchRatingReviewDetails(
                                score=obj_branch_review.rating,
                                rating_review=obj_branch_review,
                                rating_name=item_rating_master.rating_review_master.rating_name,
                            )
                            obj_detail.save()

                obj_rnr_imagelist = WebScrapPergiKulinerRnRImage.objects.filter(
                    done=False, web_pergikuliner_rnr=item_review
                )
                if obj_rnr_imagelist.count() >= 1:
                    for idx_image, item_image in enumerate(obj_rnr_imagelist):
                        # print(
                        #     f'[{idx_rev}-{idx_image}] item_image: {item_image}')

                        if self.reviews_to_db:
                            # store avatar to s3
                            url_img_download = item_review.reviewer_pic
                            dir_branch_id = "{}{}".format(
                                '/server/media/reviews/branch/', obj_branch.pk)
                            photo_s3_url = cls_aws_S3.upload_from_url(
                                url_img_download, dir_branch_id)

                            obj_check_photo = BranchRatingReviewPhotos.objects.filter(
                                rating_review=obj_branch_review,
                                img_url=photo_s3_url
                            )
                            if obj_check_photo.count() == 0:
                                obj_review_img = BranchRatingReviewPhotos(
                                    rating_review=obj_branch_review,
                                    title='{}-{}'.format(
                                        obj_branch_review.name_reviewer, 'tscrap-pgkl'),
                                    img_url=photo_s3_url)
                                obj_review_img.save()

                            item_image.done = True
                            item_image.save()

                # set done review rnr - status done
                if self.reviews_to_db:
                    item_review.done = True
                    item_review.save()

                cls_aws_S3.close_connection()
        return "Success"

    def parse_pergikuliner_reviews2(self, count_data=None):
        done_status = True
        cls_aws_S3 = UploadToS3()
        if count_data:
            obj_pergikuliner = WebScrapPergiKuliner.objects.filter(
                delstatus=False, done=done_status)[:count_data]
        else:
            obj_pergikuliner = WebScrapPergiKuliner.objects.filter(
                delstatus=False, done=done_status)
        print("obj_pergikuliner count: {}".format(obj_pergikuliner.count()))

        # get group activities for this review
        activity_group_obj = ActivityGroup.objects.get(
            group_name='Restoran')

        if obj_pergikuliner.count() >= 1:
            for idx_, item_page in enumerate(obj_pergikuliner):
                print(f'[{idx_}] {item_page.web_url}')

                # get branch object
                branch_name = item_page.branch.strip().replace(
                    "\n", "").replace("\r", "").replace("]", "").replace(
                        "[", " -").replace("  ", "").strip()
                slug_branch = slugify(branch_name)
                obj_branch = None
                obj_branch = Branch.objects.filter(slug=slug_branch)
                if obj_branch.count() >= 1:
                    obj_branch = obj_branch[0]
                else:
                    print(f'Branch Not Found!')
                    continue

                # rating
                if item_page.arr_ratings:
                    rating_list = eval(item_page.arr_ratings)
                    print(f'rating_list: {rating_list}')
                    dict_review_master = rating_list[1]

                    # add rating masters
                    if dict_review_master:
                        print(f'dict_review_master: {dict_review_master}')
                        if self.reviews_to_db:
                            for key_master in dict_review_master:
                                rating_master = key_master.strip()
                                obj_rating_master = RatingReviewMasters.objects.filter(
                                    rating_name=rating_master)
                                if obj_rating_master.count() >= 1:
                                    obj_rating_master = obj_rating_master[0]
                                else:
                                    obj_rating_master = RatingReviewMasters(
                                        rating_name=rating_master,
                                        is_active=True
                                    )
                                    obj_rating_master.save()

                                # save into RatingReviewActivity
                                obj_review_act = RatingReviewActivity.objects.filter(
                                    rating_review_master=obj_rating_master,
                                    activity_group=activity_group_obj)
                                if obj_review_act.count() == 0:
                                    obj_act_save = RatingReviewActivity(
                                        rating_review_master=obj_rating_master,
                                        activity_group=activity_group_obj)
                                    obj_act_save.save()

                obj_review_list = WebScrapPergiKulinerRnR.objects.filter(
                    done=False, web_pergikuliner=item_page
                )
                if obj_review_list.count() >= 1:
                    for idx_rev, item_review in enumerate(obj_review_list):
                        print(f'[Review-page {idx_rev}]: {item_review}')
                        # {item_review.review_title_str}
                        # {item_review.review_title_by}
                        # {item_review.reviewer_pic}
                        # {item_review.reviewer_name}
                        # {item_review.rating_total}
                        # {item_review.review_msg}
                        # {item_review.content_bottom_data}

                        if self.reviews_to_db:
                            pesan_menu = ''
                            if item_review.content_bottom_data:
                                pesan_menu = item_review.content_bottom_data[0].strip(
                                )
                            obj_branch_review = BranchRatingReviews.objects.filter(
                                branch=obj_branch,
                                name_reviewer=item_review.reviewer_name.strip())
                            if obj_branch_review.count() >= 1:
                                obj_branch_review = obj_branch_review[0]
                            else:
                                # store avatar to s3
                                url_img_download = item_review.reviewer_pic
                                dir_branch_id = "{}{}".format(
                                    '/server/media/reviews/avatar/', obj_branch.pk)
                                avatar_url = cls_aws_S3.upload_from_url(
                                    url_img_download, dir_branch_id)

                                obj_branch_review = BranchRatingReviews(
                                    branch=obj_branch,
                                    rating=item_review.rating_total,
                                    subject=item_review.review_title_str,
                                    review=item_review.review_msg.replace(
                                        'pergikuliner.com', '').replace('pergikuliner', ''),
                                    name_reviewer=item_review.reviewer_name.strip(),
                                    published=True,
                                    avatar=avatar_url,
                                    # email_reviewer,
                                    # phone_number,
                                    publish_note='{}, {}'.format(
                                        'pergikuliner.com', pesan_menu)
                                )
                                obj_branch_review.save()

                            # get list rating master
                            obj_list_master = RatingReviewActivity.objects.filter(
                                activity_group=activity_group_obj
                            )
                            if obj_list_master.count():
                                # insert rating details
                                for item_rating_master in obj_list_master:
                                    obj_detail = BranchRatingReviewDetails(
                                        score=obj_branch_review.rating,
                                        rating_review=obj_branch_review,
                                        rating_name=item_rating_master.rating_review_master.rating_name,
                                    )
                                    obj_detail.save()

                        obj_rnr_imagelist = WebScrapPergiKulinerRnRImage.objects.filter(
                            done=False, web_pergikuliner_rnr=item_review
                        )
                        if obj_rnr_imagelist.count() >= 1:
                            for idx_image, item_image in enumerate(obj_rnr_imagelist):
                                # print(
                                #     f'[{idx_rev}-{idx_image}] item_image: {item_image}')

                                if self.reviews_to_db:
                                    # store avatar to s3
                                    url_img_download = item_review.reviewer_pic
                                    dir_branch_id = "{}{}".format(
                                        '/server/media/reviews/branch/', obj_branch.pk)
                                    photo_s3_url = cls_aws_S3.upload_from_url(
                                        url_img_download, dir_branch_id)

                                    obj_check_photo = BranchRatingReviewPhotos.objects.filter(
                                        rating_review=obj_branch_review,
                                        img_url=photo_s3_url
                                    )
                                    if obj_check_photo.count() == 0:
                                        obj_review_img = BranchRatingReviewPhotos(
                                            rating_review=obj_branch_review,
                                            title='{}-{}'.format(
                                                obj_branch_review.name_reviewer, 'pergikuliner.com'),
                                            img_url=photo_s3_url)
                                        obj_review_img.save()

                                    item_image.done = True
                                    item_image.save()

                        # set done review rnr - status done
                        if self.reviews_to_db:
                            item_review.done = True
                            item_review.save()
                # break for root-loop
                # break
        cls_aws_S3.close_connection()
        return "Success"

    def parse_branch_operating_hour(self, count_data=None):
        """
        
        """
        done_status = False  # , web_pergikuliner=item_page
        if count_data:
            obj_branch_list = Branch.objects.filter(source='pergikuliner.com',
                                                    delstatus=False, is_done=done_status)[:count_data]
        else:
            obj_branch_list = Branch.objects.filter(source='pergikuliner.com',
                                                    delstatus=False, is_done=done_status)
        print("obj_branch_list count: {}".format(obj_branch_list.count()))
        if obj_branch_list.count() >= 1:
            for idx_, item_branch in enumerate(obj_branch_list):
                print(
                    f'[{idx_}]: branch : {item_branch}')
                op_hour = item_branch.operating_hour
                if op_hour:
                    op_hour = op_hour.replace(
                        'Jam Buka: ', '').replace(
                            'JamBuka', 'Jam').replace('TutupBuka', 'Tutup').replace('Buka', '').replace('TutupHari', 'Tutup').replace(
                                'Hampir Tutup', '')
                    op_hour_list = op_hour.split(",")
                    op_hour_list = [item.replace(' ', '').lower()
                                    for item in op_hour_list]
                    print(f'len(op_hour_list): {len(op_hour_list)}')
                    print(
                        f'-->: {op_hour_list}')

                    if op_hour_list:
                        obj_op_hour_bulk=[]
                        for item_op_hour in op_hour_list:
                            aa_match = None
                            if re.match(r'(\w+)-(\w+)\((\d{2}:\d{2})-(\d{2}:\d{2})\)', item_op_hour):
                                aa_match = re.match(
                                    r'(\w+)-(\w+)\((\d{2}:\d{2})-(\d{2}:\d{2})\)', item_op_hour).groups()
                                print(
                                    f'{item_op_hour} id number 1 {aa_match}')
                                range_start = self.check_day(aa_match[0])
                                range_end = self.check_day(aa_match[1])

                                time_start = aa_match[2].replace('24:00', '00:00').replace('28:00','00:00')
                                time_end = aa_match[3].replace('24:00','00:00').replace('28:00','00:00')
                                time_start = datetime.strptime(
                                    time_start, '%H:%M').time()
                                time_end = datetime.strptime(
                                    time_end, '%H:%M').time()
                                range_end_check = range_end
                            
                                range_sunday=False  
                                if range_end_check > 0:
                                    range_end = range_end+1
                                else:
                                    range_sunday = True
                                    range_end = 7
                                # print(range_start, range_end)
                                for day_here in range(range_start, range_end):
                                    obj_op_hour = BranchOperationalHour(
                                        branch=item_branch,
                                        day=day_here,
                                        hour_start=time_start,
                                        hour_end=time_end,
                                    )
                                    obj_op_hour_bulk.append(obj_op_hour)
                                
                                if range_sunday:
                                    obj_op_hour = BranchOperationalHour(
                                        branch=item_branch,
                                        day=0,
                                        hour_start=time_start,
                                        hour_end=time_end,
                                    )
                                    obj_op_hour_bulk.append(obj_op_hour)
                                # print(f'obj_op_hour_bulk 0: {obj_op_hour_bulk}')
                            elif re.match(
                                    r'(\w+)\((\d{2}:\d{2})-(\d{2}:\d{2})\)', item_op_hour):
                                aa_match = re.match(
                                    r'(\w+)\((\d{2}:\d{2})-(\d{2}:\d{2})\)', item_op_hour).groups()
                                print(
                                    f'{item_op_hour} id number 2 {aa_match}')
                                day_select = self.check_day(aa_match[0])
                                time_start = aa_match[1].replace(
                                    '24:00', '00:00')
                                time_end = aa_match[2].replace(
                                    '24:00', '00:00')
                                time_start = datetime.strptime(
                                    time_start, '%H:%M').time()
                                time_end = datetime.strptime(
                                    time_end, '%H:%M').time()
                                print(f'{time_start}-{time_end}')

                                obj_op_hour = BranchOperationalHour(
                                    branch=item_branch,
                                    day=day_select,
                                    hour_start=time_start,
                                    hour_end=time_end,
                                )
                                obj_op_hour_bulk.append(obj_op_hour)
                                # print(f'obj_op_hour_bulk 1: {obj_op_hour_bulk}')
                            elif item_op_hour=='24jam':
                                print(f'{item_op_hour} id number 3 {item_op_hour}')
                                time_start = datetime.strptime(
                                    '00:00', '%H:%M').time()
                                time_end = datetime.strptime(
                                    '23:59', '%H:%M').time()
                                print(f'{time_start}-{time_end}')

                                for day_here in range(0, 7):
                                    obj_op_hour = BranchOperationalHour(
                                        branch=item_branch,
                                        day=day_here,
                                        hour_start=time_start,
                                        hour_end=time_end,
                                    )
                                    obj_op_hour_bulk.append(obj_op_hour)
                                # print(f'obj_op_hour_bulk 2: {obj_op_hour_bulk}')
                            else:
                                print(f'{item_op_hour} not match anything!!')

                        # print(f'obj_op_hour_bulk : {obj_op_hour_bulk}')   
                        if self.op_hour_to_db:
                            #insert bulk insert
                            BranchOperationalHour.objects.bulk_create(
                                obj_op_hour_bulk)

                            # update status, operating hour has done
                            item_branch.is_done = True
                            item_branch.save()

    def parse_branch_tags(self, count_data=None):
        print("START parse_branch_tags")
        max_bulk = 100
        # BranchTags(branch, tag)
        if count_data:
            branch_obj_list = Branch.objects.filter(source='pergikuliner.com',
                                                    delstatus=False, is_done=0,
                                                    branch_type__isnull=False)[:count_data]
        else:
            branch_obj_list = Branch.objects.filter(source='pergikuliner.com',
                                                    delstatus=False, is_done=0,
                                                    branch_type__isnull=False)
        print("branch_obj_list count: {}".format(branch_obj_list.count()))
        if branch_obj_list.count() >= 1:
            max_bulk_count = 0
            branch_bulk = []
            for idx_, item_branch in enumerate(branch_obj_list):
                # print(
                #     f'{idx_}: {item_branch} branch-type: {item_branch.branch_type}')

                # get group activities for this review
                tag_group_obj = TagGroup.objects.get(
                    name='Restoran')

                branch_type_here = item_branch.branch_type.name.strip().replace(
                    'Restaurant -','').strip()
                
                tag_list = branch_type_here.split(',')
                if tag_list:
                    for tag_item in tag_list:
                        tag_item_clean = tag_item.strip().lower()
                        if tag_item_clean == '':
                            continue
                        
                        check_tag = Tag.objects.filter(group=tag_group_obj,
                                                              tag=tag_item_clean)
                        if check_tag.count()==0:
                            obj_save = Tag(group=tag_group_obj,
                                tag=tag_item_clean)
                            obj_save.save()
                        else:
                            obj_save = check_tag[0]
                        
                        check_branch_tag = BranchTags.objects.filter(branch=item_branch,
                                                                     tag=obj_save)
                        if check_branch_tag.count() == 0:
                            obj_branch_tag=BranchTags(branch=item_branch,
                                tag=obj_save)
                            # obj_branch_tag.save()
                            branch_bulk.append(obj_branch_tag)
                            max_bulk_count = max_bulk_count + 1

                            if max_bulk_count == max_bulk:
                                print(
                                    f'{max_bulk_count}: == {max_bulk}')
                                if branch_bulk:
                                    BranchTags.objects.bulk_create(branch_bulk)
                                    max_bulk_count = 0
                                    branch_bulk = []
                                    print(
                                        f'bulk_create SUCCESS')
                    
                    #update status branch
                    item_branch.is_done=1
                    item_branch.save()
            #last save
            if max_bulk_count:
                if branch_bulk:
                    BranchTags.objects.bulk_create(branch_bulk)
                    max_bulk_count = 0
            
            #update is_done=1
            # branch_obj_list.update(is_done=1)
        print("START parse_branch_tags")
        return "Success"
                    
    def check_day(self, day_str):
        day_str_lower = day_str.lower().strip()
        const_day = BranchOperationalHour.OperationDayChoices
        if day_str_lower == 'senin':
            res_out = const_day.MONDAY
        elif day_str_lower == 'selasa':
            res_out = const_day.TUESDAY
        elif day_str_lower == 'rabu':
            res_out = const_day.WEDNESDAY
        elif day_str_lower == 'kamis':
            res_out = const_day.THURSDAY
        elif day_str_lower == 'jumat':
            res_out = const_day.FRIDAY
        elif day_str_lower == 'sabtu':
            res_out = const_day.SATURDAY
        else:
            res_out = const_day.SUNDAY
        return res_out

    def update_branch_building(self, count_data=None):
        print(f'START update branch Building')
        done_status = 0
        if count_data:
            obj_pergikuliner = WebScrapPergiKuliner.objects.filter(
                delstatus=False, done=done_status)[:count_data]
        else:
            obj_pergikuliner = WebScrapPergiKuliner.objects.filter(
                delstatus=False, done=done_status)
        print("obj_pergikuliner count: {}".format(obj_pergikuliner.count()))
        if obj_pergikuliner.count():
            for idx_, item_page in enumerate(obj_pergikuliner):
                print(f'[{idx_}] {item_page.web_url}')

                # add building
                obj_building = self.create_building(item_page)

                # update branch
                branch_name = item_page.branch.strip().replace(
                            "\n", "").replace("\r", "").replace("]", "").replace(
                            "[", " -").replace("  ", "").strip()
                slug_branch = slugify(branch_name)
                obj_branch = None
                if self.store_to_db:
                    obj_branch = Branch.objects.filter(slug=slug_branch)
                    if obj_branch.count() >= 1:
                        print(f'{obj_branch} building Updated')
                        obj_branch = obj_branch[0]
                        obj_branch.building = obj_building
                        obj_branch.source = 'pergikuliner.com'
                        obj_branch.save()
                
                #update done status
                item_page.done=1
                item_page.save()
        print('DONE update branch Building')
        return "success"

    def update_branch_price(self, count_data=None):
        #price_info
        """
        Rp. 100.000 - Rp. 200.000 /orang
        Di bawah Rp. 50.000  /orang
        Di atas Rp. 200.000 /orang
        Di bawah Rp. 50.000 /orang
        Rp. 50.000 - Rp. 100.000 /orang
        Di Bawah Rp. 50.000 /orang
        """
        print("START update_branch_price")
        # BranchTags(branch, tag)
        if count_data:
            branch_obj_list = Branch.objects.filter(source='pergikuliner.com',
                                                    delstatus=False, is_done=0,
                                                    price_info__isnull=False)[:count_data]
        else:
            branch_obj_list = Branch.objects.filter(source='pergikuliner.com',
                                                    delstatus=False, is_done=0,
                                                    price_info__isnull=False)
        print("branch_obj_list count: {}".format(branch_obj_list.count()))
        if branch_obj_list.count() >= 1:
            for idx_, item_branch in enumerate(branch_obj_list):
                price_info_here = item_branch.price_info.strip().lower().replace(
                    ' ', '').replace('/orang', '').replace('rp.', '')
                
                print(
                    f'{idx_}: {item_branch.branch_name}:: price_info: {price_info_here}')

                price_min = None
                price_max = None
                if price_info_here.find('bawah') >= 0:
                    price_min = 0
                    price_max = price_info_here.replace(
                        'dibawah', '').replace('.0', '0')
                    price_max = float(price_max)
                elif price_info_here.find('atas') >= 0:
                    price_min = price_info_here.replace(
                        'diatas', '').replace('.0', '0')
                    price_min = float(price_min)
                    price_max = float(price_min) * 10
                elif price_info_here.find('-') >= 0:
                    price_clean = price_info_here.split('-')
                    price_min = float(price_clean[0].replace('.0', '0'))
                    price_max = float(price_clean[1].replace('.0', '0'))
                else:
                    pass
                print(
                    f'price_min {price_min}: price_max: {price_max}')
                if self.store_to_db:
                    if price_min and price_max:
                        if price_min >=0 and price_max>=0:
                            item_branch.price_min = price_min
                            item_branch.price_max = price_max
                            #update status branch
                            item_branch.is_done=1
                            item_branch.save()
            
        print("START update_branch_price")
        return "Success"

    def update_branch_operational_hour(self, count_data=None):
        #operating_hour
        print("START update_branch_operational_hour")
        # BranchTags(branch, tag)
        if count_data:
            branch_obj_list = Branch.objects.filter(source='pergikuliner.com',
                                                    delstatus=False, is_done=0,
                                                    operating_hour__isnull=False,
                                                    #operating_hour__icontains='Hampir Tutup',
                                                    )[:count_data]
        else:
            branch_obj_list = Branch.objects.filter(source='pergikuliner.com',
                                                    delstatus=False, is_done=0,
                                                    operating_hour__isnull=False,
                                                    #operating_hour__icontains='Hampir Tutup',
                                                    )
        print("branch_obj_list count: {}".format(branch_obj_list.count()))
        if branch_obj_list.count() >= 1:
            for idx_, item_branch in enumerate(branch_obj_list):
                op_hour = item_branch.operating_hour
                print(
                    f'{idx_}: {item_branch.branch_name}:: op_hour: {op_hour}')
                if op_hour:
                    op_hour = op_hour.replace(
                        'Jam Buka: ', '').replace(
                            'JamBuka', 'Jam').replace('TutupBuka', 'Tutup').replace('Buka', '').replace('TutupHari', 'Tutup').replace(
                                'Hampir Tutup','')
                    item_branch.operating_hour = op_hour
                else:
                    item_branch.operating_hour = 'Belum ber-operational'

                #update status branch
                item_branch.is_done=1
                if self.store_to_db:
                    item_branch.save()
            
        print("START update_branch_operational_hour")
        return "Success"

    def compress_branch_images(self, count_data=None, char_start=None):
         #operating_hour
        print("START update_branch_operational_hour")
        # BranchTags(branch, tag)
        if count_data:
            branch_img_list = BranchImages.objects.filter(
                                                    delstatus=False, is_done=0,
                                                    )[:count_data]
        else:
            branch_img_list = BranchImages.objects.filter(
                                                    delstatus=False, is_done=0,
                                                    )
        if char_start:
            branch_img_list = branch_img_list.filter(branch__branch_name__startswith=char_start)
        
        print("branch_img_list count: {}".format(branch_img_list.count()))
        if branch_img_list.count() >= 1:
            cls_img_compress = BranchImageCompressor()
            cls_img_compress.open_class_s3()

            for id_, item_img in enumerate(branch_img_list):
                print(f'item_img: {item_img.image_url}')
                # url_input = 'https://halalmas.s3-ap-southeast-1.amazonaws.com/server/media/branch/1000/picture-1450443521.jpg'
                url_input = item_img.image_url
                img_size = cls_img_compress.get_img_from_url(url_input)
                file_nm, s3_path = cls_img_compress.compress_and_upload_to_s3()

                #update fields
                item_img.name = file_nm
                item_img.s3_path = s3_path
                item_img.img_prefix = 'ori, lg, md, sm, thumb'
                item_img.size = img_size

                #update status
                item_img.is_done=1
                item_img.save()

            #close s3 connection
            cls_img_compress.close_s3_connection()
        print("END update_branch_operational_hour")
    
    def compress_branch_review_images(self, count_data=None):
         #operating_hour
        print("START compress_branch_review_images")
        # BranchTags(branch, tag)
        if count_data:
            branch_img_list = BranchRatingReviewPhotos.objects.filter(
                delstatus=False, is_done=0,
            )[:count_data]
        else:
            branch_img_list = BranchRatingReviewPhotos.objects.filter(
                delstatus=False, is_done=0,
            )
        print("branch_img_list count: {}".format(branch_img_list.count()))
        if branch_img_list.count() >= 1:
            cls_img_compress = BranchImageCompressor()
            cls_img_compress.open_class_s3()

            for id_, item_img in enumerate(branch_img_list):
                print(f'item_img: {item_img.img_url}')
                # url_input = 'https://halalmas.s3-ap-southeast-1.amazonaws.com/server/media/branch/1000/picture-1450443521.jpg'
                url_input = item_img.img_url
                img_size = cls_img_compress.get_img_from_url(url_input)
                file_nm, s3_path = cls_img_compress.compress_and_upload_to_s3()

                #update fields
                item_img.name = file_nm
                item_img.s3_path = s3_path
                item_img.img_prefix = 'ori, lg, md, sm, thumb'
                # item_img.size = img_size

                #update status
                item_img.is_done = 1
                item_img.save()

            #close s3 connection
            cls_img_compress.close_s3_connection()
        print("END compress_branch_review_images")
    
    def compress_branch_review_avatar(self, count_data=None):
         #operating_hour
        print("START compress_branch_review_avatar")
        # BranchTags(branch, tag)
        if count_data:
            branch_img_list = BranchRatingReviews.objects.filter(
                delstatus=False, is_done=0, avatar__isnull=False,
            )[:count_data]
        else:
            branch_img_list = BranchRatingReviews.objects.filter(
                delstatus=False, is_done=0, avatar__isnull=False,
            )
        print("branch_img_list count: {}".format(branch_img_list.count()))
        if branch_img_list.count() >= 1:
            cls_img_compress = BranchImageCompressor()
            cls_img_compress.open_class_s3()

            for id_, item_img in enumerate(branch_img_list):
                print(f'item_img: {item_img.avatar}')
                # url_input = 'https://halalmas.s3-ap-southeast-1.amazonaws.com/server/media/branch/1000/picture-1450443521.jpg'
                url_input = item_img.avatar
                img_size = cls_img_compress.get_img_from_url(url_input)
                file_nm, s3_path = cls_img_compress.compress_and_upload_to_s3()

                #update fields
                item_img.name = file_nm
                item_img.s3_path = s3_path
                item_img.img_prefix = 'ori, lg, md, sm, thumb'
                # item_img.size = img_size

                #update status
                item_img.is_done = 1
                item_img.save()

            #close s3 connection
            cls_img_compress.close_s3_connection()
        print("END compress_branch_review_avatar")

    def parse_branch_group_activity(self, count_data=None):
        print("START parse_branch_group_activity")
        max_bulk = 100
        # BranchTags(branch, tag)
        if count_data:
            branch_obj_list = Branch.objects.filter(source='pergikuliner.com',
                                                    delstatus=False, is_done=0)[:count_data]
        else:
            branch_obj_list = Branch.objects.filter(source='pergikuliner.com',
                                                    delstatus=False, is_done=0)
        print("branch_obj_list count: {}".format(branch_obj_list.count()))
        if branch_obj_list.count() >= 1:

            # get group activities for this review
            activity_group_obj = ActivityGroup.objects.get(
                group_name='Restoran')

            for idx_branch, branch_item in enumerate(branch_obj_list):
                print(f'[Branch-item {idx_branch}]: {branch_item}')

                obj_branch_act = BranchActivity(branch=branch_item,
                               activity_group=activity_group_obj)
                
                obj_branch_act.save()

                #update is_done=1
                branch_item.is_done=1
                branch_item.save()

        return "Success"
def run_parsing_pergikuliner():
    PergikulinerParsetoTempat().parse_pergikuliner(1)


def run_parsing_pergikuliner_reviews():
    PergikulinerParsetoTempat().parse_pergikuliner_reviews(11)


def run_parsing_branch_operating_hour():
    PergikulinerParsetoTempat().parse_branch_operating_hour(500)


def run_parsing_branch_tags():
    max_record = 100
    branch_all = 520
    range_data = int(branch_all/max_record)
    data_mod = branch_all % max_record
    for rec_count in range(range_data):
        print(f'rec_count {rec_count} : {max_record} START')
        PergikulinerParsetoTempat().parse_branch_tags(max_record)
        print(f'rec_count {rec_count} : {max_record} END')

    if(data_mod):
        print(f'data_mod {data_mod} : START')
        PergikulinerParsetoTempat().parse_branch_tags(data_mod)
        print(f'data_mod {data_mod} : END')
    PergikulinerParsetoTempat().parse_pergikuliner_reviews(11)


def run_update_branch_building():
    PergikulinerParsetoTempat().update_branch_building(10)


def run_update_branch_price():
    PergikulinerParsetoTempat().update_branch_price()


def run_update_branch_operational_hour():
    PergikulinerParsetoTempat().update_branch_operational_hour()


def run_compress_branch_images():
    PergikulinerParsetoTempat().compress_branch_images(10)


def run_compress_branch_review_images():
    PergikulinerParsetoTempat().compress_branch_review_images(10000)


def run_compress_branch_review_avatar():
    PergikulinerParsetoTempat().compress_branch_review_avatar(10000)

def run_parse_branch_group_activity():
    PergikulinerParsetoTempat().parse_branch_group_activity(10)

if __name__ == "__main__":
    run_parsing_pergikuliner()
