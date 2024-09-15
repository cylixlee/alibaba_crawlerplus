import json

import requests

from src.conf import CONFIG, DATA_DIR
from src.exceptions import RequestNotSuccessfulException
from src.locators import (
    AlibabaSearchTab,
    AlibabaSearchUrlLocator,
    AlibabaSupplierCountry,
)
from src.parsers import AlibabaPageJsonParser


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

    # Temporary code to fetch contents.
    locator = AlibabaSearchUrlLocator(
        "Hailing",
        tab=AlibabaSearchTab.Suppliers,
        country=AlibabaSupplierCountry.China,
    )
    response = requests.get(
        url=locator.baseurl(),
        params=locator.params(),
        headers=CONFIG["disguise-headers"],
    )

    if response.status_code == 200:
        with open(DATA_DIR / "sample.html", "w", encoding="utf8") as f:
            f.write(response.text)
    else:
        raise RequestNotSuccessfulException(locator)

    # Temporary code to parse page.
    with open(DATA_DIR / "sample.html", encoding="utf8") as f:
        content = f.read()
    parser = AlibabaPageJsonParser()
    with open(DATA_DIR / "sample.json", "w", encoding="utf8") as f:
        jsonobj = parser.parse(content)
        json.dump(jsonobj, f, indent=4)


# Guideline recommended Main Guard
#
# This is VERY necessary to both adopting ``if __name__ == "__main__"`` pattern and
# self-defined ``main()`` function. About more detail, see :func:`main`.
if __name__ == "__main__":
    main()
