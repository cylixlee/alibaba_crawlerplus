import pathlib
import pickle
import weakref

from scrapy import Item, Spider

from ..conf import CACHE_DIR
from ..items import Detail, DetailItem
from ..util import AdministrativeArea

__all__ = ["DetailItemPipeline"]


class DetailItemPipeline(object):
    cache_path = CACHE_DIR / "details.pickle"
    items: dict[AdministrativeArea, list[Detail]] = {}
    _finalizer: weakref.finalize

    def open_spider(self, spider: Spider) -> None:
        def finalizer(data: dict, path: pathlib.Path) -> None:
            with open(path, "wb") as file:
                pickle.dump(data, file=file)

        self._finalizer = weakref.finalize(self, finalizer, self.items, self.cache_path)

    def close_spider(self, spider: Spider) -> None:
        self._finalizer()

    def process_item(self, item: Item, spider: Spider) -> Item:
        if not isinstance(item, DetailItem):
            return item
        if item["area"] not in self.items.keys():
            self.items[item["area"]] = []
        self.items[item["area"]].append(item["detail"])
        return item
