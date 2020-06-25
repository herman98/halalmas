import os
from django.contrib.gis.utils import LayerMapping
from .models import ProvinsiBorder, KabupatenBorder, \
    KecamatanBorder, KelurahanBorder

# `LayerMapping` dictionary for model
provinsiborder_mapping = {
    'gid_0': 'GID_0',
    'name_0': 'NAME_0',
    'gid_1': 'GID_1',
    'name_1': 'NAME_1',
    'varname_1': 'VARNAME_1',
    'nl_name_1': 'NL_NAME_1',
    'type_1': 'TYPE_1',
    'engtype_1': 'ENGTYPE_1',
    'cc_1': 'CC_1',
    'hasc_1': 'HASC_1',
    'geom': 'MULTIPOLYGON',
}

kabupatenborder_mapping = {
    'gid_0': 'GID_0',
    'name_0': 'NAME_0',
    'gid_1': 'GID_1',
    'name_1': 'NAME_1',
    'nl_name_1': 'NL_NAME_1',
    'gid_2': 'GID_2',
    'name_2': 'NAME_2',
    'varname_2': 'VARNAME_2',
    'nl_name_2': 'NL_NAME_2',
    'type_2': 'TYPE_2',
    'engtype_2': 'ENGTYPE_2',
    'cc_2': 'CC_2',
    'hasc_2': 'HASC_2',
    'geom': 'MULTIPOLYGON',
}

kecamatanborder_mapping = {
    'gid_0': 'GID_0',
    'name_0': 'NAME_0',
    'gid_1': 'GID_1',
    'name_1': 'NAME_1',
    'nl_name_1': 'NL_NAME_1',
    'gid_2': 'GID_2',
    'name_2': 'NAME_2',
    'nl_name_2': 'NL_NAME_2',
    'gid_3': 'GID_3',
    'name_3': 'NAME_3',
    'varname_3': 'VARNAME_3',
    'nl_name_3': 'NL_NAME_3',
    'type_3': 'TYPE_3',
    'engtype_3': 'ENGTYPE_3',
    'cc_3': 'CC_3',
    'hasc_3': 'HASC_3',
    'geom': 'MULTIPOLYGON',
}

kelurahanborder_mapping = {
    'gid_0': 'GID_0',
    'name_0': 'NAME_0',
    'gid_1': 'GID_1',
    'name_1': 'NAME_1',
    'gid_2': 'GID_2',
    'name_2': 'NAME_2',
    'gid_3': 'GID_3',
    'name_3': 'NAME_3',
    'gid_4': 'GID_4',
    'name_4': 'NAME_4',
    'varname_4': 'VARNAME_4',
    'type_4': 'TYPE_4',
    'engtype_4': 'ENGTYPE_4',
    'cc_4': 'CC_4',
    'geom': 'MULTIPOLYGON',
}


# os.path.dirname(__file__),
abs_path_data = '/Users/sky/halalmas/server/data'

# Shapefile path
provinsi_shp = os.path.abspath(
    os.path.join(
        abs_path_data,
        'indonesia', 'gadm36_IDN_1.shp'
    ),
)

kabupaten_shp = os.path.abspath(
    os.path.join(
        abs_path_data,
        'indonesia', 'gadm36_IDN_2.shp'
    ),
)

kecamatan_shp = os.path.abspath(
    os.path.join(
        abs_path_data,
        'indonesia', 'gadm36_IDN_3.shp'
    ),
)

kelurahan_shp = os.path.abspath(
    os.path.join(
        abs_path_data,
        'indonesia', 'gadm36_IDN_4.shp'
    ),
)


def run(verbose=True):
    """
    The transform keyword is set to False 
    because the data in the shapefile does not need to be converted -- it's already in WGS84 (SRID=4326)
    """
    # Provinsi
    lm_provinsi = LayerMapping(
        ProvinsiBorder, provinsi_shp,
        provinsiborder_mapping, transform=False)
    lm_provinsi.save(strict=True, verbose=verbose)

    # Kabupaten
    lm_kabupaten = LayerMapping(
        KabupatenBorder, kabupaten_shp,
        kabupatenborder_mapping, transform=False)
    lm_kabupaten.save(strict=True, verbose=verbose)

    # Kecamatan
    lm_kecamatan = LayerMapping(
        KecamatanBorder, kecamatan_shp,
        kecamatanborder_mapping, transform=False)
    lm_kecamatan.save(strict=True, verbose=verbose)

    # Kelurahan
    lm_kelurahan = LayerMapping(
        KelurahanBorder, kelurahan_shp,
        kelurahanborder_mapping, transform=False)
    lm_kelurahan.save(strict=True, verbose=verbose)
