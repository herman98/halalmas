from __future__ import unicode_literals

import operator
import datetime
import logging
import json

from functools import reduce

from django.contrib.gis.geos import Point
from django.shortcuts import render
from django.db.models import Q
from django.utils import timezone
from django.conf import settings
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from halalmas.api.helper.response_api import ResponseAPI 
from halalmas.server.objects.indonesia import utils as iu

# set decorator for login required
from halalmas.crm import (tmptlogin_required,
                              tmptlogin_required_group,
                              tmptlogin_required_multigroup)
from halalmas.server.objects.companies.models import Company

from .forms import CompanySearchForm


logger = logging.getLogger(__name__)


@tmptlogin_required
class CRMCompanyCreatePage(View):
    template_name = 'object/company/create_update.html'
    
    @method_decorator(csrf_protect)
    def get(self, request):
        # qs = Branch.objects.filter(id=branch_id, delstatus=False).first()
        return render(request, self.template_name, {
            "company": None,
            'type': 'create'
        })        

@tmptlogin_required
class CRMCompanyEditPage(View):
    template_name = 'object/company/create_update.html'

    @method_decorator(csrf_protect)
    def get(self, request, pk):
        qs = Company.objects.filter(id=pk).first()
        return render(request, self.template_name, {
            "company": qs, 
            'type': 'edit'
        })


