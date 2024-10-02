import pathlib
import pickle
import weakref

from scrapy import Item, Spider

from ..conf import CACHE_DIR
from ..items import Catalog, CatalogItem
from ..util import AdministrativeArea

__all__ = ["CatalogItemPipeline"]


class CatalogItemPipeline(object):
    cache_path = CACHE_DIR / "catalogs.pickle"
    items: dict[AdministrativeArea, list[Catalog]] = {}
    _finalizer: weakref.finalize

    def open_spider(self, spider: Spider) -> None:
        def finalizer(data: dict, path: pathlib.Path) -> None:
            with open(path, "wb") as file:
                pickle.dump(data, file=file)

        self._finalizer = weakref.finalize(self, finalizer, self.items, self.cache_path)

    def close_spider(self, spider: Spider) -> None:
        self._finalizer()

    def process_item(self, item: Item, spider: Spider) -> Item:
        if not isinstance(item, CatalogItem):
            return item
        if item["area"] not in self.items.keys():
            self.items[item["area"]] = []
        self.items[item["area"]].append(item["catalog"])
        return item
