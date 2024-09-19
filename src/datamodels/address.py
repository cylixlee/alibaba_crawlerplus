from dataclasses import dataclass
from typing import Self

__all__ = ["AdministrativeArea"]


@dataclass
class AdministrativeArea(object):
    """
    A structure representing an administrative area (province, city, district, etc.)

    :method:`__eq__` and :method:`__hash__` are implemented in order to put instances of
    this class as dict (hashmap) keys.

    Note that there're two fields: :field:`parent` and :field:`child`, which are not
    participated in calculating the hash. Resursive hell will happen if we do so.
    """

    address: str
    name: str
    parent: Self | None
    children: list[Self]

    def __eq__(self, value: object) -> bool:
        if isinstance(value, AdministrativeArea):
            return self.address == value.address and self.name == value.name
        return False

    def __hash__(self) -> int:
        return hash((self.address, self.name))