@tmptlogin_required
# @tmptlogin_required_exclude(['finance'])
class CRMCompanyListView(ListView):
    model = Company
    paginate_by = 50  # get_conf("PAGINATION_ROW")
    template_name = 'object/company/list.html'

    def http_method_not_allowed(self, request, *args, **kwargs):
        return ListView.http_method_not_allowed(self, request, *args, **kwargs)

    def get_template_names(self):
        return ListView.get_template_names(self)

    def get_queryset(self):
        self.qs = super(CRMCompanyListView, self).get_queryset()
        self.qs = self.qs.filter(delstatus=False)

        self.err_message_here = None
        self.tgl_range = None
        self.tgl_start = None
        self.tgl_end = None
        self.status_choice = None
        self.status_order = None
        self.search_q = None
        self.status_now = None

        # print(f"self.request.GET: {self.request.GET}")
        if self.request.method == 'GET':
            self.tgl_range = self.request.GET.get('datetime_range', None)
            self.status_choice = self.request.GET.get('status_choice', None)
            self.status_order = self.request.GET.get('status_order', None)
            self.search_q = self.request.GET.get('search_q', '').strip()
            self.status_now = self.request.GET.get('status_now', None)

            if(self.status_order):
                __status_ord = self.status_order
                print(f' __status_ord: {__status_ord}')
                if __status_ord == 'latest':
                    self.qs = self.qs.order_by('-cdate', 'name')
                elif __status_ord == 'longest':
                    self.qs = self.qs.order_by('cdate')
                elif __status_ord == 'name_asc':
                    self.qs = self.qs.order_by('name')
                elif __status_ord == 'name_desc':
                    self.qs = self.qs.order_by('-name')
                else:
                    self.qs = self.qs.order_by('-cdate', 'name')
            else:
                self.qs = self.qs.order_by('-udate', 'name')

            if isinstance(self.search_q, (str, bytes)) and self.search_q:
                self.qs = self.qs.filter(reduce(operator.or_,
                        [
                            Q(**{('%s__icontains' %
                                    'name'): self.search_q}),
                            Q(**{('%s__icontains' %
                                    'address'): self.search_q}),
                            Q(**{('%s__icontains' %
                                    'location__latitude'): self.search_q}),
                            Q(**{('%s__icontains' %
                                    'location__longitude'): self.search_q}),
                        ]))

            if(self.status_choice):
                status_here = self.status_choice
                print(f'status:{status_here}')
                if status_here != '-empty-' :
                    self.qs = self.qs.filter(organization_type=status_here)

            if(self.status_now):
                # print "OKAY STATUS NOW : ", self.status_now
                if(self.status_now == 'True'):
                    # print "HARI INI"
                    startdate = datetime.datetime.today()
                    startdate = startdate.replace(hour=0, minute=0, second=0)
                    enddate = startdate + datetime.timedelta(days=1)
                    enddate = enddate - datetime.timedelta(seconds=1)
                    self.qs = self.qs.filter(
                        cdate__range=[startdate, enddate])
                else:
                    _date_range = self.tgl_range.split('-')
                    if(_date_range[0].strip() != 'Invalid date'):
                        _tgl_mulai = datetime.datetime.strptime(
                            _date_range[0].strip(), "%d/%m/%Y %H:%M")
                        _tgl_end = datetime.datetime.strptime(
                            _date_range[1].strip(), "%d/%m/%Y %H:%M")
                        # print "BEBAS"
                        if(_tgl_end > _tgl_mulai):
                            self.qs = self.qs.filter(
                                cdate__range=[_tgl_mulai, _tgl_end])
                        else:
                            self.err_message_here = "Tgl Sampai Harus Lebih besar dari Tgl Dari"
                    else:
                        self.err_message_here = "Format Tanggal tidak valid"
        else:
            print("{}".format("else request GET"))

        # print(self.qs.query)
        return self.qs

    def get_context_object_name(self, object_list):
        return ListView.get_context_object_name(self, object_list)

    def get_context_data(self, **kwargs):
        context = super(CRMCompanyListView, self).get_context_data(**kwargs)
        if self.request.method == 'GET':
            context['form_search'] = CompanySearchForm(self.request.GET.copy())
        else:
            context['form_search'] = CompanySearchForm()
        context['results_per_page'] = self.paginate_by
        context['obj_search'] = None
        context['err_msg'] = self.err_message_here
        context['PROJECT_URL'] = settings.PROJECT_URL
        get_copy = self.request.GET.copy()
        parameters = get_copy.pop('page', True) and get_copy.urlencode()
        context['parameters'] = parameters
        return context

    def get(self, request, *args, **kwargs):
        return ListView.get(self, request, *args, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        rend_here = super(CRMCompanyListView, self).render_to_response(
            context, **response_kwargs)
        return rend_here


# @tmptlogin_required
# # @tmptlogin_required_exclude(['finance'])
# class CompanyDetailView(DetailView):
#     model = Company
#     template_name = 'object/company/details.html'

#     def get_context_data(self, **kwargs):
#         context = super(CompanyDetailView, self).get_context_data(**kwargs)
#         context['now'] = timezone.now()
#         return context


# @tmptlogin_required
# class CompanyEditPageView(View):
#     model = Company
#     template_name = 'object/company/edit_create.html'
    
#     @method_decorator(csrf_protect)
#     def get(self, request, building_id):
#         qs = self.model.objects.filter(id=building_id, delstatus=False).first()
#         return render(request, self.template_name, {
#             "building": qs,
#             'type': 'edit', 
#             'building_id': building_id,
#         })    

# @tmptlogin_required
# class CompanyCreatePageView(View):
#     model = Company
#     template_name = 'object/company/edit_create.html'
    
#     @method_decorator(csrf_protect)
#     def get(self, request):
#         return render(request, self.template_name, {
#             "building": None,
#             'type': 'create', 
#             'building_id': None,
#         })    


# #START API BRAND
# class CRMLocationView(View, ResponseAPI):

#     def get(self, request, lat, lon):
#         try:
#             print(f'lat {lat}, lon {lon}')
#             point_search = Point(float(lon), float(lat))

#             kelurahan = iu.get_kelurahan_by_coordinate(point_search)
#             print(f'kelurahan {kelurahan}')
#             if kelurahan:
#                 rs = {
#                     'propinsi': kelurahan.name_1,
#                     'kota': kelurahan.name_2,
#                     'kecamatan': kelurahan.name_3,
#                     'kelurahan': kelurahan.name_4,
#                 }

#                 return self.resp(status=True, data=rs)
#         except Exception as e:
#             return self.resp(f'error generate location by lat lon => {e}')      
#         return self.resp(f'error no gis found from lat lon => {e}')
