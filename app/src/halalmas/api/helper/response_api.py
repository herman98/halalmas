from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator

class ResponseAPI:
    """
    https://www.django-rest-framework.org/api-guide/responses/
    Response(data, status=None, template_name=None, headers=None, content_type=None)
    """
    per_page = 10
    page = 1
    count = 0
    status_paginate = False
    status_paginate_crm = False
    has_next = False,
    has_previous = False,

    def paginate(self, **kwargs):
        self.per_page = kwargs.get('per_page', 10)
        self.page = kwargs.get('page', 1)
        self.count = kwargs.get('count', 0)
        self.status_paginate = False

    def pagination(self, per_page, page, count):
        self.status_paginate = True
        self.per_page = int(per_page)
        self.page = int(page)
        self.count = count

    def pagination_crm(self, per_page, page, count, has_next, has_previous):
        self.status_paginate_crm = True
        self.per_page = per_page
        self.page = page
        self.count = count
        self.has_next = has_next
        self.has_previous = has_previous

    def resp(self, msg='Sukses !', status=False, data=None):
        rs = {
            "status": status,
            "msg": msg,
            "data": data,
        }

        if self.status_paginate_crm:
            rs["pagination"]: {
                    "page": self.page,
                    "per_page": self.per_page,
                    "count": self.count,
                    "has_next": self.has_next,
                    "has_previous": self.has_previous,
                    # "has_other_page": rs.has_other_pages(),
                    # "next_page_number": rs.next_page_number() or None,
                    # "previous_page_number": rs.previous_page_number() or None,
                }

        return JsonResponse(rs)

    def res(self, msg='Sukses !', status=False, data=None):
        rs = {
            'status': status,
            'msg': msg,
            'data': data,
        }

        if self.status_paginate:
            rs['paginate'] = {
                'per_page': self.per_page,
                'page': self.page,
                'count': self.count
            }

        return Response(rs)
