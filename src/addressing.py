"""
Addressing module.

This module contains utility functions to get (load) the whole administrative area, and
searching among then to form a complete administrative address.

Conventionally, the dataclass :class:`AdministrativeArea` is defined in
:module:`datamodels` module, not here.
"""

from .configuration import CONFIG
from .datamodels import AdministrativeArea

__administrative_area: AdministrativeArea | None = None


def administrative_area() -> AdministrativeArea:
    """
    Traverse administrative areas in the configuration file, and constructs tree
    structure according to that.
    """
    global __administrative_area

    if __administrative_area is None:
        __administrative_area = __load(CONFIG["administrative-area"])
    return __administrative_area


def administrative_address_of(addr: str | list[str]) -> str:
    """
    Search the tree structure of administrative areas, returns the name according to the
    tree.
    """
    if isinstance(addr, list):
        addr = " ".join(addr)
    addr = addr.lower()
    return __search(addr, administrative_area())


# load administrative areas recursively
def __load(data: dict) -> AdministrativeArea:
    # configuration must be complete.
    assert data["address"] is not None and data["name"] is not None
    area = AdministrativeArea(data["address"], data["name"], None, [])
    if "children" in data.keys() and len(data["children"]) > 0:
        for child in data["children"]:
            subarea = __load(child)
            subarea.parent = area
            area.children.append(subarea)
    return area


# search the tree and returns the address name
def __search(addr: str, area: AdministrativeArea) -> str:
    for child in area.children:
        childresult = __search(addr, child)
        if childresult != "":  # matches the first child that appears in addr.
            return area.name + childresult
    if area.address in addr:
        return area.name
    return ""
