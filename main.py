import pathlib

from src.datamodels import AdministrativeArea, AlibabaCompanyOffer
from src.misc.addressing import administrative_units
from src.misc.resuming import DefaultResumableState, transaction

type OffersCrawlerResult = dict[AdministrativeArea, list[AlibabaCompanyOffer]]


class OffersCrawler(DefaultResumableState):
    def __init__(self, path: pathlib.Path) -> None:
        super().__init__(path)
        self._offers: OffersCrawlerResult = {}

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

    @transaction
    def _crawl_area(self, area: AdministrativeArea) -> None:
        pass


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


# Guideline recommended Main Guard
#
# This is VERY necessary to both adopting ``if __name__ == "__main__"`` pattern and
# self-defined ``main()`` function. About more detail, see :func:`main`.
if __name__ == "__main__":
    main()
