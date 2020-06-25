from __future__ import unicode_literals

import urllib.request as urllib2
import json
import urllib

import hashlib
import random
import logging

from os.path import join

from django.db import connections, transaction
from django.conf import settings

KNOWN_FILE_EXTENTIONS = ('csv', 'kml')
XWORK_ALLCAPS_NAMES = getattr(settings, 'HALALMAS_ALLCAPS_NAMES', ())

ALLCAPS_NAMES = tuple(
    set(XWORK_ALLCAPS_NAMES).union(set(KNOWN_FILE_EXTENTIONS)))

FILE_UPLOAD_TEMP_DIR = getattr(settings, 'FILE_UPLOAD_TEMP_DIR', 'uploadfile/')


def display_name(name):
    SEPARATOR = ' '
    name = name.replace('_', ' ')
    return SEPARATOR.join([
        word.upper() if word.lower() in ALLCAPS_NAMES else word.title()
        for word in name.split(SEPARATOR)])


def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def execute_sql(db_conn, sql_query):
    try:
        cursor = connections[db_conn].cursor()
        transaction.commit_unless_managed(using=db_conn)
#        print(sql_query)
        cursor.execute(sql_query)
        return dictfetchall(cursor)
    except Exception as e:
        return "Error execute_sql : ", e


def make_random_password(length=10, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'):
    "Generates a random password with the given length and given allowed_chars"
    # Note that default value of allowed_chars does not have "I" or letters
    # that look like it -- just to avoid confusion.
#         from random import choice
#         return(''.join([choice(allowed_chars) for i in range(length)]))
    return generate_hash(allowed_chars, length)


def generate_hash(string, length=10):
    # salt = hashlib.sha224(str(random.random())).hexdigest()[:5]
    salt = hashlib.sha256(str(random.getrandbits(256)).encode('utf-8')).hexdigest()[:5]
    str_data = "{}{}".format(salt, string)
    return hashlib.sha224(str(str_data).encode("utf-8")).hexdigest()[:length]


def generate_random_str(length=10):
    return make_random_password(length)
    
def upload_handle(f, generate_dir=FILE_UPLOAD_TEMP_DIR, suffix=False):
    if suffix:
        fileName = join(generate_dir, ('tmp_%s' % f.name))
    else:
        fileName = join(generate_dir, ('%s' % f.name))

    # create file from uploaded
    destination = open(fileName, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

    return fileName


def upload_handle_media(f, upload_to, f_suffix=None):
    print("settings.MEDIA_ROOT: {}".format(settings.MEDIA_ROOT))
    generate_dir = join(settings.MEDIA_ROOT, upload_to)
    if f_suffix:
        f_out = '%s_%s' % (f_suffix, f.name)
    else:
        f_out = '%s' % f.name

    fileName = join(generate_dir, f_out)

    # create file from uploaded
    destination = open(fileName, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

    return dict(file_name=fileName,
                file_url="%s/%s/%s" % (media_urls(), upload_to, f_out)
                )


class OrderList(object):
    def __init__(self):
        self.output_list = []

    def atoi(self, text):
        int_val = int(text) if text.isdigit() else text
        return int_val

    def __natural_keys(self, text):
        '''
        alist.sort(key=natural_keys) sorts in human order
        http://nedbatchelder.com/blog/200712/human_sorting.html
        (See Toothy's implementation in the comments)
        '''
        return [self.atoi(text.split('_')[1])]

    def sort(self, list_input, prefix=None):
        # remove if not pass regex
        if prefix:
            for val in list_input:
                if not val.strip().startswith(prefix):
                    list_input.remove(val)
                    self.output_list.append(val)

        _sort_res = sorted(list_input, key=self.__natural_keys)
        return _sort_res + self.output_list


# import re
# def get_from_post_rest(url, data_dict, username=None, password=None):
#     logger.info("Data sent: %s" % data_dict)
#     result = None
#     if username and password:
#         password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
#         password_mgr.add_password(None, url, username, password)
#         handler = urllib2.HTTPBasicAuthHandler(password_mgr)
#         opener = urllib2.build_opener(handler)
#         urllib2.install_opener(opener)

#         if data_dict:
#             data = data_dict
#             result = urllib.urlencode(data)
#             req = urllib2.Request(url, result)
#         else:
#             req = urllib2.Request(url)

#         response = urllib2.urlopen(req)

#         code = response.code
#         try:
#             result = json.loads(response.read())
#         except Exception as e:
#             logger.info("Err get_from_post_rest: %s" % e)
#             logger.info(response.read())
#             result = response.read()
#     else:
#         code = 1
#         try:
#             result = urllib2.urlopen(url).read()
#         except Exception as e:
#             result = e

#     return result, code
