import logging

from rest_framework import serializers

logger = logging.getLogger(__name__)


class BuildingCategorySerializers(serializers.Serializer):
    id = serializers.IntegerField()    
    name = serializers.CharField()


class BuildingSerializers(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=125,trim_whitespace=True)
    address = serializers.CharField(max_length=1500, allow_blank=True,
        allow_null=True, trim_whitespace=True)
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    kodepos = serializers.CharField(allow_blank=True, allow_null=True)
    operational_hour_per_day = serializers.IntegerField()
    operational_day_per_week = serializers.IntegerField()
    operational_day_per_month = serializers.IntegerField()
    image_url = serializers.CharField(max_length=255, allow_blank=True, allow_null=True,
        trim_whitespace=True)
    xwork_pk = serializers.IntegerField()
    description_id = serializers.CharField(max_length=5000, allow_blank=True, allow_null=True,
        trim_whitespace=True)
    building_access_id = serializers.CharField(
        max_length=5000, allow_blank=True, allow_null=True,
        trim_whitespace=True)
    facilities_id = serializers.CharField(
        max_length=5000, allow_blank=True, allow_null=True,
        trim_whitespace=True)
    description_en = serializers.CharField(max_length=5000, allow_blank=True, allow_null=True,
        trim_whitespace=True)
    building_access_en = serializers.CharField(
        max_length=5000, allow_blank=True, allow_null=True,
        trim_whitespace=True)
    facilities_en = serializers.CharField(
        max_length=5000, allow_blank=True, allow_null=True,
        trim_whitespace=True)
    location = serializers.SerializerMethodField()

    # relation 
    building_category = BuildingCategorySerializers()

    def get_location(self, this):
        if this.kelurahan:
            return {
                'propinsi': this.kelurahan.name_1,
                'kota': this.kelurahan.name_2,
                'kecamatan': this.kelurahan.name_3,
                'kelurahan': this.kelurahan.name_4,
            }
        else:
            return {
                'propinsi': '',
                'kota': '',
                'kecamatan': '',
                'kelurahan': '',
            }