from django.contrib.gis import admin
from .models import Currency  # , CurrencyHistory


class CurrencyAdmin(admin.OSMGeoAdmin):
    """ Currency Rate Master Data Admin page"""

    list_display = ['curr_name', 'curr_value',
                    'rate_sale', 'rate_buy', 'is_active', 'creator']
    search_fields = ['curr_name', ]
    list_filter = ['is_active']

    fieldsets = (
        ('Data Field', {
            'fields': ('curr_name', 'curr_value',
                       'rate_sale', 'rate_buy', 'is_active', ),
        }),
        ('Timestamp', {
            'classes': ('collapse',),  # collapse
            'fields': ('delstatus', 'deldate', 'cdate', 'udate'),
        }),
    )
    readonly_fields = ('cdate', 'udate')


# class CurrencyHistoryAdmin(admin.OSMGeoAdmin):
#     """ Currency Rate history Data Admin page"""

#     list_display = ['pk', 'currency', 'curr_value',
#                     'rate_sale', 'rate_buy', ]
#     search_fields = ['currency__curr_name', ]


admin.site.register(Currency, CurrencyAdmin)
# admin.site.register(CurrencyHistory, CurrencyHistoryAdmin)
