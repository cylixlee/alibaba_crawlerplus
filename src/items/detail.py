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

    def is_result_of(self, catalog: Catalog) -> bool:
        return (
            self.detail_url == catalog.detail_url
            and self.domain == catalog.domain
            and self.name == catalog.name
            and self.provided_products == catalog.provided_products
        )


class DetailItem(Item):
    detail = Field()
    area = Field()  # for classification and insertion into corresponding list
