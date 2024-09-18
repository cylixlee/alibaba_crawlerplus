from dataclasses import dataclass
from typing import Self

__all__ = ["AdministrativeArea"]


@dataclass
class AdministrativeArea(object):
    address: str
    name: str
    parent: Self | None
    children: list[Self]

    def __hash__(self) -> int:
        return hash((self.address, self.name))
