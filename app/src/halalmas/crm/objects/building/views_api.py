import json
import logging
import operator

from functools import reduce

from django.db.models import Q
from django.contrib.gis.geos import Point
from django.views import View
from halalmas.api.helper.response_api import ResponseAPI
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.conf import settings

# from halalmas.core.utils.branch_img_compress import compress_s3_image_from_url
from halalmas.server.objects.indonesia import utils as iu
from halalmas.crm import (tmptlogin_required,
                              tmptlogin_required_group,
                              tmptlogin_required_multigroup)

from halalmas.server.objects.buildings.models import (
    Building, Location, BuildingCategory )

from .serializers import BuildingSerializers, BuildingCategorySerializers

logger = logging.getLogger(__name__)


def validation_body(data_body):
    if 'xwork_pk' in data_body:
        data_body['xwork_pk'] = data_body['xwork_pk'] if data_body['xwork_pk']!='' else None
    
    if 'operational_hour_per_day' in data_body:
        data_body['operational_hour_per_day'] = data_body['operational_hour_per_day'] if data_body['operational_hour_per_day']!='' else 0
    
    if 'operational_day_per_week' in data_body:
        data_body['operational_day_per_week'] = data_body['operational_day_per_week'] if data_body['operational_day_per_week']!='' else 0
    
    if 'operational_day_per_month' in data_body:
        data_body['operational_day_per_month'] = data_body['operational_day_per_month'] if data_body['operational_day_per_month']!='' else 0
    
    if 'building_category_id' in data_body:
        data_body['building_category_id'] = data_body['building_category_id'] if data_body['building_category_id'] not in ['', 0]  else None
    
    return data_body


class BuildingCategoryView(View, ResponseAPI):
    qs = BuildingCategory
    def get(self, request):
        query = request.GET.get('query', None)

        if isinstance(query, (str, bytes)) and query:
            # print('BuildingCategoryView Filter HERE')
            self.qs = self.qs.objects.filter(reduce(operator.or_,
                [
                    Q(**{('%s__icontains' % 'name'): query}),
                ]
            ), delstatus=False)[:10]
        else:
            # print('BuildingCategoryView Filter ELSE')
            self.qs = self.qs.objects.filter(delstatus=False)[:10]

        self.qs = list(map(lambda x:
            BuildingCategorySerializers(x).data,
            self.qs
        ))
        return self.resp(status=True, data=self.qs)

class BuildingCreateView(View, ResponseAPI):
    
    @method_decorator(csrf_protect)
    def post(self, request):
        body = json.loads(request.body.decode('utf-8'))
        
        try:
            print(f'update building-body #3: {body}')
            # validation
            # if 'xwork_pk' in body:
            #     body['xwork_pk'] = body['xwork_pk'] if body['xwork_pk']!='' else None
            body = validation_body(body.copy())
            
            print(f'update building-body #4: {body}')
            # add_building = Building.objects.create(**body)
            add_building = Building(**body)
            add_building.save()

        except Exception as e:
            return self.resp(msg=f'error create building ==> {e}')

        rs = BuildingSerializers(add_building).data

        return self.resp(status=True, data=rs)


class BuildingDetailView(View, ResponseAPI):

    @method_decorator(csrf_protect)        	
    def get(self, request, pk):
        
        try:
            qs = Building.objects.filter(id=pk).first()
        except Exception as e:
            return self.resp(msg=f'error get building ==> {e}')

        if qs is None:
            return self.resp(msg=f'building is null for this id ==> {pk}')

        rs = BuildingSerializers(qs).data
        # print(f'BuildingDetailView: {rs}')
        return self.resp(status=True, data=rs)


class BuildingUpdateView(View, ResponseAPI):
    @method_decorator(csrf_protect)
    def post(self, request, pk):
        body = json.loads(request.body.decode('utf-8'))
        
        qs = Building.objects.filter(id=pk)

        if qs.count() == 0:
            return self.resp(msg=f'building is null for this id ==> {pk}')

        try:
            print(f'update building-body #3: {body}')
            #validation
            # if 'xwork_pk' in body:
            #     body['xwork_pk'] = body['xwork_pk'] if body['xwork_pk']!='' else None
            body = validation_body(body.copy())
            
            print(f'update building-body #4: {body}')
            building = qs.update(**body)

        except Exception as e:
            return self.resp(msg=f'error update building ==> {e}')

        rs = qs.first()
        #execute save object method
        rs.save()

        rs = BuildingSerializers(rs).data
        return self.resp(status=True, data=rs)
    

#START API BRAND
class CRMLocationView(View, ResponseAPI):

    def get(self, request, lat, lon):
        try:
            print(f'lat {lat}, lon {lon}')
            point_search = Point(float(lon), float(lat))

            kelurahan = iu.get_kelurahan_by_coordinate(point_search)
            print(f'kelurahan {kelurahan}')
            if kelurahan:
                rs = {
                    'propinsi': kelurahan.name_1,
                    'kota': kelurahan.name_2,
                    'kecamatan': kelurahan.name_3,
                    'kelurahan': kelurahan.name_4,
                }

                return self.resp(status=True, data=rs)
        except Exception as e:
            return self.resp(f'error generate location by lat lon => {e}')      
        return self.resp(f'error no gis found from lat lon => {e}')

AWS_PUBLIC_MEDIA_LOCATION = getattr(
    settings, 'AWS_PUBLIC_MEDIA_LOCATION', 'server/media_dev/public')


from halalmas.core.utils.aws_s3_upload_service import S3_Services
class BuildingLogo(View, ResponseAPI):
    building = Building.objects

    def post(self, request, building_id):

        # print(request.FILES.dict())
        print(request.POST.dict())
        
        logo_image = request.FILES.get('logo_image', None)
        delstatus = request.POST.get('del_status', 'false')
        print(f'BuildingLogo {building_id} {logo_image} delstatus: {delstatus}' )
        
        building_obj = self.building.filter(id=building_id)
        if building_obj == 0:
            return self.resp(f'error! there is no building')
        url = None

        # try:
        if delstatus == 'true':
            print("MASUK SINI GA!")
            building_obj.update(image_url=None)
        else:
            if logo_image:
                rs = building_obj.first()
                url = self.upload_logo(logo_image, rs.id)
                rs.image_url = url
                rs.save()
        
                #compress image
                # compress_s3_image_from_url(url)
        # except Exception as e:
        #     return self.resp(f'error upload logo building, {e}')
        
        return self.resp(status=True, data=url)   

        

    def upload_logo(self, logo_image, building_pk):
        if logo_image:
            file_path = f"{AWS_PUBLIC_MEDIA_LOCATION}/building/{building_pk}/{logo_image.name}" 
            upload = S3_Services()
            upload.file_path = file_path
            upload.filex = logo_image
            upload.upload_boto3()
            url = f'https://halalmas.s3-ap-southeast-1.amazonaws.com/{file_path}'
            return url
        else:
            return None