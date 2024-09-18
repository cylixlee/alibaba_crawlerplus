import pathlib
from datetime import timedelta

from src.datamodels import AdministrativeArea, AlibabaCompanyDetail, AlibabaCompanyOffer
from src.misc.addressing import administrative_units
from src.misc.resuming import DefaultResumableState, transaction
from src.parsers import (
    AlibabaJsonOffersParser,
    AlibabaPageJsonParser,
    AlibabaXpathCompanyParser,
    ComposeParser,
)
from src.requesthubs import (
    AbstractRequestHub,
    SleepyRequestHub,
    default_captcha_detector,
)
from src.urls import AlibabaSearchTab, AlibabaSearchUrl, AlibabaSupplierCountry

PROJECT_DIR = pathlib.Path(__file__).parent
CACHE_DIR = PROJECT_DIR / "cache"


class OffersCrawler(DefaultResumableState):
    def __init__(self, path: pathlib.Path, *, requesthub: AbstractRequestHub) -> None:
        super().__init__(path)
        self._offers: dict[AdministrativeArea, list[AlibabaCompanyOffer]] = {}
        self._pages: dict[AdministrativeArea, int] = {}
        self._completed: set[AdministrativeArea] = set()
        self._requesthub = requesthub

    def crawl(self) -> dict[AdministrativeArea, list[AlibabaCompanyOffer]]:
        for unit in administrative_units():
            # (kind of) Integrity check.
            #
            # If all units are crawled and cached, this function simply returns the
            # result; otherwise, incremental crawling is performed.
            #
            # This saves a lot of duplicate work and makes this task resumable.
            if unit not in self._completed:
                print(f"crawling area {unit.name} ({unit.address})")
                self._crawl_area(unit)
            else:
                print(f"(offers) area {unit.name} ({unit.address}) clear (cached).")
        return self._offers

    @transaction
    def _crawl_area(self, area: AdministrativeArea) -> None:
        parser = ComposeParser(
            AlibabaPageJsonParser(),
            AlibabaJsonOffersParser(),
        )

        if area not in self._pages.keys():
            print("=== starting from page 1 ===")
            self._pages[area] = 1
        else:
            print(f"=== continue from page {self._pages[area]} ===")

        while True:
            url = AlibabaSearchUrl(
                area.address,
                tab=AlibabaSearchTab.Suppliers,
                country=AlibabaSupplierCountry.China,
                page=self._pages[area],
            )
            content = self._requesthub.request(url)
            offers: list[AlibabaCompanyOffer] = parser.parse(content)
            if not offers:
                break

            print(f"crawled {len(offers)} offers (from {url})...")
            self._pages[area] += 1
            self._save_offers(area, offers)
        self._completed.add(area)

    @transaction
    def _save_offers(
        self,
        area: AdministrativeArea,
        offers: list[AlibabaCompanyOffer],
    ) -> None:
        if area not in self._offers.keys():
            print(f"creating new offerlist of {area.name} ({area.address})")
            self._offers[area] = offers
        else:
            self._offers[area].extend(offers)


class DetailsCrawler(DefaultResumableState):
    def __init__(
        self,
        path: pathlib.Path,
        offers: dict[AdministrativeArea, list[AlibabaCompanyOffer]],
        *,
        requesthub: AbstractRequestHub,
    ) -> None:
        super().__init__(path)
        self._offers = offers
        self._details: dict[AdministrativeArea, list[AlibabaCompanyDetail]] = {}
        self._requesthub = requesthub
        self._indices: dict[AdministrativeArea, int] = {}
        self._completed: set[AdministrativeArea] = set()
        self._parser = AlibabaXpathCompanyParser()

    def crawl(self) -> dict[AdministrativeArea, list[AlibabaCompanyDetail]]:
        for area, offers in self._offers.items():
            if area not in self._completed:
                self._crawl_area(area, offers)
            else:
                print(f"(detail) area {area.name} ({area.address}) clear (cached).")
        return self._details

    @transaction
    def _crawl_area(
        self,
        area: AdministrativeArea,
        offers: list[AlibabaCompanyOffer],
    ) -> None:
        if area not in self._indices.keys():
            self._indices[area] = 0
            print(f"=== starting from index {self._indices[area]} ===")
        else:
            print(f"=== continue from index {self._indices[area]} ===")

        while self._indices[area] < len(offers):
            offer = offers[self._indices[area]]
            print(f"crawling offer {self._indices[area]} from {offer.detail_url}")
            self._crawl_detail(area, offer)
        self._completed.add(area)

    @transaction
    def _crawl_detail(
        self,
        area: AdministrativeArea,
        offer: AlibabaCompanyOffer,
    ) -> None:
        content = self._requesthub.request(offer.detail_url)
        detail = self._parser.parse(offer, content)
        if area not in self._details:
            print(f"creating new detaillist of {area.name} ({area.address})")
            self._details[area] = [detail]
        else:
            self._details[area].append(detail)
        self._indices[area] += 1


def main() -> None:
    """
    Entrypoint of this program.

    Adopting ``if __name__ == "__main__"`` pattern and defining ``main()`` function
    simultaneously is **VERY** necessary.

    1. We use :var:`__name__` variable to detect whether the current module is executed
    as a script, not imported as lib.

    2. If we don't define the ``main`` function, any variable declared in the ``if``
    statement will become **GLOBAL**. That may cause some covert errors and bugs.

    Additionally, the `main()` function should not receive any arguments. Startup
    arguments should be written in configuration files.
    """
    requesthub = SleepyRequestHub(
        request_interval=timedelta(seconds=3),
        min_sleep=timedelta(seconds=225),
        max_sleep=timedelta(minutes=90),
        captcha_detector=default_captcha_detector,
    )

    offers_cache_path = CACHE_DIR / "offers.pickle"
    details_cache_path = CACHE_DIR / "details.pickle"

    if offers_cache_path.exists():
        offers_crawler = OffersCrawler.load(offers_cache_path)
        offers_crawler._requesthub = requesthub
    else:
        offers_crawler = OffersCrawler(offers_cache_path, requesthub=requesthub)
    offers = offers_crawler.crawl()

    if details_cache_path.exists():
        details_crawler = DetailsCrawler.load(details_cache_path)
        details_crawler._requesthub = requesthub
    else:
        details_crawler = DetailsCrawler(
            details_cache_path,
            offers,
            requesthub=requesthub,
        )
    details_crawler.crawl()


# Guideline recommended Main Guard
#
# This is VERY necessary to both adopting ``if __name__ == "__main__"`` pattern and
# self-defined ``main()`` function. About more detail, see :func:`main`.
if __name__ == "__main__":
    main()
