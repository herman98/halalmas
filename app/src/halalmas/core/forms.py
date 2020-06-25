
from __future__ import unicode_literals
from dal import autocomplete

from datetime import datetime, timedelta

# from django.utils.safestring import mark_safe
# from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class AutocompleteWidget(autocomplete.ModelSelect2):
    """Some custom code ..."""
    class Media:
        """Add jQuery dependency so autocomplete light's custom js
        is always inserted after jQuery
        """
        extra = '' if settings.DEBUG else '.min'
        js = [
            'admin/js/vendor/jquery/jquery{}.js'.format(extra),  # new line
            # scripts from original app
            'autocomplete_light/jquery.init.js',
            'autocomplete_light/autocomplete.init.js',
            'autocomplete_light/vendor/select2/dist/js/select2.full.js',
            'autocomplete_light/select2.js',
            'admin/js/jquery.init.js',  # new line
        ]
