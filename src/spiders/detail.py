import pickle
from typing import Iterable, override

from scrapy import Spider
from scrapy.http import Request, Response

from ..conf import CACHE_DIR
from ..items import Catalog
from ..util import AdministrativeArea

__all__ = ["DetailSpider"]


class DetailSpider(Spider):
    name = "detail"
    allowed_domains = ["alibaba.com"]

    @override
    def start_requests(self) -> Iterable[Request]:
        # start to crawl detail pages according to catalogs.
        with open(CACHE_DIR / "catalogs.pickle", "rb") as f:
            cache: dict[AdministrativeArea, list[Catalog]] = pickle.load(f)
        for area, catalogs in cache.items():
            for catalog in catalogs:
                meta = {
                    "catalog": catalog,
                    "area": area,
                }
                yield Request(url=catalog.detail_url, meta=meta)

    @override
    def parse(self, response: Response):
        pass
