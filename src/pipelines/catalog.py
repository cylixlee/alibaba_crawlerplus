import pickle
import weakref
from io import TextIOWrapper

from scrapy import Item, Spider

from ..conf import CACHE_DIR
from ..items import Catalog, CatalogItem
from ..util import AdministrativeArea

__all__ = ["CatalogItemPipeline"]


class CatalogItemPipeline(object):
    cache_path = CACHE_DIR / "catalogs.pickle"
    items: dict[AdministrativeArea, list[Catalog]] = {}
    _file: TextIOWrapper
    _finalizer: weakref.finalize

    def open_spider(self, spider: Spider):
        self._file = open(self.cache_path, "wb")
        self._finalizer = weakref.finalize(self, lambda f: f.close(), self._file)

    def close_spider(self, spider: Spider):
        pickle.dump(self.items, self._file)
        self._finalizer()

    def process_item(self, item: Item, spider: Spider) -> Item:
        if not isinstance(item, CatalogItem):
            return item
        if item["area"] not in self.items.keys():
            self.items[item["area"]] = []
        self.items[item["area"]].append(item["catalog"])
        return item
