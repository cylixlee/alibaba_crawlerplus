import pathlib
from datetime import timedelta

from src.datamodels import AdministrativeArea, AlibabaCompanyOffer
from src.misc.addressing import administrative_units
from src.misc.resuming import DefaultResumableState, transaction
from src.parsers import AlibabaJsonOffersParser, AlibabaPageJsonParser, ComposeParser
from src.requesthubs import (
    AbstractRequestHub,
    SleepyRequestHub,
    default_captcha_detector,
)
from src.urls import AlibabaSearchTab, AlibabaSearchUrl, AlibabaSupplierCountry

type OffersCrawlerResult = dict[AdministrativeArea, list[AlibabaCompanyOffer]]

PROJECT_DIR = pathlib.Path(__file__).parent
CACHE_DIR = PROJECT_DIR / "cache"


class OffersCrawler(DefaultResumableState):
    def __init__(self, path: pathlib.Path, *, requesthub: AbstractRequestHub) -> None:
        super().__init__(path)
        self._offers: OffersCrawlerResult = {}
        self._requesthub = requesthub

    def crawl(self) -> OffersCrawlerResult:
        for unit in administrative_units():
            # (kind of) Integrity check.
            #
            # If all units are crawled and cached, this function simply returns the
            # result; otherwise, incremental crawling is performed.
            #
            # This saves a lot of duplicate work and makes this task resumable.
            if unit not in self._offers.keys():
                self._crawl_area(unit)
        return self._offers

    def _crawl_area(self, area: AdministrativeArea) -> None:
        parser = ComposeParser(
            AlibabaPageJsonParser(),
            AlibabaJsonOffersParser(),
        )
        page = 0
        while True:
            url = AlibabaSearchUrl(
                area.address,
                tab=AlibabaSearchTab.Suppliers,
                country=AlibabaSupplierCountry.China,
                page=page,
            )
            content = self._requesthub.request(url)
            offers: list[AlibabaCompanyOffer] = parser.parse(content)
            if not offers:
                break
            print(f"crawled {len(offers)} offers...")
            self._save_offers(area, offers)

    @transaction
    def _save_offers(
        self,
        area: AdministrativeArea,
        offers: list[AlibabaCompanyOffer],
    ) -> None:
        if area not in self._offers.keys():
            offerlist = []
            self._offers[area] = offerlist
        else:
            offerlist = self._offers[area]
        offerlist.extend(offers)


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
    crawler = OffersCrawler(CACHE_DIR / "offers.pickle", requesthub=requesthub)
    crawler.crawl()


# Guideline recommended Main Guard
#
# This is VERY necessary to both adopting ``if __name__ == "__main__"`` pattern and
# self-defined ``main()`` function. About more detail, see :func:`main`.
if __name__ == "__main__":
    main()
