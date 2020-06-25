import json
import logging

from django.views import View
from halalmas.api.helper.response_api import ResponseAPI
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from halalmas.crm import (tmptlogin_required,
                              tmptlogin_required_group,
                              tmptlogin_required_multigroup)

from halalmas.server.objects.companies.models import Company
from halalmas.server.objects.buildings.models import Location

logger = logging.getLogger(__name__)

# class LocationSerializers(GeoFeatureModelSerializer):
#     id = serializers.IntegerField()    
#     name = serializers.CharField()
#     latitude = serializers.FloatField()
#     longitude = serializers.FloatField()

#     class Meta:
#         model = Location
#         geo_field = "coord_osm"
#         fields = ('id', 'name', 'latitude', 'longitude')

class LocationSerializers(serializers.Serializer):
    id = serializers.IntegerField()    
    name = serializers.CharField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()

class CompanySerializers(serializers.Serializer):
    id = serializers.IntegerField()
    organization_type = serializers.CharField()
    group_type = serializers.IntegerField()
    name = serializers.CharField()
    npwp = serializers.CharField()
    address = serializers.CharField()
    post_code = serializers.CharField()
    phone = serializers.CharField()
    siup = serializers.CharField()
    owner_name = serializers.CharField()
    location = LocationSerializers()
    kelurahan = serializers.CharField()
    kecamatan = serializers.CharField()
    kabupaten = serializers.CharField()
    propinsi = serializers.CharField()
    unit = serializers.CharField()
    floor = serializers.CharField()


class CompanyCreateView(View, ResponseAPI):
    location = Location.objects

    @method_decorator(csrf_protect)        
    def post(self, request):
        body = json.loads(request.body.decode('utf-8'))
        
        try:
            # print(f'create company-body #1: {body}')
            location = body.get('location', None)

            if 'location' in body: del body['location']

            # print(f'create company-body #2: {body}')
            # print(f'create company-location : {location}')

            location_obj = self.create_location(location, body['name'])
            if location_obj:
                body['location'] = location_obj
            
            # print(f'create company-body #3: {body}')
            add_company = Company.objects.create(**body)

        except Exception as e:
            return self.resp(msg=f'error create company ==> {e}')

        rs = CompanySerializers(add_company).data

        return self.resp(status=True, data=rs)
    
    def create_location(self, location, company_name):
        # print("create_location HERE")
        if location['name'] == '' or location['name'] == None:
            location['name'] = "{}-location".format(company_name)

        rs = self.location.create(
            name=location['name'],
            latitude=None,
            longitude=None,
            coord_google=None,
            coord_osm=None,
        )
        
        print("rs save #1: {}".format(rs))
        if location['lat'] != 0 and location['lon'] != 0:
            print("rs update #2: {}".format(rs))
            rs.latitude=location['lat']
            rs.longitude=location['lon']
            
        print("rs location save RETURN")
        rs.save()
        return rs

class CompanyDetailView(View, ResponseAPI):

    @method_decorator(csrf_protect)        	
    def get(self, request, pk):
        
        try:
            qs = Company.objects.filter(id=pk).first()
        except Exception as e:
            return self.resp(msg=f'error get company ==> {e}')

        if qs is None:
            return self.resp(msg=f'company is null for this id ==> {pk}')

        rs = CompanySerializers(qs).data
        
        return self.resp(status=True, data=rs)


class CompanyUpdateView(View, ResponseAPI):
    location = Location.objects

    @method_decorator(csrf_protect)
    def post(self, request, pk):
        body = json.loads(request.body.decode('utf-8'))
        
        qs = Company.objects.filter(id=pk)

        if qs.count() == 0:
            return self.resp(msg=f'company is null for this id ==> {pk}')

        try:
            # print(f'update company-body #1: {body}')
            location = body.get('location', None)

            if 'location' in body: del body['location']

            # print(f'update company-body #2: {body}')
            # print(f'update company-location : {location}')

            location_obj = self.update_location(location, body['name'])
            if location_obj:
                body['location'] = location_obj
            
            # print(f'update company-body #3: {body}')
            company = qs.update(**body)

        except Exception as e:
            return self.resp(msg=f'error update company ==> {e}')

        rs = qs.first()
        rs = CompanySerializers(rs).data

        return self.resp(status=True, data=rs)
    
    def update_location(self, location, company_name):
        # print(f"update_location: {location}")
        logger.info(f"update_location: {location}")
        
        loc_obj = None
        create_flag = False
        if 'id' in location: 
            if location['id'] is None:
                create_flag = True
            else:    
                get_loc_by_id = self.location.filter(id=location['id'])
                if get_loc_by_id.count() == 0:
                    create_flag = True
                else:
                    # print(f'update #0: {get_loc_by_id}')
                    loc_obj = get_loc_by_id[0]
        else:
            create_flag = True
        
        if create_flag == True:
            # print(f'HERE CREATE True {loc_obj}')
            loc_obj = self.create_location(location, company_name)
            loc_obj.refresh_from_db()

        # print(f'update #1: {loc_obj}')
        if location['lat'] != 0 and location['lon'] != 0:
            # print("update #2")
            loc_obj.name=location['name']
            loc_obj.latitude=location['lat']
            loc_obj.longitude=location['lon']
        else:  
            # print("update #3")
            loc_obj.name=location['name']
            loc_obj.latitude=None
            loc_obj.longitude=None
            coord_google=None
            loc_obj.coord_osm=None
        
        loc_obj.save()
        # print("update location finished")
        logger.info(f"update location finished {loc_obj}")
        return loc_obj
    
    def create_location(self, location, company_name):
        # print("create_location HERE")
        if location['name'] == '' or location['name'] == None:
            location['name'] = "{}-location".format(company_name)

        rs = self.location.create(
            name=location['name'],
            latitude=None,
            longitude=None,
            coord_google=None,
            coord_osm=None,
        )
        
        print("rs save #1: {}".format(rs))
        if location['lat'] != 0 and location['lon'] != 0:
            # print("rs update #2: {}".format(rs))
            rs.latitude=location['lat']
            rs.longitude=location['lon']
            
        # print("rs location save RETURN")
        rs.save()
        return rs

        
        