import pickle
from dataclasses import asdict
from typing import Iterable, override

from scrapy import Selector, Spider
from scrapy.http import Request, Response
from scrapy.selector import SelectorList

from ..conf import CACHE_DIR, CONFIG
from ..items import Catalog, Detail, DetailItem
from ..util import AdministrativeArea, search_administrative

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
        xpaths = CONFIG["xpath"]["detail"]
        catalog: Catalog = response.meta["catalog"]
        area: AdministrativeArea = response.meta["area"]

        bill = _fuzzy_select(response, xpaths["bill"])
        address = _fuzzy_select(response, xpaths["address"])
        orders = _fuzzy_select(response, xpaths["orders"])
        administrative_address = search_administrative([address, catalog.name])

        yield DetailItem(
            {
                "detail": Detail(
                    **asdict(catalog),
                    administrative_address=administrative_address,
                    bill=bill,
                    orders=orders,
                ),
                "area": area,
            }
        )


def _fuzzy_select(response: Response, xpath: str | list[str]) -> str:
    if isinstance(xpath, str):
        return response.xpath(xpath).extract_first()
    for x in xpath:
        result: SelectorList[Selector] = response.xpath(x)
        if len(result) > 0:
            return result.extract_first()
    return ""
