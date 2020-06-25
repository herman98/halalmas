import boto
import requests
import io, os

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

from django.conf import settings
from boto.s3.key import Key

"""
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
S3_MEDIA_BUCKET = os.getenv('S3_BUCKET_NAME')
S3_BUCKET_GALLERY = os.getenv('S3_BUCKET_GALLERY')

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_S3_REGION_NAME = os.getenv('AWS_S3_DEFAULT_REGION')

SES_ACCESS_KEY = os.getenv('SES_ACCESS_KEY')
SES_SECRET_KEY = os.getenv('SES_SECRET_KEY')
SES_REGION = os.getenv('SES_REGION')


# AWS - S3
export S3_BUCKET_NAME="halalmas"
export S3_BUCKET_GALLERY="halalmas"
export COMPRESS_IMAGE_FORMAT="JPEG"

# AWS - IM
export AWS_ACCESS_KEY_ID="AKIAIJ5ZERDP33U5HSSQ"
export AWS_SECRET_ACCESS_KEY="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"
export AWS_S3_DEFAULT_REGION="ap-southeast-1"

# AWS - SES
export SES_ACCESS_KEY="AKIAJKAEUT5TBYUZ7GDA"
export SES_SECRET_KEY="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"
export SES_REGION="us-west-2"

"""


class UploadToS3(object):
    def __init__(self):
        self.conn = boto.connect_s3(settings.AWS_ACCESS_KEY_ID,
                                    settings.AWS_SECRET_ACCESS_KEY)
        self.bucket_name = settings.S3_MEDIA_BUCKET
        self.bucket = self.conn.get_bucket(self.bucket_name)
        self.key_bucket = Key(self.bucket)
        self.AWS_S3_REGION_NAME = settings.AWS_S3_REGION_NAME
        self.file_ext = 'JPG'

        # init method
        self.set_s3_http_addr()

    def upload_from_url(self, url, dir_path):
        # try:
        filename_here = url.split('/')[-1]
        if filename_here:
            self.file_ext = filename_here.split(".")[1]
        self.key_bucket.key = "{}/{}".format(dir_path, filename_here
                                                )
        print(f'self.key_bucket.key: {self.key_bucket.key}')

        file_object = urlopen(url)           # 'Like' a file object
        fp = io.BytesIO(file_object.read())   # Wrap object
        self.key_bucket.set_contents_from_file(fp)
        self.key_bucket.make_public()

        # https://halalmas.s3-ap-southeast-1.amazonaws.com/server/media/branch/1/picture-1484192699.JPG
        return "https://{}.s3-{}.amazonaws.com{}".format(
            self.bucket_name,
            self.AWS_S3_REGION_NAME,
            self.key_bucket.key)
        # except Exception as e:
        #     print(f'ERR exception: {e}')
        #     return None

    def upload_image_stream_file(self, img_source, filename_full_path):
        try:
            s3_checker = "https://{}.s3.{}.amazonaws.com".format(
                self.bucket_name,
                self.AWS_S3_REGION_NAME)
            print(f's3_checker:{s3_checker}')
            if (filename_full_path.find(s3_checker)>-1):
                self.key_bucket.key = filename_full_path.replace(s3_checker,'')
            else:
                self.key_bucket.key = filename_full_path
            print(f'self.key_bucket.key: {self.key_bucket.key}')

            img_source.seek(0)
            self.key_bucket.set_contents_from_file(img_source)
            # self.key_bucket.set_contents_from_string(fp.getvalue(), headers={
            #     "Content-Type": "image/jpg"})
            self.key_bucket.make_public()

            # https://halalmas.s3-ap-southeast-1.amazonaws.com/server/media/branch/1/picture-1484192699.JPG
            # dir_s3 = self.s3_http_addr
            # print(f'dir_s3: {dir_s3}')
            # return "{}{}".format(dir_s3, self.key_bucket.key)
            return "https://{}.s3-{}.amazonaws.com{}".format(
                self.bucket_name,
                self.AWS_S3_REGION_NAME,
                self.key_bucket.key)
        except Exception as e:
            print(f'ERR exception: {e}')
            return None

    def save_into_local(self, image_stream, temporarylocation):
        image_stream.seek(0)
        with open(temporarylocation,'wb') as out: ## Open temporary file as bytes
            out.write(image_stream.read())                ## Read bytes into file

        ## Do stuff with module/file
        # os.remove(temporarylocation)

    def upload_from_url_list(self, url_list, dir_path):
        for item_url in url_list:
            self.upload_from_url(item_url, dir_path)
        return "success"

    def s3_http_addr_custom(self, format_1=None):
        if format_1:
            self.s3_http_addr = "https://{}.s3.amazonaws.com".format(
                self.bucket_name)
        else:
            self.s3_http_addr = "https://{}.s3-{}.amazonaws.com".format(
                self.bucket_name,
                self.AWS_S3_REGION_NAME)
        return self.s3_http_addr

    def set_s3_http_addr(self, http_addr=None):
        if http_addr:
            self.s3_http_addr = http_addr
        else:
            self.s3_http_addr = "https://{}.s3-{}.amazonaws.com".format(
                self.bucket_name,
                self.AWS_S3_REGION_NAME)
        return self.s3_http_addr

    @property
    def get_s3_http_addr(self):
        return self.s3_http_addr

    @property
    def get_file_ext(self):
        return "{}".format(self.file_ext)

    def close_connection(self):
        self.conn.close()


