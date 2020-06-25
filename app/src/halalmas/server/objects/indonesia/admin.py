from django.contrib.gis import admin
from .models import KelurahanBorder, KecamatanBorder, \
    KabupatenBorder, ProvinsiBorder


class KelurahanBorderAdmin(admin.OSMGeoAdmin):
    """ OSMGeoAdmin = Open Street Map """

    list_display = ['name_4', 'gid_0', 'name_0', 'gid_1', 'name_1', 'gid_2', 'name_2', 'gid_3',
                    'name_3', 'gid_4', 'varname_4', 'type_4', 'engtype_4', 'cc_4',
                    'slug_0','slug_1','slug_2','slug_3','slug_4']
    search_fields = ['name_1', 'name_2', 'name_3', 'name_4']

    list_filter = ['name_1']
    save_on_top = True

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class KecamatanBorderAdmin(admin.OSMGeoAdmin):
    """ OSMGeoAdmin = Open Street Map 
        gid_0 = models.CharField(max_length=80)
    name_0 = models.CharField(max_length=80)
    gid_1 = models.CharField(max_length=80)
    name_1 = models.CharField(max_length=80)
    nl_name_1 = models.CharField(max_length=80)
    gid_2 = models.CharField(max_length=80)
    name_2 = models.CharField(max_length=80)
    nl_name_2 = models.CharField(max_length=80)
    gid_3 = models.CharField(max_length=80)
    name_3 = models.CharField(max_length=80)
    varname_3 = models.CharField(max_length=80)
    nl_name_3 = models.CharField(max_length=80)
    type_3 = models.CharField(max_length=80)
    engtype_3 = models.CharField(max_length=80)
    cc_3 = models.CharField(max_length=80)
    hasc_3 = models.CharField(max_length=80)
    geom = models.MultiPolygonField(srid=4326)
    """

    list_display = ['name_3', 'gid_0', 'name_0', 'gid_1', 'name_1', 'gid_2', 'name_2', 'gid_3',
                    'engtype_3', 'slug_0','slug_1','slug_2','slug_3']
    search_fields = ['name_1', 'name_2', 'name_3', ]

    list_filter = ['name_1']
    save_on_top = True

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class KabupatenBorderAdmin(admin.OSMGeoAdmin):
    """ OSMGeoAdmin = Open Street Map 
         gid_0 = models.CharField(max_length=80)
    name_0 = models.CharField(max_length=80, verbose_name='Negara')
    gid_1 = models.CharField(max_length=80)
    name_1 = models.CharField(max_length=80, verbose_name='Propinsi')
    nl_name_1 = models.CharField(max_length=80)
    gid_2 = models.CharField(max_length=80)
    name_2 = models.CharField(max_length=80, verbose_name='Kabupaten/Kota')
    varname_2 = models.CharField(max_length=80)
    nl_name_2 = models.CharField(max_length=80)
    type_2 = models.CharField(max_length=80)
    engtype_2 = models.CharField(max_length=80)
    cc_2 = models.CharField(max_length=80)
    hasc_2 = models.CharField(max_length=80)
    geom = models.MultiPolygonField(srid=4326)
    """

    list_display = ['name_2', 'gid_0', 'name_0', 'gid_1', 'name_1', 'gid_2',
                    'engtype_2', 'slug_0','slug_1','slug_2']
    search_fields = ['name_1', 'name_2', ]

    list_filter = ['name_1']
    save_on_top = True

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class PropinsiBorderAdmin(admin.OSMGeoAdmin):
    """ OSMGeoAdmin = Open Street Map 
        gid_0 = models.CharField(max_length=80)
        name_0 = models.CharField(max_length=80)
        gid_1 = models.CharField(max_length=80)
        name_1 = models.CharField(max_length=80)
        varname_1 = models.CharField(max_length=80)
        nl_name_1 = models.CharField(max_length=80)
        type_1 = models.CharField(max_length=80)
        engtype_1 = models.CharField(max_length=80)
        cc_1 = models.CharField(max_length=80)
        hasc_1 = models.CharField(max_length=80)
        geom = models.MultiPolygonField(srid=4326)

    """

    list_display = ['name_1', 'gid_0', 'name_0', 'gid_1',
                    'engtype_1', 'slug_0','slug_1']
    search_fields = ['name_1', ]
    # list_filter = ['name_1']
    save_on_top = True

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(KelurahanBorder, KelurahanBorderAdmin)
admin.site.register(KecamatanBorder, KecamatanBorderAdmin)
admin.site.register(KabupatenBorder, KabupatenBorderAdmin)
admin.site.register(ProvinsiBorder, PropinsiBorderAdmin)
# admin.site.register(IndonesiaBorder, admin.GeoModelAdmin)
