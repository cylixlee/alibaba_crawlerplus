import pickle
from dataclasses import asdict
from typing import Iterable, override

from scrapy import Spider
from scrapy.http import Request, Response

from ..conf import CACHE_DIR, CONFIG
from ..items import Catalog, Detail, DetailItem
from ..util import AdministrativeArea, search_administrative

__all__ = ["DetailSpider"]


class DetailSpider(Spider):
    name = "detail"
    allowed_domains = ["alibaba.com"]

    @override
    def start_requests(self) -> Iterable[Request]:
        # load catalogs data to start crawling.
        with open(CACHE_DIR / "catalogs.pickle", "rb") as f:
            catalogs_cache: dict[AdministrativeArea, list[Catalog]] = pickle.load(f)

        # if there's already part of the details, de-duplicate them.
        cache_path = CACHE_DIR / "details.pickle"
        if cache_path.exists():
            with open(cache_path, "rb") as f:
                details_cache: dict[AdministrativeArea, list[Detail]] = pickle.load(f)
            for area, details in details_cache.items():
                print(f"=== Skipping {len(details)} records in area {area.name} ===")

                # eliminate duplicate targets.
                #
                # due to the concurrency inside Scrapy, we cannot assume that DetailItems
                # are saved in the same order of CatalogItems.
                targets: list[Catalog] = []
                for catalog in catalogs_cache[area]:
                    has_requested = False
                    for detail in details:
                        if detail.is_result_of(catalog):
                            # print(f" >> Skipped {detail.detail_url}")
                            has_requested = True
                            break
                    if not has_requested:
                        targets.append(catalog)
                catalogs_cache[area] = targets

        # yield requests to the engine.
        for area, catalogs in catalogs_cache.items():
            for catalog in catalogs:
                meta = {
                    "catalog": catalog,
                    "area": area,
                }
                yield Request(url=catalog.detail_url, meta=meta)

    @override
    def parse(self, response: Response) -> Iterable[DetailItem]:
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
        xpath = [xpath]
    for x in xpath:
        result = response.xpath(x).extract_first()
        if result:
            return result
    return ""
