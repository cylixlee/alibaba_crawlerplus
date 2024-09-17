import pprint

from src.configuration import DATA_DIR
from src.datamodels import AlibabaCompanyOffer
from src.parsers import (
    AlibabaJsonOffersParser,
    AlibabaPageJsonParser,
    AlibabaXpathCompanyParser,
    ComposeParser,
)


def main():
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
    with open(DATA_DIR / "sample.html", encoding="utf8") as f:
        data = f.read()
        parser = ComposeParser(
            AlibabaPageJsonParser(),
            AlibabaJsonOffersParser(),
        )
        offers: list[AlibabaCompanyOffer] = parser.parse(data)

    with open(DATA_DIR / "sample-detail.html", encoding="utf8") as f:
        data = f.read()
        parser = AlibabaXpathCompanyParser()
        detail = parser.parse(offers[0], data)
        pprint.pp(detail)


# Guideline recommended Main Guard
#
# This is VERY necessary to both adopting ``if __name__ == "__main__"`` pattern and
# self-defined ``main()`` function. About more detail, see :func:`main`.
if __name__ == "__main__":
    main()
