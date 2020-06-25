import csv
import json
import re
import requests
import pprint

from time import sleep
from bs4 import BeautifulSoup


from halalmas.scrappers.models import WebScrapper, WebScrapperDetail
from halalmas.scrappers.pergikuliner.models import (
    WebScrapPergiKuliner, WebScrapPergiKulinerImage,
    WebScrapPergiKulinerRnR, WebScrapPergiKulinerRnRImage)

DOMAIN_NAME_TO_SCRAP = 'https://pergikuliner.com'


class WebScrapping(object):
    def __init__(self, url, location, count_data=None):
        self.url = url
        self.location = location
        self.count_data = count_data
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
        # self.dict_key_name = ['code', 'value', 'sale', 'buy']

    def clean_list(self, data_in):
        data_out = data_in.strip().split("\n")
        return self.remove_empty_on_list(data_out)

    def remove_empty_on_list(self, data_arr):
        data_out = [
            x for x in data_arr if x != '']
        data_out = [x.replace("\n", "").replace(
            "[", "").replace("]", "") for x in data_out]
        data_out = [x.replace("  ", "") for x in data_out]
        data_out = map(str.strip, data_out)
        return list(data_out)

    def concate_list_to_dict(self, list_1, list_2):
        list_2_out = []
        for idx, item in enumerate(list_1):
            list_2_out.append(list_2[idx].replace(item, ""))
        return dict(zip(list_1, list_2_out))

    def get_location_from_script(self, soup_in):
        script_ = soup_in.find_all(
            'script')
        if script_:
            for src_ in script_:
                res_find = src_.text.find(
                    "map_options()")
                # print('res_find: {}'.format(res_find))
                if res_find > 0:
                    find_end = src_.text[res_find:].find(");")
                    # print('find_end: {}'.format(find_end))
                    if find_end:
                        str_func = src_.text[res_find:(res_find+find_end)]
                        # print('lat-lon: {}'.format(str_func))
                        # parsing latlon
                        data_out = str_func.replace("map_options() {", "")
                        find_start = data_out.find("{")
                        find_end = data_out.find("}")
                        data_out = data_out[find_start:find_end+1]
                        # print('data_out: {}'.format(data_out))
                        data_out_dict = json.loads(
                            data_out.replace('  ', '').replace(u'\xa0', ""))
                        return data_out_dict
        else:
            return {}

    def get_all_images(self, url_root):
        """
        https://pergikuliner.com/restaurants/ab-steakhouse-by-chef-akira-back-setiabudi/gallery?filter_by=semua&page=2
        """
        # remove location on url
        new_url = "{}/{}".format(url_root.rsplit('/', 2)
                                 [0], url_root.rsplit('/', 1)[1])

        filter_by = ['semua', 'makanan', 'suasana']
        data_dict_out = {}
        for filter_item in filter_by:
            data_list_out = []
            for idx_item in range(1, 6):
                url_image = "{}/gallery?filter_by={}&page={}".format(
                    new_url, filter_item, idx_item)
                # print("url_image {}".format(url_image))

                html2 = None
                r2 = requests.get(
                    url_image, headers=self.headers, timeout=100)
                # print("OK #1", r)
                if r2.status_code == 200:
                    html2 = r2.text
                    soup_image = BeautifulSoup(html2, 'html.parser')
                    img_tag_all = soup_image.find_all(
                        'img', attrs={'class': "img-responsive"})
                    for img_item in img_tag_all:
                        img_src = img_item['src']
                        img_src_selected = "{}{}".format(
                            "https:", img_src.rsplit('https:', 1)[1])
                        # print("img_item: {}".format(img_src_selected))
                        data_list_out.append(img_src_selected)
            data_dict_out[filter_item] = data_list_out
        return data_dict_out

    def get_reviews(self, soup_in, url_root):
        """
        div , class=reviews
        Review
        - User
        - title
        - reting per value
        - Review
        - Rating total per user
        - date visit
        - menu yang di pesan
        - foto
        - price per pax
        """
        div_reviews = soup_in.find(
            'div', attrs={'class': "reviews"})
        a_href_list = div_reviews.find_all(
            "a", attrs={'class': 'link-more-review'})
        url_list_review = []
        for a_href_item in a_href_list:
            a_href_url = a_href_item['href']
            url_list_review.append(a_href_url)
            # print("a_href_url: {}".format(a_href_url))

        data_list_out = []
        if url_list_review:
            for url_item in url_list_review:
                # init dict out
                data_dict_out = {}
                data_dict_out['rnr_url'] = ''
                data_dict_out['review_title_str'] = ''
                data_dict_out['review_title_by'] = ''
                data_dict_out['reviewer_pic'] = ''
                data_dict_out['reviewer_name'] = ''
                data_dict_out['rating_total'] = ''
                data_dict_out['rating_image'] = ''
                data_dict_out['review_msg'] = ''
                data_dict_out['content_bottom_data'] = ''

                html2 = None
                url_review = "{}{}".format(DOMAIN_NAME_TO_SCRAP, url_item)
                r2 = requests.get(
                    url_review, headers=self.headers, timeout=100)
                # print("OK #1", r)
                if r2.status_code == 200:
                    html2 = r2.text
                    soup_review = BeautifulSoup(html2, 'html.parser')
                    review_title = soup_review.find(
                        'div', attrs={'class': "review-title"})
                    # print("review_title: {}".format(review_title))

                    data_dict_out['rnr_url'] = url_review
                    if review_title:
                        review_title_str = review_title.find("h2").text
                        review_title_by = review_title.find("p").text
                        # print("review_title_str: {}".format(review_title_str))
                        # print("review_title_by: {}".format(review_title_by))
                        data_dict_out['review_title_str'] = review_title_str
                        data_dict_out['review_title_by'] = review_title_by

                    # reviewer
                    div_reviewer = soup_review.find(
                        'div', attrs={'class': "reviewer-part"})
                    if div_reviewer:
                        # reviewer pic
                        reviewer_pic = div_reviewer.find("img")['src']
                        img_src_selected = "{}{}".format(
                            "https:", reviewer_pic.rsplit('https:', 1)[1])
                        img_src_selected = img_src_selected.rsplit('%', 2)[0]
                        # print("reviewer_pic: {}".format(img_src_selected))
                        data_dict_out['reviewer_pic'] = img_src_selected

                        # reviwer name
                        reviewer_name = div_reviewer.find(
                            "span", attrs={'itemprop': 'name'})
                        reviewer_name = reviewer_name.text.strip()
                        # print("reviewer_name: {}".format(reviewer_name))
                        data_dict_out['reviewer_name'] = reviewer_name

                        # rating-total
                        rating_total = soup_review.find(
                            "span", attrs={'itemprop': 'ratingValue'})
                        rating_total = rating_total.text.strip()
                        # print("rating_total: {}".format(
                        #     rating_total))
                        data_dict_out['rating_total'] = rating_total

                        # review image
                        review_image = soup_review.find(
                            "div", attrs={'class': 'image-list-wrapper row'})
                        review_image_2 = soup_review.find(
                            "div", attrs={'class': 'col-sm-9 col-md-10 image-list-wrapper'})
                        if review_image or review_image_2:
                            image_list_out = []
                            if review_image:
                                img_tag_all = review_image.find_all('img')
                                # print("img_tag_all: {}".format(img_tag_all))
                                for img_item in img_tag_all:
                                    img_src = img_item['src']
                                    img_src_selected = "{}{}".format(
                                        "https:", img_src.rsplit('https:', 1)[1])
                                    # print("img_item: {}".format(img_src_selected))
                                    image_list_out.append(img_src_selected)
                            if review_image_2:
                                img_tag_all = review_image_2.find_all('img')
                                # print("img_tag_all: {}".format(img_tag_all))
                                for img_item in img_tag_all:
                                    img_src = img_item['src']
                                    img_src_selected = "{}{}".format(
                                        "https:", img_src.rsplit('https:', 1)[1])
                                    # print("img_item: {}".format(
                                    #     img_src_selected))
                                    image_list_out.append(img_src_selected)
                            data_dict_out['rating_image'] = image_list_out

                        # menu yang dipesan
                        content_bottom = soup_review.find(
                            "div", attrs={'class': 'col-xs-12 content-bottom'})
                        # print("content_bottom: {}".format(content_bottom))
                        if content_bottom:
                            div_item = content_bottom.find_all("div")
                            content_bottom_data = []
                            for p_item in div_item:
                                aa = p_item.find("p")
                                if aa:
                                    content_bottom_data.append(aa.text.strip())
                                bb = p_item.find("span")
                                if bb:
                                    content_bottom_data.append(bb.text.strip())
                            # print("content_bottom_data: {}".format(
                            #     content_bottom_data))
                            data_dict_out['content_bottom_data'] = content_bottom_data

                        # review content
                        review_msg = soup_review.find(
                            "div", attrs={'itemprop': 'reviewBody'})
                        # print("review_msg: {}".format(
                            # review_msg))
                        data_dict_out['review_msg'] = review_msg
                # for loop break
                # break
                data_list_out.append(data_dict_out)
        return data_list_out

    def get_info_detail(self, soup_in):
        div_info_list = soup_in.find(
            'div', attrs={'class': 'info-list'})
        arr_li = [
            item.text for item in div_info_list.find_all('li')]
        arr_li_span = [
            item.text for item in div_info_list.find_all('span')]
        arr_info_span = self.remove_empty_on_list(arr_li_span)
        arr_info = self.remove_empty_on_list(arr_li)
        # print("arr_info_span: {}".format(arr_info_span))
        # print("arr_info: {}".format(arr_info))
        info_list_out = self.concate_list_to_dict(
            arr_info_span, arr_info)
        return info_list_out

    def get_facilities(self, soup_in):
        div_facility_list = soup_in.find(
            'div', attrs={'class': 'facility-list'})
        arr_li_facility_checked = [
            item.text for item in div_facility_list.find_all('label', attrs={'class': 'checked'})]
        arr_li_facility_unchecked = [
            item.text for item in div_facility_list.find_all('label', attrs={'class': 'unchecked'})]
        arr_facility_checked = self.remove_empty_on_list(
            arr_li_facility_checked)
        arr_facility_unchecked = self.remove_empty_on_list(
            arr_li_facility_unchecked)
        return arr_facility_checked, arr_facility_unchecked

    def get_ratings(self, soup_in):
        div_ratings = soup_in.find(
            'div', attrs={'class': 'item-rating'})
        total_rating = div_ratings.text
        arr_header = self.clean_list(total_rating)
        print("div_ratings: {}".format(arr_header))

        div_rating_detail = soup_in.find(
            'div', attrs={'class': 'detail-review row'})
        dict_detail = {}
        if div_rating_detail:
            arr_rating_detail_key = [
                item.text for item in div_rating_detail.find_all('div', attrs={'class': 'rate-box-top best-rating'})]
            arr_rating_detail_value = [
                item.text for item in div_rating_detail.find_all('div', attrs={'class': 'rate-box-bottom best-rating'})]
            arr_rating_detail_key = self.remove_empty_on_list(
                arr_rating_detail_key)
            arr_rating_detail_value = self.remove_empty_on_list(
                arr_rating_detail_value)
            # print("arr_rating_detail_key: {}".format(arr_rating_detail_key))
            # print("arr_rating_detail_value: {}".format(arr_rating_detail_value))
            dict_detail = self.concate_list_to_dict(
                arr_rating_detail_key, arr_rating_detail_value)
            
        return arr_header, dict_detail

    def get_listing(self):
        # get list group/header , location__in=['bandung', 'surabaya']
        web_scrapper_group = WebScrapper.objects.filter(
            domain_name=DOMAIN_NAME_TO_SCRAP, done=0)
        print("web_scrapper_group: {}".format(web_scrapper_group))
        if web_scrapper_group.count() == 0:
            return "-Data Group Not Exists to Scrap-"

        for web_data in web_scrapper_group:
            print("max_page: {}".format(web_data.max_page))
            for page in range(1, web_data.max_page):
                url_web_list = "{}{}".format(
                    web_data.urls_page[:len(web_data.urls_page)-1], page)
                print("url_web_list: {}".format(url_web_list))
                html = None
                try:
                    r = requests.get(
                        url_web_list, headers=self.headers, timeout=100)
                    # print("OK #1", r)
                    if r.status_code == 200:
                        html = r.text
                        # print("OK #2", html)

                        soup = BeautifulSoup(html, 'html.parser')
                        # print(soup.prettify(formatter="minimal"))

                        print("tag with h3")
                        for tag in soup.find_all('h3', attrs={'class': 'item-name'}):
                            url_detail = tag.find('a')['href']
                            print(url_detail)
                            obj_detail = WebScrapperDetail.objects.filter(
                                urls_detail=url_detail)
                            if obj_detail.count() == 0:
                                obj_save = WebScrapperDetail(
                                    web_source=web_data,
                                    urls_detail=url_detail)
                                obj_save.save()
                except Exception as ex:
                    print("ERR Exception : {}".format(str(ex)))
                finally:
                    print("{} OK".format(web_data))

    def listing_location(self):
        html = None
        try:
            r = requests.get(self.url, headers=self.headers, timeout=100)
            if r.status_code == 200:
                html = r.text
                soup = BeautifulSoup(html, 'html.parser')
                # print(soup.prettify(formatter="minimal"))

                print("tag with nav")
                for nav in soup.find_all('nav', attrs={'pagination'}):
                    last_page = nav.find('span', attrs={'last'})
                    print(last_page)
                    href_last_page = last_page.find('a')['href']
                    print(href_last_page)
                    int_last_page = href_last_page[href_last_page.find(
                        "=")+1:].strip()
                    print("int_last_page: {}".format(int_last_page))

                    obj_list = WebScrapper.objects.filter(
                        domain_name=DOMAIN_NAME_TO_SCRAP, location=self.location,
                        delstatus=False)
                    print("obj_list.count(): {}".format(obj_list.count()))
                    if obj_list.count() == 0:
                        WebScrapper.create(
                            DOMAIN_NAME_TO_SCRAP, self.location, self.url, int(int_last_page))
        except Exception as ex:
            print(str(ex))
        finally:
            return "OK"

    def scrap_scripts(self):
        print("START Scrapping Script Part")
        if self.count_data:
            web_detail_list = WebScrapperDetail.objects.filter(
                done=0).order_by("-pk")[:self.count_data]
        else:
            web_detail_list = WebScrapperDetail.objects.filter(
                done=0).order_by("-pk")
        print("web_detail_list count : {}".format(web_detail_list.count()))
        if web_detail_list.count() >= 1:
            for item_detail in web_detail_list:
                url_detail_page = "{}{}".format(
                    item_detail.web_source.domain_name, item_detail.urls_detail)
                print("url_detail_page: {}".format(url_detail_page))

                html = None
                try:
                    r = requests.get(
                        url_detail_page, headers=self.headers, timeout=100)
                    # print("OK #1", r)
                    if r.status_code == 200:
                        html = r.text
                        # print("OK #2", html)

                        soup = BeautifulSoup(html, 'html.parser')
                        # print(soup.prettify(formatter="minimal"))
                        data_location = self.get_location_from_script(soup)
                        print('location this branch: {}'.format(
                            data_location))
                except Exception as ex:
                    print("ERR Exception : {}".format(str(ex)))
                finally:
                    print("{} OK".format(item_detail))
        print("END Scrapping Script Part")

    def scrap_detail_page(self):
        """
        Nama Merchant -
        Brand Merchant -
        Building + Address + latlon -
        Nomor Telepon -
        Branch Price Range -
        Branch Type: Food and Beverage ???
        Tags(culinary, jenis makanan) -
        Payments -
        Facilities -
        Image Gallery -
        Rating -
        Review -
        - User
        - title
        - reting per value
        - Review
        - Rating total per user
        - date visit
        - menu yang di pesan
        - foto
        - price per pax
        """
        print("START Scrapping Detail Page")
        if self.count_data:
            web_detail_list = WebScrapperDetail.objects.filter(done=0, delstatus=False)[
                :self.count_data]
        else:
            web_detail_list = WebScrapperDetail.objects.filter(
                done=0, delstatus=False)

        print("web_detail_list count : {}".format(web_detail_list.count()))
        if web_detail_list.count() >= 1:
            for idx_row, item_detail in enumerate(web_detail_list):
                url_detail_page = "{}{}".format(
                    item_detail.web_source.domain_name, item_detail.urls_detail)
               
                html = None
                try:
                    # url_detail_page = 'https://pergikuliner.com/restaurants/jakarta/bakmi-ayam-alok-meruya'
                    print("[{}] url_detail_page: {}".format(idx_row, url_detail_page))
                    r = requests.get(
                        url_detail_page, headers=self.headers, timeout=100)
                    # print("OK #1", r)
                    if r.status_code == 200:
                        html = r.text
                        # print("OK #2", html)

                        soup = BeautifulSoup(html, 'html.parser')

                        # brand and branch
                        # branch = url_detail_page.rsplit('/', 1)[1]
                        # print("branch: {}".format(branch))
                        brand = soup.find('h1').text
                        print("brand: {}".format(
                            self.clean_list(brand)))
                        branch_2 = soup.find('h2').text
                        print("branch_2: {}".format(
                            self.clean_list(branch_2)))

                        # location this branch
                        data_location = self.get_location_from_script(soup)
                        print('location this branch: {}'.format(
                            data_location))

                        # get detail group
                        detail_group = soup.find(
                            'div', attrs={'id': 'height-mark'})
                        # print("detail_group: {}".format(detail_group))

                        # building and address
                        building_data = detail_group.find(
                            'span', attrs={'class': 'left'})
                        arr_building = self.clean_list(building_data.text)
                        print("building addrs: {}".format(arr_building))

                        # phone number and open time
                        phone_n_open = detail_group.find(
                            'p', attrs={'class': 'large-screen-toggle'})
                        # print("phone_n_open: {}".format(phone_n_open))
                        arr_phone_n_open = ''
                        if phone_n_open:
                            phone_n_open = phone_n_open.find_all('span')
                            arr_phone_n_open = self.clean_list(
                                phone_n_open[0].text)
                            # print("phone_n_open: {}".format(arr_phone_n_open))

                        # Price id:avg-price
                        price = detail_group.find(
                            'span', attrs={'id': 'avg-price'}).text.strip()
                        # print("price: {}".format(price))

                        # detail info branch
                        info_list_out = self.get_info_detail(soup)
                        # print("info_list_out: {}".format(info_list_out))

                        # facility part
                        arr_facility_checked, arr_facility_unchecked = self.get_facilities(
                            soup)
                        # print("arr_facility_checked: {}".format(
                        #     arr_facility_checked))
                        # print("arr_facility_unchecked: {}".format(
                        #     arr_facility_unchecked))

                        # # get ratings
                        arr_ratings = self.get_ratings(soup)
                        # print("arr_ratings: {}".format(arr_ratings))

                        # get images
                        print("-START Getting Image-")
                        dict_images = self.get_all_images(url_detail_page)
                        print("-END Getting Image-")

                        # get reviews
                        print("-START Getting Rating n Review-")
                        list_reviews = self.get_reviews(soup, url_detail_page)
                        print("-END Getting Rating n Review-")

                        #save to DB
                        obj_pergikuliner = WebScrapPergiKuliner.objects.filter(
                            web_url=item_detail)
                        if obj_pergikuliner.count() == 0:
                            obj_save = WebScrapPergiKuliner(
                                web_url=item_detail,
                                brand="{}".format(brand),
                                branch="{}".format(branch_2),
                                location="{}".format(data_location),
                                building="{}".format(arr_building),
                                phone_n_open="{}".format(arr_phone_n_open),
                                price="{}".format(price),
                                info_list_out="{}".format(info_list_out),
                                arr_facility_checked="{}".format(arr_facility_checked),
                                arr_facility_unchecked="{}".format(arr_facility_unchecked),
                                arr_ratings="{}".format(arr_ratings))
                            obj_save.save()
                        else:
                            obj_save = obj_pergikuliner[0]
                            obj_save.brand="{}".format(brand)
                            obj_save.branch="{}".format(branch_2)
                            obj_save.location="{}".format(data_location)
                            obj_save.building="{}".format(arr_building)
                            obj_save.phone_n_open="{}".format(arr_phone_n_open)
                            obj_save.price="{}".format(price)
                            obj_save.info_list_out="{}".format(info_list_out)
                            obj_save.arr_facility_checked="{}".format(
                                arr_facility_checked)
                            obj_save.arr_facility_unchecked="{}".format(
                                arr_facility_unchecked)
                            obj_save.arr_ratings = "{}".format(arr_ratings)
                            obj_save.save()

                        #save all images
                        for item_key in dict_images.keys():
                            for image_url_item in dict_images[item_key]:
                                obj_image_ = WebScrapPergiKulinerImage(
                                    web_pergikuliner=obj_save,
                                    image_url="{}".format(
                                        image_url_item),
                                    image_category="{}".format(
                                        item_key)
                                )
                                obj_image_.save()

                        #save all reviews
                        for item_review in list_reviews:
                            obj_pergikuliner_rnr = WebScrapPergiKulinerRnR.objects.filter(
                                web_pergikuliner=obj_save, rnr_url=item_review['rnr_url'])
                            if obj_pergikuliner_rnr.count() == 0:
                                obj_pergikuliner_rnr_ = WebScrapPergiKulinerRnR(
                                    web_pergikuliner=obj_save,
                                    rnr_url="{}".format(
                                        item_review['rnr_url']),
                                    review_title_str="{}".format(
                                        item_review['review_title_str']),
                                    review_title_by="{}".format(
                                        item_review['review_title_by']),
                                    reviewer_pic="{}".format(
                                        item_review['reviewer_pic']),
                                    reviewer_name="{}".format(
                                        item_review['reviewer_name']),
                                    rating_total="{}".format(
                                        item_review['rating_total']),
                                    review_msg="{}".format(
                                        item_review['review_msg']),
                                    content_bottom_data="{}".format(
                                        item_review['content_bottom_data']),
                                )
                                obj_pergikuliner_rnr_.save()
                            else:
                                obj_pergikuliner_rnr_ = obj_pergikuliner_rnr[0]

                            #item_review['rating_image']
                            for item_rnr_image in item_review['rating_image']:
                                obj_rnr_image = WebScrapPergiKulinerRnRImage.objects.filter(
                                    web_pergikuliner_rnr=obj_pergikuliner_rnr_, image_url=item_rnr_image)
                                if obj_rnr_image.count() == 0:
                                    obj_rnr_image_ = WebScrapPergiKulinerRnRImage(
                                        web_pergikuliner_rnr=obj_pergikuliner_rnr_,
                                        image_url="{}".format(
                                            item_rnr_image))
                                    obj_rnr_image_.save()

                        # update done status
                        item_detail.done = True
                        item_detail.save()
                        print("[{}] item_detail: {} SAVED and DONE".format(
                            idx_row, item_detail))

                except Exception as ex:
                    print("ERR Exception : {}".format(str(ex)))
                finally:
                    print("{} OK".format(item_detail))
                
                #break for loop
                # break

        print("END Scrapping Detail Page")


