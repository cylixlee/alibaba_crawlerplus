"""
Addressing module.

This module contains utility functions to get (load) the whole administrative area, and
searching among then to form a complete administrative address.

Conventionally, the dataclass :class:`AdministrativeArea` is defined in
:module:`datamodels` module, not here.
"""

from collections import deque

from ..conf import CONFIG
from ..datamodels import AdministrativeArea

__all__ = [
    "administrative_areas",
    "administrative_units",
    "administrative_address_of",
]

# cache variables
_administrative_areas: list[AdministrativeArea] | None = None
_administrative_units: list[AdministrativeArea] | None = None


def administrative_areas() -> list[AdministrativeArea]:
    """
    Traverse administrative areas in the configuration file, and constructs tree
    structure according to that.

    :returns: a list containing :class:`AdministrativeArea`s, each of which is an
        abstraction of the administrative area in real life in the form of tree.

    To search a specific address, see :func:`administrative_address_of`.
    """
    global _administrative_areas

    if _administrative_areas is None:
        data = CONFIG["administrative-area"]
        areas = []
        for element in data:
            areas.append(_load(element))
        _administrative_areas = areas
    return _administrative_areas


def administrative_units() -> list[AdministrativeArea]:
    """
    Returns the leaf nodes of all administrative area trees.

    This is useful because we often search the most precise address (e.g. districts)
    instead of the less one (e.g. province). The latter will result in inefficient density
    of useful data, and probably a performance downgrade.
    """
    global _administrative_units

    if _administrative_units is None:
        queue: deque[AdministrativeArea] = deque(administrative_areas())
        result: list[AdministrativeArea] = []
        while len(queue) > 0:
            element = queue.popleft()
            if element.children:
                for child in element.children:
                    queue.append(child)
            else:
                result.append(element)
        _administrative_units = result
    return _administrative_units


def administrative_address_of(addr: str | list[str]) -> list[str] | None:
    """
    Search the tree structures of administrative areas, returns the name according to the
    tree.

    This function searches all administrative areas loaded from configuration, and returns
    the first match if any. Otherwise, the last result (should be ``None``) is returned.
    """
    if isinstance(addr, list):
        addr = " ".join(addr)
    addr = addr.lower()

    for area in administrative_areas():
        result = _search(addr, area)
        if result:
            return result
    return result


# load administrative areas recursively
def _load(data: dict) -> AdministrativeArea:
    # configuration must be complete.
    assert data["address"] is not None and data["name"] is not None
    area = AdministrativeArea(data["address"], data["name"], None, [])
    if "children" in data.keys() and len(data["children"]) > 0:
        for child in data["children"]:
            subarea = _load(child)
            subarea.parent = area
            area.children.append(subarea)
    return area


# search the tree and returns the address name
def _search(addr: str, area: AdministrativeArea) -> list[str] | None:
    for child in area.children:
        childresult = _search(addr, child)
        if len(childresult) > 0:  # matches the first child that appears in addr.
            return [area.name, *childresult]
    if area.address in addr:
        return [area.name]
    return None
