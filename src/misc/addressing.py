"""
Addressing module.

This module contains utility functions to get (load) the whole administrative area, and
searching among then to form a complete administrative address.

Conventionally, the dataclass :class:`AdministrativeArea` is defined in
:module:`datamodels` module, not here.
"""

from ..conf import CONFIG
from ..datamodels import AdministrativeArea

__all__ = [
    "administrative_areas",
    "administrative_address_of",
]

__administrative_area: list[AdministrativeArea] | None = None


def administrative_areas() -> list[AdministrativeArea]:
    """
    Traverse administrative areas in the configuration file, and constructs tree
    structure according to that.

    :returns: a list containing :class:`AdministrativeArea`s, each of which is an
        abstraction of the administrative area in real life in the form of tree.

    To search a specific address, see :func:`administrative_address_of`.
    """
    global __administrative_area

    if __administrative_area is None:
        data = CONFIG["administrative-area"]
        __administrative_area = []
        for element in data:
            __administrative_area.append(_load(element))
    return __administrative_area


def administrative_address_of(addr: str | list[str]) -> list[str]:
    """
    Search the tree structures of administrative areas, returns the name according to the
    tree.

    This function searches all administrative areas loaded from configuration, and returns
    the first match if any. Otherwise, the last result (an empty list ``[]``) is returned.
    """
    if isinstance(addr, list):
        addr = " ".join(addr)
    addr = addr.lower()

    for area in administrative_areas():
        result = _search(addr, area)
        if len(result) > 0:
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
def _search(addr: str, area: AdministrativeArea) -> list[str]:
    for child in area.children:
        childresult = _search(addr, child)
        if len(childresult) > 0:  # matches the first child that appears in addr.
            return [area.name, *childresult]
    if area.address in addr:
        return [area.name]
    return []
