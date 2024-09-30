from dataclasses import dataclass

from scrapy import Field, Item

__all__ = ["Catalog", "CatalogItem"]


@dataclass
class Catalog(object):
    """
    Search results from Alibaba's search engine.

    Currently this dataclass contains some information about a supplier. An additional
    class :class:`CatalogItem` is introduced because Scrapy framework only recognize that,
    while we need this dataclass to be serialized with Pickle.
    """

    detail_url: str
    domain: str
    name: str
    provided_products: str


class CatalogItem(Item):
    """
    An item from the catalog of search results. In this project, some information about a
    supplier (manufacturer, or business entity).
    """

    catalog = Field()
    area = Field()
