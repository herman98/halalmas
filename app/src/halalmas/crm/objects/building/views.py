from __future__ import unicode_literals

import operator
import datetime
import logging
import json

from functools import reduce


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

# set decorator for login required
from halalmas.crm import (tmptlogin_required,
                              tmptlogin_required_group,
                              tmptlogin_required_multigroup)
from halalmas.server.objects.buildings.models import Building

from .forms import BuildingSearchForm


logger = logging.getLogger(__name__)



@tmptlogin_required
# @tmptlogin_required_exclude(['finance'])
class BuildingListView(ListView):
    model = Building
    paginate_by = 50  # get_conf("PAGINATION_ROW")
    template_name = 'object/building/list.html'

    def http_method_not_allowed(self, request, *args, **kwargs):
        return ListView.http_method_not_allowed(self, request, *args, **kwargs)

    def get_template_names(self):
        return ListView.get_template_names(self)

    def get_queryset(self):
        self.qs = super(BuildingListView, self).get_queryset()
        self.qs = self.qs.filter(delstatus=False)
        self.qs = self.qs.order_by('-cdate', 'name')

        self.err_message_here = None
        self.tgl_range = None
        self.tgl_start = None
        self.tgl_end = None
        self.category = None
        self.status_choice = None
        self.status_order = None
        self.status_pick = None
        self.search_q = None
        self.status_now = None

        # print(f"self.request.GET: {self.request.GET}")
        if self.request.method == 'GET':
            self.tgl_range = self.request.GET.get('datetime_range', None)
            self.status_choice = self.request.GET.get('status_choice', None)
            self.status_order = self.request.GET.get('status_order', None)
            self.category = self.request.GET.get('category', None)
            self.status_pick = self.request.GET.get('status_pick', None)
            self.search_q = self.request.GET.get('search_q', '').strip()
            self.status_now = self.request.GET.get('status_now', None)

            if(self.status_order):
                __status_ord = self.status_order
                print(f' __status_ord: {__status_ord}')
                if __status_ord == 'latest':
                    self.qs = self.qs.order_by('-cdate', 'name')
                elif __status_ord == 'name_asc':
                    self.qs = self.qs.order_by('name')
                elif __status_ord == 'longest':
                    self.qs = self.qs.order_by('cdate')
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
                                    'latitude'): self.search_q}),
                            Q(**{('%s__icontains' %
                                    'longitude'): self.search_q}),
                            Q(**{('%s__icontains' %
                                    'description_id'): self.search_q}),
                            Q(**{('%s__icontains' %
                                    'building_access_id'): self.search_q}),
                        ]))
            if self.category:
                self.qs = self.qs.filter(building_category=self.category)

            if(self.status_choice):
                __active = self.status_pick
                __status = self.status_choice
                print(f'active: {__active} , status:{__status}')
                if __status == 'is_desc_id':
                    self.qs = self.qs.filter(is_desc_id=__active)
                elif __status == 'is_building_access_id':
                    self.qs = self.qs.filter(is_building_access_id=__active)
                elif __status == 'is_facilities_id':
                    self.qs = self.qs.filter(is_facilities_id=__active)
                

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

        return self.qs

    def get_context_object_name(self, object_list):
        return ListView.get_context_object_name(self, object_list)

    def get_context_data(self, **kwargs):
        context = super(BuildingListView, self).get_context_data(**kwargs)
        if self.request.method == 'GET':
            context['form_search'] = BuildingSearchForm(self.request.GET.copy())
        else:
            context['form_search'] = BuildingSearchForm()
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
        rend_here = super(BuildingListView, self).render_to_response(
            context, **response_kwargs)
        return rend_here


@tmptlogin_required
# @tmptlogin_required_exclude(['finance'])
class BuildingDetailView(DetailView):
    model = Building
    template_name = 'object/building/details.html'

    def get_context_data(self, **kwargs):
        context = super(BuildingDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


@tmptlogin_required
class BuildingEditPageView(View):
    model = Building
    template_name = 'object/building/create_update.html'
    
    @method_decorator(csrf_protect)
    def get(self, request, building_id):
        qs = self.model.objects.filter(id=building_id, delstatus=False).first()
        return render(request, self.template_name, {
            "building": qs,
            'type': 'edit', 
            'building_id': building_id,
        })    

@tmptlogin_required
class BuildingCreatePageView(View):
    model = Building
    template_name = 'object/building/create_update.html'
    
    @method_decorator(csrf_protect)
    def get(self, request):
        return render(request, self.template_name, {
            "building": None,
            'type': 'create', 
            'building_id': None,
        })    


