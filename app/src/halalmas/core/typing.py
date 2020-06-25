from typing import TypeVar, Generic


# Date
DateTime = TypeVar("<DateTime>")
Date = TypeVar('<Date>')
DateStr = TypeVar('<Date (YYYY-MM-DD)>')


# Point(lon, lat)
WKT = TypeVar("<WKT ('POINT({lon} {lat})')>")
MultiPolygon = TypeVar("<Multipolygon>")

# Indonesia
ProvinsiBorder = TypeVar('ProvinsiBorder')
KabupatenBorder = TypeVar('KabupatenBorder')
KecamatanBorder = TypeVar('KecamatanBorder')
KelurahanBorder = TypeVar('KelurahanBorder')


# Building
Building = TypeVar('Building')
