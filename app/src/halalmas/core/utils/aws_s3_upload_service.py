import boto3

from django.conf import settings

# from botocore.exceptions import 


AWS_ACCESS_KEY_ID = getattr(
    settings, 'AWS_ACCESS_KEY_ID', None)
AWS_SECRET_ACCESS_KEY = getattr(
    settings, 'AWS_SECRET_ACCESS_KEY', None)
S3_MEDIA_BUCKET = getattr(
    settings, 'S3_MEDIA_BUCKET', 'halalmas')

class S3_Services():
    bucket_name = S3_MEDIA_BUCKET
    file_path = None
    filex = None
    
    def upload_boto3(self):
        if self.bucket_name and self.file_path and self.filex:
            session = boto3.Session(
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            )
            s3 = session.resource('s3')
            a = s3.Bucket(self.bucket_name).put_object(
                Key=self.file_path, Body=self.filex, ACL='public-read', ContentType='image/jpeg')
        else:
            raise Exception(f'params must completed before upload a image')