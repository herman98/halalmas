from __future__ import unicode_literals

import json
from django.http import HttpResponse


def ajax_response(reason, result=None):
    if result is None:
        result = "nok"
    return HttpResponse(
        json.dumps({"reason": reason,
                    'result': result}),
        content_type="application/json"
    )


def ajax_response_dump(js_data):
    return HttpResponse(
        json.dumps(js_data),
        content_type="application/json"
    )
