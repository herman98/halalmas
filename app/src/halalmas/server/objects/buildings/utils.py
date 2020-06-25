from typing import List, Dict
from geodjango import typing as typ


from .models import Buildings


def bulk_insert_building(buildings: List[Dict[str, any]]):
    building_bulk = []
    for building in buildings:
        building_bulk.append(
            Buildings(
                name=building['name'],
                address=building['address'],
                coord_google=building['coord_google']
            )
        )
    Buildings.objects.bulk_create(building_bulk)
