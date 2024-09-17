from dataclasses import dataclass
from typing import Optional, Self

__all__ = ["AdministrativeArea"]


@dataclass
class AdministrativeArea(object):
    address: str
    name: str
    parent: Optional[Self]
    children: list[Self]
