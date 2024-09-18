from dataclasses import dataclass
from typing import Self

__all__ = ["AdministrativeArea"]


@dataclass
class AdministrativeArea(object):
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
