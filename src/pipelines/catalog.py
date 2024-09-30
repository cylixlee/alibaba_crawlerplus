import pickle

from scrapy import Item, Spider

from ..conf import CACHE_DIR
from ..items import Catalog, CatalogItem
from ..util import AdministrativeArea

__all__ = ["CatalogItemPipeline"]


class CatalogItemPipeline(object):
    cache_path = CACHE_DIR / "catalogs.pickle"
    items: dict[AdministrativeArea, list[Catalog]] = {}

    def process_item(self, item: Item, spider: Spider) -> Item:
        if not isinstance(item, CatalogItem):
            return item
        self._synchronize(item)
        return item

    def _synchronize(self, item: CatalogItem) -> None:
        if item["area"] not in self.items.keys():
            self.items[item["area"]] = []
        self.items[item["area"]].append(Catalog.from_item(item))
        with open(self.cache_path, "wb") as f:
            pickle.dump(self.items, f)