def upload(url):
    # try:
    conn = boto.connect_s3(settings.AWS_ACCESS_KEY_ID,
                           settings.AWS_SECRET_ACCESS_KEY)
    bucket_name = settings.S3_MEDIA_BUCKET
    bucket = conn.get_bucket(bucket_name)
    k = Key(bucket)
    # In my situation, ids at the end are unique
    # k.key = url.split('/')[::-1][0]
    # k.key = "{}/{}".format('/server/media/branch/1/', url.split('/')[-1])
    k.key = "{}/{}".format('rating-review/11215/img/', url.split('/')[-1])
    print(f'key: {k.key}')

    file_object = urlopen(url)           # 'Like' a file object
    fp = io.BytesIO(file_object.read())   # Wrap object
    k.set_contents_from_file(fp)
    k.make_public()
    return "Success"

    # except Exception as e:
    #     print(f'ERR: {e}')
    #     return e


# def upload_2():
#     # Uses the creds in ~/.aws/credentials
#     s3 = boto3.resource('s3')
#     bucket_name_to_upload_image_to = 'photos'
#     s3_image_filename = 'test_s3_image.png'
#     internet_image_url = 'https://docs.python.org/3.7/_static/py.png'

#     # Do this as a quick and easy check to make sure your S3 access is OK
#     for bucket in s3.buckets.all():
#         if bucket.name == bucket_name_to_upload_image_to:
#             print('Good to go. Found the bucket to upload the image into.')
#             good_to_go = True

#     if not good_to_go:
#         print('Not seeing your s3 bucket, might want to double check permissions in IAM')

#     # Given an Internet-accessible URL, download the image and upload it to S3,
#     # without needing to persist the image to disk locally
#     req_for_image = requests.get(internet_image_url, stream=True)
#     file_object_from_req = req_for_image.raw
#     req_data = file_object_from_req.read()

#     # Do the actual upload to s3
#     s3.Bucket(bucket_name_to_upload_image_to).put_object(
#         Key=s3_image_filename, Body=req_data)


def test_one():
    # url_here = 'https://assets-pergikuliner.com/uploads/image/picture/433380/picture-1484192699.JPG'
    url_here = 'https://halalmas.s3.ap-southeast-1.amazonaws.com/rating-review/11215/10_1568456375133_20190914_162633.jpg'
    upload(url_here)
