import requests
import io

from django.conf import settings
from PIL import Image

from .aws_s3_upload import UploadToS3
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

# from tempatdotcom.core.lib.image_compress import CompressImage

Image.LOAD_TRUNCATED_IMAGES = True
COMPRESS_IMAGE_FORMAT = getattr(
    settings, "COMPRESS_IMAGE_FORMAT", 'jpg')

XWORK_IMG_SIZE = {
    'lg': (750, 499),
    'md': (680, 453),
    'sm': (360, 225),
    'thumb': (112, 70),
}
SAVED_IMAGE_PATH = 'img'
MIN_FILE_SIZE = 100  # below this limit will not be compressed
IMAGE_COMPRESS_QUALITY = 90
CELERY_RUNNING = getattr(settings, 'CELERY_RUNNING', False)

class BranchImageCompressor(object):
    def __init__(self, *args, **kwargs):
        self.file_stream = None
        self.filename_src = None
        self.s3_path_src = None
        self.s3_dest_path = None
        # self.open_class_s3()

    def open_class_s3(self):
        self.clsUploadToS3 = UploadToS3()

    def get_img_from_url(self, url_in):
        self.filename_src = url_in.split('/')[-1]
        # check if '?'
        aa = self.filename_src.split('?')
        if len(aa) >= 2:
            self.filename_src = aa[0]
        if self.filename_src:
            self.file_ext = self.filename_src.split(".")[1]
            to_replace = self.clsUploadToS3.get_s3_http_addr
            # print(f'to_replace: {to_replace}')
            to_replace_1 = self.clsUploadToS3.s3_http_addr_custom(1)
            # print(f'to_replace_1: {to_replace_1}')
            self.s3_path_src = url_in.replace(
                self.filename_src, '').replace(to_replace, '').replace(to_replace_1, '')
            # check if '?'
            bb = self.s3_path_src.split('?')
            if len(bb) >= 2:
                self.s3_path_src = bb[0]

        print(f'self.filename_src: {self.filename_src}')
        print(f'self.s3_path_src: {self.s3_path_src}')

        file_object = urlopen(url_in)           # 'Like' a file object
        fp_stream = io.BytesIO(file_object.read())   # Wrap object
        self.file_stream = Image.open(fp_stream)

        # Bug PIL: https: // bugs.launchpad.net/openobject-server/+bug/1091703
        if self.file_stream.mode == "CMYK":
            self.file_stream = self.file_stream.convert("RGB")
        # print(f'self.file_stream: {self.file_stream}')
        return self.file_stream.size

    def get_class_s3(self):
        return self.clsUploadToS3

    @property
    def get_file_stream(self):
        return self.file_stream

    def compress_and_upload_to_s3(self, image_file=None):
        print(f'compress_and_upload_to_s3')

        default_path = SAVED_IMAGE_PATH
        dir_out = '{}{}'.format(self.s3_path_src, default_path)

        if image_file:
            file_img_here = image_file
        else:
            file_img_here = self.file_stream

        print(f'file_img_here: {file_img_here}')

        compress_to = ['ori', 'lg', 'md', 'sm', 'thumb']
        for tag in compress_to:
            new_filename = '{}_{}'.format(tag, self.filename_src)
            full_path = "{}/{}".format(dir_out, new_filename)
            # check if '?'
            aa = full_path.split('?')
            if len(aa) >= 2:
                full_path = aa[0]
            print(f'full_path: {full_path}')
            quality = 100 if tag == "ori" else IMAGE_COMPRESS_QUALITY
            file_img_here.quality = quality
            file_img_here.thumbnail(
                XWORK_IMG_SIZE.get(tag, file_img_here.size), Image.ANTIALIAS)
            try:
                output = io.BytesIO()
                file_img_here.save(
                    output, 'JPEG')

                # upload to s3
                print('===============',full_path)
                self.clsUploadToS3.upload_image_stream_file(output, full_path)
                # remark if Productions : save file into local folder
                # self.clsUploadToS3.save_into_local(output, f'/home/herman3g/tempatdotcom/aws/s3/{new_filename}')

            except Exception as e:
                print("ERR: {}".format(e))

            #remark after test
            # break

        return self.filename_src, self.s3_path_src

    def close_s3_connection(self):
        self.clsUploadToS3.close_connection()


from tempatdotcom.server.tasks import compress_s3_image_from_url_task

def compress_s3_image_from_url(url_input):
    if CELERY_RUNNING:
        compress_s3_image_from_url_task.delay(url_input)
    else:
        compress_s3_image_from_url_task(url_input)

    # cls_img_compress = BranchImageCompressor()
    # cls_img_compress.open_class_s3()
    # cls_img_compress.get_img_from_url(url_input)
    # cls_img_compress.compress_and_upload_to_s3()
    # cls_img_compress.close_s3_connection()


def test_one():
    # cls_upload_tos3 = UploadToS3()
    # print(
    #     f'cls_upload_tos3.get_s3_http_addr {cls_upload_tos3.get_s3_http_addr}')

    url_input = 'https://tempatdotcom.s3-ap-southeast-1.amazonaws.com/server/media/branch/1000/picture-1450443521.jpg'
    compress_s3_image_from_url(url_input)
    # print(f'{get_file_stream} {cls_img_compress.get_file_stream}')
