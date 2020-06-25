from __future__ import absolute_import
from __future__ import unicode_literals

import logging
from django.core import exceptions


logger = logging.getLogger(__name__)


class GetInstanceMixin(object):
    def get_or_none(self, **kwargs):
        """Extends get to return None if no object is found based on query."""
        try:
            logger.debug(
                "Getting instance for %s with %s" % (self.model, kwargs))
            instance = self.get(**kwargs)
            logger.info(
                "Got instance primary_key=%s for %s" % (instance.pk, self.model))
            return instance
        except exceptions.ObjectDoesNotExist:
            logger.warn(
                "No instance found for %s with %s" % (self.model, kwargs))
            return None