def run_group():
    # 'https://pergikuliner.com/restoran/jakarta/?page=1'
    # url_master = ['restoran', ['jakarta', 'depok', 'bogor', 'tangerang', 'bekasi', 'bandung', 'surabaya',
    #     'jakarta/jakarta-utara', 'jakarta/jakarta-barat', 'jakarta/jakarta-timur', 
    #     'jakarta/jakarta-selatan', 'jakarta/jakarta-pusat','tangerang/tangerang', 'tangerang/serpong','tangerang/bsd']
    #               ]
    url_master = ['jakarta/jakarta-selatan/grand-wijaya-center',
                  'jakarta/jakarta-barat/central-park',
                  'jakarta/jakarta-utara/food-centrum',
                  'jakarta/jakarta-pusat/menteng-central',
                  'jakarta/jakarta-utara/pasar-moi',
                  'jakarta/jakarta-selatan/pasar-mayestik',
                  'jakarta/jakarta-selatan/pasar-minggu',
                  'jakarta/jakarta-barat/avenue-house',
                  'jakarta/jakarta-pusat/altitude-the-plaza',
                  'jakarta/jakarta-timur/aeon-mall-jakarta-garden-city',
                  'jakarta/jakarta-pusat/grand-indonesia',
                  'jakarta/jakarta-selatan/md-place',
                  'jakarta/jakarta-timur/ciracas',
                  'jakarta/jakarta-barat/arkz-food-garage',
                  'jakarta/jakarta-selatan/karet-kuningan',
                  'jakarta/jakarta-selatan/pacific-place',
                  'jakarta/jakarta-selatan/bursa-efek-jakarta',
                  'jakarta/jakarta-barat/jawara-food-court',
                  'jakarta/jakarta-selatan/hang-lekir',
                  'jakarta/jakarta-timur/cakung',
                  'jakarta/jakarta-timur/cawang',
                  'jakarta/jakarta-barat/gajah-mada',
                  'jakarta/jakarta-pusat/gajah-mada-plaza',
                  'jakarta/jakarta-pusat/sawah-besar',
                  'jakarta/jakarta-pusat/tanah-abang',
                  'jakarta/jakarta-selatan/radio-dalam',
                  'jakarta/jakarta-barat/tanjung-duren',
                  'jakarta/jakarta-utara/tanjung-priok',
                  'jakarta/jakarta-selatan/lebak-bulus',
                  'jakarta/jakarta-selatan/mall-ambassador',
                  'jakarta/jakarta-barat/hayam-wuruk',
                  'jakarta/jakarta-barat/taman-fatahillah',
                  'jakarta/jakarta-utara/taman-impian-jaya-ancol',
                  'jakarta/jakarta-pusat/taman-ismail-marzuki',
                  'jakarta/jakarta-timur/arion-mall',
                  'jakarta/jakarta-utara/kelapa-gading',
                  'jakarta/jakarta-timur/kampung-melayu',
                  'jakarta/jakarta-selatan/mampang',
                  'jakarta/jakarta-selatan/pelaspas-dharmawangsa',
                  'jakarta/jakarta-timur/buaran-plaza',
                  'jakarta/jakarta-selatan/darmawangsa-square',
                  'jakarta/jakarta-selatan/kalibata-city-square',
                  'jakarta/jakarta-barat/lokasari-square',
                  'jakarta/jakarta-utara/mangga-dua-square',
                  'jakarta/jakarta-timur/tamini-square',
                  'jakarta/jakarta-utara/harco-mangga-dua',
                  'jakarta/jakarta-selatan/plaza-festival',
                  'jakarta/jakarta-pusat/sampoerna-strategic-square',
                  'jakarta/jakarta-barat/komplek-taman-duta-mas',
                  'jakarta/jakarta-barat/ruko-tanjung-duren-square',
                  'jakarta/jakarta-utara/pasar-muara-karang',
                  'jakarta/jakarta-pusat/metro-atom-pasar-baru',
                  'jakarta/jakarta-pusat/metro-atom-plaza',
                  'jakarta/jakarta-pusat/plaza-atrium',
                  'jakarta/jakarta-selatan/rasuna-garden-foodstreet',
                  'jakarta/jakarta-timur/bassura-city',
                  'jakarta/jakarta-utara/pik-avenue',
                  'jakarta/jakarta-selatan/lotte-shopping-avenue',
                  'jakarta/jakarta-barat/ruko-sixth-avenue',
                  'jakarta/jakarta-barat/px-pavilion',
                  'jakarta/jakarta-utara/baywalk-mall',
                  'jakarta/jakarta-pusat/kawasan-kuliner-bsm',
                  'jakarta/jakarta-pusat/maxx-kitchen',
                  'jakarta/jakarta-pusat/mega-glodok-kemayoran',
                  'jakarta/jakarta-timur/pondok-bambu',
                  'jakarta/jakarta-selatan/pondok-indah',
                  'jakarta/jakarta-selatan/pondok-indah-mall',
                  'jakarta/jakarta-timur/pondok-kelapa',
                  'jakarta/jakarta-selatan/kebayoran-baru',
                  'jakarta/jakarta-selatan/kebayoran-lama',
                  'jakarta/jakarta-pusat/kemayoran',
                  'jakarta/jakarta-selatan/melawai'
                  ]
    # create scrap group
    for location in url_master:
        print("location: {}".format(location))
        url_scrap_list = "{}/{}/{}/?page={}".format(
            DOMAIN_NAME_TO_SCRAP, 'restoran', location, "1")
        print("url_scrap_list: {}".format(url_scrap_list))

        WebScrapping(url_scrap_list, location).listing_location()


def run_detail():
    result = WebScrapping(1, 2).get_listing()
    print("result: {}".format(result))


def run_scraping_detail():
    WebScrapping(3, 4, 1).scrap_detail_page()


def run_scrap_scripts():
    WebScrapping(5, 6, 1).scrap_scripts()


if __name__ == "__main__":
    run_scraping_detail()
