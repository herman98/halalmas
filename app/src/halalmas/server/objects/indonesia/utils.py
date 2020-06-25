from halalmas.core import typing as typ
from halalmas.core.exceptions import DataNotFound


def to_OSM_coordinate(pnt_wkt) -> typ.WKT:
    """ Fixing coordinate from Google Map to OSM (Open Street Map)
    Finding:
    Here we use Indonesia's boundaries data from OSM.
    But latlon from openstreet map is different from google map.
    That's why this function is created to adjust Google Map's latlon to be equal as in OSM.

    For example:
    Tested building is `Wisma 76`,
    if we query, we will get Wisma 76 is in Kemanggisan which actually is in Slipi.
    We add longitude to 0.002200 in order to be considered in Slipi.

    Conclusion:
    After research we asume that longitude taken from google map is -0.002200 from OSM.

    NOTE: This function still in experimental !!!
    """
    lon_diff = 0.002200
    pnt_wkt.x += lon_diff

    return pnt_wkt


def get_kelurahan_by_coordinate(coordinate: typ.WKT) -> typ.KelurahanBorder:
    from .models import KelurahanBorder

    kelurahan = KelurahanBorder.objects.filter(
        geom__contains=coordinate)
    if not kelurahan:
        raise DataNotFound("<Kelurahan {}> not found".format(kelurahan))

    return kelurahan[0]

