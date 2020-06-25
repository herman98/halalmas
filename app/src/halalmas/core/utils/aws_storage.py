from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
from django.core.files.storage import Storage

AWS_PUBLIC_MEDIA_LOCATION = getattr(
    settings, 'AWS_PUBLIC_MEDIA_LOCATION', 'public')
AWS_PRIVATE_MEDIA_LOCATION = getattr(
    settings, 'AWS_PRIVATE_MEDIA_LOCATION', 'private')

# class StaticStorage(S3Boto3Storage):
#     location = settings.AWS_STATIC_LOCATION

# class MediaStorage(S3Boto3Storage):
#     location = 'media'
# file_overwrite = False


class S3_MediaMixins(object):
    def __init__(self):
        self.location = AWS_PUBLIC_MEDIA_LOCATION
        self.location_here = None

    def set_path(self, specific_path=None, extension=None):
        self.location_here = None
        if specific_path:
            if extension:
                self.location_here = "{}/{}".format(
                    self.location, specific_path)
            else:
                self.location_here = specific_path
        return self.location_here


class PublicMediaStorage(S3Boto3Storage):
    location = AWS_PUBLIC_MEDIA_LOCATION
    file_overwrite = False


class PrivateMediaStorage(S3Boto3Storage):
    location = AWS_PRIVATE_MEDIA_LOCATION
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False


class AWSTempatStorage(Storage):
    def __init__(self, *args, **kwargs):
        print("PublicMediaStorage fx:init")
        """
        The init method MUST NOT require any args to be set.
        The Storage instance should be able to be instantiated
        without passing in any args. You could use kwargs with 
        default values though.

        If you want to read settings you should read them from 
        django.conf.settings.
        """
        super().__init__(*args, **kwargs)

    def _open(self, name, mode='rb'):
        print("PublicMediaStorage fx:_open")
        """Required method that implements how files are opened/read"""
        raise NotImplementedError("Method not implemented yet.")

    def _save(self, name, content):
        print("PublicMediaStorage fx:_save")
        """Required method that implements how files are save/written"""
        raise NotImplementedError("Method not implemented yet.")

    def delete(self, name):
        print("PublicMediaStorage fx:delete")
        """Optional method that delete file at filepath"""
        raise NotImplementedError("Method not implemented yet.")

    def exists(self, name):
        print("PublicMediaStorage fx:exists")
        """Optional method that return if file exists"""
        raise NotImplementedError("Method not implemented yet.")

    def listdir(self, path):
        print("PublicMediaStorage fx:listdir")
        """Optional method that return list of files and dirs in path"""
        raise NotImplementedError("Method not implemented yet.")

    def size(self, name):
        print("PublicMediaStorage fx:size")
        """Optional method that return filesize of file"""
        raise NotImplementedError("Method not implemented yet.")

    def url(self, name):
        print("PublicMediaStorage fx:url")
        """Optional method that return the public URL of a file"""
        raise NotImplementedError("Method not implemented yet.")

    def path(self, name):
        print("PublicMediaStorage fx:path")
        """Optional method that return absolute path of file"""
        raise NotImplementedError("Method not implemented yet.")
