"""
Module of producing URLs.

Instead of putting hard-coded URLs all around, producing one according to specific needs
is much more flexible and clear. Additionally, we've preserved some abstract API interface
for possible future extension of this program.

Note that the URL rule of a server may vary from times to times. If the WebAPI of the site
has changed, make sure to adapt the corresponding source to the current situation.
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Iterable, override
from urllib.parse import urlencode

from .typedefs import ItemOrIterable

__all__ = [
    "AbstractUrlLocator",
    "AlibabaSearchTab",
    "AlibabaSupplierCountry",
    "AlibabaSearchUrlLocator",
]


class AbstractUrlLocator(ABC):
    """
    A URL locator.

    Since we're writing crawlers, using URL queries are much easier and intuitive than
    using browser drivers (e.g. Selenium). We can take advantage of RESTless WebAPI to
    obtain certain pages.
    """

    @abstractmethod
    def baseurl(self) -> str:
        """
        Provide a baseurl for requests.

        For example, when we use Baidu to search contents about "China", with some rubbish
        queries trimmed, the URL will be "https://www.baidu.com/s?wd=China".

        Let's break it into two parts ::

            baseurl = "https://www.baidu.com/s"
            queries = {
                "wd": "China",
            }

        :class:`AbstractUrlLocator`s' work is to form the complete URLs from ``baseurl``
        and ``queries``. These two parts are required and cannot be absent.
        """
        pass

    @abstractmethod
    def params(self) -> dict:
        """
        Form a dictionary that can be transformed into URL queries.

        For more detail, see :method:`baseurl`.
        """
        pass

    def locate(self) -> str:
        """
        Produce a complete URL, with queries appended to baseurl.

        This function is not necessary when using 3rd-party libraries like ``requests``.
        :func:`request.get` automatically handles URL production and only requires baseurl
        (to be passed as parameter ``url``) and query dictionary (to be passed as
        parameter ``params``). In that case, just call :method:`baseurl` and
        :method:`params` separately.
        """
        return self.baseurl() + "?" + urlencode(self.params())

    def __str__(self) -> str:
        return self.locate()


class AlibabaSearchTab(Enum):
    """
    Tabs of the search result page.

    When we use the search engine inside Alibaba.com, we can filter the results by
    categories. For example, we can only show the regional suppliers related to "smart
    phones" if we specify the tab of ``AlibabaSearchUrlLocator`` as ``ggs``.
    """

    All = "all"
    Suppliers = "supplier"
    VerifiedManufacturers = "verifiedManufactory"
    RegionalSupplies = "ggs"


class AlibabaSupplierCountry(Enum):
    """
    A filter query parameter for specifying suppliers' country (or countries).

    When the URL is encoded with ``country`` parameter, it will filter the results whose
    supplier is among the given country range. If there's one single country specified,
    for example, China, then there will be only China suppliers' products.

    If there're multiple countries, separated by comma ``,`` (which is then automatically
    url-encoded as ``%2C``), results whose suppliers are among those countries are
    filtered.
    """

    China = "CN"
    France = "FR"
    HongKongChina = "HK"
    India = "IN"
    SouthAfrica = "ZA"
    TaiwanChina = "TW"
    Thailand = "TH"
    UnitedKingdom = "UK"
    UnitedStates = "US"
    Vietnam = "VN"


class AlibabaSearchUrlLocator(AbstractUrlLocator):
    """
    Locator of Alibaba's search URL.

    For more details, see :classmethod:`locate`.
    """

    def __init__(
        self,
        search_text: str,
        *,
        tab: AlibabaSearchTab = AlibabaSearchTab.All,
        country: ItemOrIterable[AlibabaSupplierCountry] | None = None,
        page: int | None = None,
    ) -> None:
        """
        :param search_text: The text to type into the search bar of Alibaba.
        :param tab: The tab to display a specific kind of search results. Defaults to
            ``AlibabaSearchTab.All``.
        :param country: The country (or countries) in which the search results' suppliers
            are located. ``None``, one ``AlibabaSupplierCountry`` object or an Iterable
            object over that are all acceptable.
        """
        self.search_text = search_text
        self.tab = tab
        self.country = country
        self.page = page

    @override
    def baseurl(self) -> str:
        return "https://www.alibaba.com/trade/search"

    @override
    def params(self) -> dict[str, str]:
        """
        Produces Alibaba-recognizable search URL queries.
        """
        params: dict[str, str] = {
            "SearchText": self.search_text,
            "tab": self.tab.value,
        }
        if self.country is not None:
            if isinstance(self.country, Iterable):
                countries = ",".join([c.value for c in self.country])
                params["country"] = countries
            else:
                params["country"] = self.country.value
        if self.page is not None:
            params["page"] = self.page
        return params
