from dataclasses import dataclass

from scrapy import Field, Item

from ..util import AdministrativeArea
from .catalog import Catalog

__all__ = ["Detail", "DetailItem"]


@dataclass
class Detail(Catalog):
    administrative_address: list[AdministrativeArea] | None
    bill: str
    orders: str


class DetailItem(Item):
    detail = Field()
    area = Field()  # for classification and insertion into corresponding list
