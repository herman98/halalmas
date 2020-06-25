from django.db import models
# from django.utils.safestring import mark_safe
from cuser.fields import CurrentUserField

from tempatdotcom.server.models import TimeStampedModel


class WebScrapper(TimeStampedModel):
    """
    This is master of WebScrapper Group
    """
    domain_name = models.CharField(max_length=225)
    location = models.CharField(max_length=500, blank=True, null=True)
    urls_page = models.CharField(max_length=500, blank=True, null=True)
    max_page = models.IntegerField(blank=True, null=True)
    done = models.IntegerField(default=0, blank=True, null=True)

    class Meta:
        db_table = "web_scrapper"
        verbose_name_plural = u'Web Scrappers'
        ordering = ['domain_name', 'location']

    @classmethod
    def create(cls, domain_name, location, urls_page, max_page):
        # _domain_name_enc = str(domain_name).encode('UTF-8')
        # _urls_page_enc = str(urls_page).encode('UTF-8')
        cls_here = cls(domain_name=domain_name,
                       location=location, urls_page=urls_page,
                       max_page=max_page)
        cls_here.save()
        return cls_here

    def __str__(self):
        return "{}-{}".format(self.domain_name, self.location)


class WebScrapperDetail(TimeStampedModel):
    """
    This is master of WebScrapper Detail page
    """
    web_source = models.ForeignKey(
        WebScrapper, on_delete=models.DO_NOTHING, blank=True, null=True)
    urls_detail = models.CharField(max_length=500, blank=True, null=True)
    done = models.IntegerField(default=0, blank=True, null=True)

    class Meta:
        db_table = "web_scrapper_detail"
        verbose_name_plural = u'Web Scrapper Detail Pages'
        ordering = ['web_source__domain_name', 'urls_detail']

    def __str__(self):
        return "{}{}".format(self.web_source, self.urls_detail)
