import pickle
import weakref
from io import TextIOWrapper

from scrapy import Item, Spider

from ..conf import CACHE_DIR
from ..items import Detail, DetailItem
from ..util import AdministrativeArea

__all__ = ["DetailItemPipeline"]


class DetailItemPipeline(object):
    cache_path = CACHE_DIR / "details.pickle"
    items: dict[AdministrativeArea, list[Detail]] = []
    _file: TextIOWrapper
    _finalizer: weakref.finalize

    def open_spider(self, spider: Spider):
        self._file = open(self.cache_path, "wb")
        self._finalizer = weakref.finalize(self, lambda f: f.close(), self._file)

    def close_spider(self, spider: Spider):
        pickle.dump(self.items, self._file)
        self._finalizer()

    def process_item(self, item: Item, spider: Spider) -> Item:
        if not isinstance(item, DetailItem):
            return item
        if item["area"] not in self.items.keys():
            self.items[item["area"]] = []
        self.items[item["area"]].append(item["detail"])
        return item
