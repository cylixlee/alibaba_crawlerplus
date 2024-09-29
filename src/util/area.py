from collections import deque
from dataclasses import dataclass
from functools import cache
from typing import override

from ..conf import CONFIG

__all__ = ["AdministrativeArea", "administrative_roots", "administrative_nodes"]


@dataclass
class AdministrativeArea(object):
    """
    Corresponding data structure of `administrative-area`s in configuration.

    This class overrides :method:`__eq__` and :method:`__hash__`, in order to be used as
    dict keys or sets' elements. The ``children`` field does not participate in those
    because children's state does not affect the parent's.
    """

    address: str
    name: str
    children: list["AdministrativeArea"] | None

    @override
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, AdministrativeArea):
            return False
        return self.address == value.address and self.name == value.name

    @override
    def __hash__(self) -> int:
        return hash((self.name, self.address))


@cache
def administrative_roots() -> list[AdministrativeArea]:
    """
    Get roots of administrative area trees.

    This function is cached. Call it whenever and wherever you want.
    """
    roots = []
    for data in CONFIG["administrative-area"]:
        roots.append(_parse_administrative_area(data))
    return roots


@cache
def administrative_nodes() -> list[AdministrativeArea]:
    """
    Get all nodes on the administrative area trees.

    This function is cached. Call it whenever and wherever you want.
    """
    nodes = []
    queue = deque(administrative_roots())
    while len(queue) > 0:
        element = queue.popleft()
        if element.children is not None:
            for child in element.children:
                queue.append(child)
        nodes.append(element)
    return nodes


def _parse_administrative_area(data: dict) -> AdministrativeArea:
    area = AdministrativeArea(data["address"], data["name"], None)
    if "children" in data.keys():
        children = []
        for child_data in data["children"]:
            children.append(_parse_administrative_area(child_data))
        area.children = children
    return area
