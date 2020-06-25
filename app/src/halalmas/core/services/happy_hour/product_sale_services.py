from __future__ import unicode_literals

import operator
import datetime
import logging

from functools import reduce

from django.db.models import Q
from django.conf import settings

from tempatdotcom.server.hosts.happy_hour.models import BranchSaleProduct, Branch
from tempatdotcom.core.utils.aws_s3_upload_service import S3_Services
from tempatdotcom.crm.objects.merchant.happy_hours.serializers import ProductSaleDetailSerializers, ProductSaleSerializers

AWS_PUBLIC_MEDIA_LOCATION = getattr(
    settings, 'AWS_PUBLIC_MEDIA_LOCATION', 'server/media_dev/public')

class ProductSaleServices():
    qs = BranchSaleProduct
    
    def create_product_service(self, request):
        body = request.POST

        branch_id = body.get('branch_id', None)
        get_branch = Branch.objects.filter(id=branch_id).first()

        files = request.FILES.get('picture_file', None)
        if files is None:
            file_path = None
            url = None
            file_name = None
        else:
            file_path = f"{AWS_PUBLIC_MEDIA_LOCATION}/branch/{branch_id}/products/{files.name}" 
            url = f'https://tempatdotcom.s3-ap-southeast-1.amazonaws.com/{file_path}'
            file_name = files.name

        # print(f'branch_id: {branch_id}')
        # print(f'get_branch ID: {get_branch.id}')
        # print(f'url: {url}')
        if files:
            upload = S3_Services()
            upload.file_path = file_path
            upload.filex = files
            upload.upload_boto3()

        create_product = self.qs( #.objects.create
            title_name=body.get('title_name', None),
            sub_title_name=body.get('sub_title_name', None),
            normal_rate=body.get('normal_rate', None),
            discount_rate=body.get('discount_rate', None),
            is_strike_out=True if body.get('is_strike_out', False) == 'true' else False ,
            min_purchase=body.get('min_purchase', None),
            max_purchase=body.get('max_purchase', None),
            picture_url=url,
            picture_file=file_name,
            branch=get_branch,
            is_open_price=True if body.get('is_open_price', False) == 'true' else False
        )
        create_product.save()
        if files:
            try:
                from tempatdotcom.core.utils.branch_img_compress import compress_s3_image_from_url
                compress_s3_image_from_url(url)
                create_product.url = url
                create_product.save()
            except Exception as e:
                print(e)

        return create_product

    def list_product_service(self, query, branch_id):

        if isinstance(query, (str, bytes)) and query:
            self.qs = self.qs.objects.filter(reduce(operator.or_,
                [
                    Q(**{('%s__icontains' % 'title_name'): query}),
                    Q(**{('%s__icontains' % 'sub_title_name'): query}),
                ]
            ), branch_id=branch_id, delstatus=False).order_by('-cdate')
        else:
            self.qs = self.qs.objects.filter(branch_id=branch_id, delstatus=False).order_by('-cdate')

        self.qs = list(map(lambda x:
            ProductSaleSerializers(x).data,
            self.qs
        ))
        return self.qs

    def update_product_service(self, request, product_id):
        product_sale = self.qs.objects.filter(id=product_id, delstatus=False)       
        body = request.POST
        branch_id = body.get('branch_id', None)
        get_branch = Branch.objects.filter(id=branch_id).first()

        files = request.FILES.get('picture_file', None)
        if files is None:
            url = None
            file_name = None
        else:
            file_path = f"{AWS_PUBLIC_MEDIA_LOCATION}/branch/{branch_id}/products/{files.name}" 
            url = f'https://tempatdotcom.s3-ap-southeast-1.amazonaws.com/{file_path}'
            file_name = files.name

        if files:
            upload = S3_Services()
            upload.file_path = file_path
            upload.filex = files
            upload.upload_boto3()

        payload = {  
            'title_name': body.get('title_name', None),
            'sub_title_name': body.get('sub_title_name', None),
            'normal_rate': body.get('normal_rate', None),
            'discount_rate': body.get('discount_rate', None),
            'is_strike_out': True if body.get('is_strike_out', False) == 'true' else False ,
            'min_purchase': body.get('min_purchase', None),
            'max_purchase': body.get('max_purchase', None),
            'branch': get_branch,
            'is_open_price': True if body.get('is_open_price', False) == 'true' else False
        }

        if files:
            payload['picture_url'] = url
            payload['picture_file'] = file_name

        update_product = product_sale.update(**payload)
        
        if files: 
            try:
                from tempatdotcom.core.utils.branch_img_compress import compress_s3_image_from_url
                compress_s3_image_from_url(payload['picture_url'])
            except Exception as e:
                print(e)

    def delete_product_service(self, product_id):
        product_sale = self.qs.objects.filter(id=product_id, delstatus=False).first()
        
        product_sale.delstatus = True
        product_sale.save()

        return product_id

    def detail_product_service(self, product_id):
        product_sale = self.qs.objects.filter(id=product_id, delstatus=False).first()
        return ProductSaleDetailSerializers(product_sale).data