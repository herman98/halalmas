# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from dal import autocomplete

from django import forms
from django.contrib import admin

from tempatdotcom.core.forms import AutocompleteWidget
from .models import WebScrapper, WebScrapperDetail

from .pergikuliner.admin import *


class WebScrapperModelForm(forms.ModelForm):
    domain_name = urls_page = forms.CharField(widget=forms.Textarea(
        attrs={'rows': '5', 'cols': '150'}), required=False)

    class Meta:
        model = WebScrapper
        exclude = ('cdate', 'udate',)


class WebScrapperAdmin(admin.ModelAdmin):
    # models = Brand
    form = WebScrapperModelForm

    list_per_page = 50
    search_fields = ('domain_name', 'pk', 'location', 'urls_page',)
    list_display = ('domain_name', 'pk', 'location', 'urls_page', 'max_page', 'done',
                    'delstatus',)
    list_filter = ('done', 'delstatus',)
    fieldsets = (
        ('Field', {
            'fields': ('domain_name', 'location',
                       'urls_page', 'max_page', 'done',),
        }),
        ('Timestamp', {
            'classes': ('collapse',),  # collapse
            'fields': ('delstatus', 'deldate', 'cdate', 'udate'),
        }),
    )
    readonly_fields = ('cdate', 'udate')
    save_on_top = True
    actions = ['make_done_true', 'make_done_false']

    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    def make_done_true(self, request, queryset):
        rows_updated = queryset.update(done=True)
        self.message_user(
            request, "%s done were successfully marked as true." % rows_updated)

    def make_done_false(self, request, queryset):
        rows_updated = queryset.update(done=False)
        self.message_user(
            request, "%s done were successfully marked as false." % rows_updated)

    make_done_true.short_description = "Mark selected done as True"
    make_done_false.short_description = "Mark selected done as False"


class WebScrapperDetailModelForm(forms.ModelForm):
    urls_detail = forms.CharField(widget=forms.Textarea(
        attrs={'rows': '5', 'cols': '150'}), required=False)

    class Meta:
        model = WebScrapperDetail
        exclude = ('cdate', 'udate',)
        widgets = {
            'web_source': AutocompleteWidget(url='scrapper-autocomplete'),
        }


class WebScrapperDetailAdmin(admin.ModelAdmin):
    # models = WebScrapperDetail
    form = WebScrapperDetailModelForm

    list_per_page = 50
    search_fields = ('web_source__domain_name', 'pk', 'urls_detail',
                     'web_source__location', )
    list_display = ('web_source', 'pk', 'urls_detail', 'done',
                    'delstatus',)
    list_filter = ('done', 'delstatus',)
    fieldsets = (
        ('Foreignkey Field', {
            'fields': ('web_source', ),
        }),
        ('Field', {
            'fields': ('urls_detail', 'done', ),
        }),
        ('Timestamp', {
            'classes': ('collapse',),  # collapse
            'fields': ('delstatus', 'deldate', 'cdate', 'udate'),
        }),
    )
    readonly_fields = ('cdate', 'udate')
    save_on_top = True
    actions = ['make_done_true', 'make_done_false']

    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    def make_done_true(self, request, queryset):
        rows_updated = queryset.update(done=True)
        self.message_user(
            request, "%s done were successfully marked as true." % rows_updated)

    def make_done_false(self, request, queryset):
        rows_updated = queryset.update(done=False)
        self.message_user(
            request, "%s done were successfully marked as false." % rows_updated)

    make_done_true.short_description = "Mark selected done as True"
    make_done_false.short_description = "Mark selected done as False"


admin.site.register(WebScrapperDetail, WebScrapperDetailAdmin)
admin.site.register(WebScrapper, WebScrapperAdmin)
