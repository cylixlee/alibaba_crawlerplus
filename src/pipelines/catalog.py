import pickle
import weakref
from io import TextIOWrapper

from scrapy import Item, Spider

from ..conf import CACHE_DIR
from ..items import CatalogItem

__all__ = ["CatalogItemPipeline"]


class CatalogItemPipeline(object):
    cache_path = CACHE_DIR / "catalogs.pickle"
    items: list[CatalogItem]
    _file: TextIOWrapper
    _finalizer: weakref.finalize

    def open_spider(self, spider: Spider):
        self.items = []
        self._file = open(self.cache_path, "wb")
        self._finalizer = weakref.finalize(self, lambda f: f.close(), self._file)

    def close_spider(self, spider: Spider):
        self._finalizer()

    def process_item(self, item: Item, spider: Spider) -> Item:
        if not isinstance(item, CatalogItem):
            return item
        self._synchronize(item)
        return item

    def _synchronize(self, item: CatalogItem) -> None:
        self.items.append(item)
        pickle.dump(self.items, self._file)
