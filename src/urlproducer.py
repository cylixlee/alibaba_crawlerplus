"""
Module of producing Alibaba search URLs.

Instead of putting hard-coded URLs all around, producing one according to specific needs
is much more flexible and clear. Additionally, we've preserved some abstract API interface
for possible future extension of this program.

Note that the rule of Alibaba's search engine may vary from times to times. If the WebAPI
of Alibaba has changed, make sure to adapt the corresponding source to the current
situation.
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Iterable, override
from urllib.parse import urlencode

from .typedefs import ItemOrIterable

__all__ = [
    "AbstractUrlProducer",
    "AlibabaSearchTab",
    "AlibabaSupplierCountry",
    "AlibabaSearchUrlProducer",
]


class AbstractUrlProducer(ABC):
    """
    A URL producer.

    Since we're writing crawlers, using URL queries are much easier and intuitive than
    using browser drivers (e.g. Selenium). We can take advantage of RESTless WebAPI to
    obtain certain pages.
    """

    @classmethod
    @abstractmethod
    def produce(cls, **kwargs) -> str: ...


class AlibabaSearchTab(Enum):
    """
    Tabs of the search result page.

    When we use the search engine inside Alibaba.com, we can filter the results by
    categories. For example, we can only show the regional suppliers related to "smart
    phones" if we specify the tab of ``AlibabaSearchUrlProducer`` as ``ggs``.
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


class AlibabaSearchUrlProducer(AbstractUrlProducer):
    """
    Producer of Alibaba's search URL.

    For more details, see :classmethod:`produce`.
    """

    _baseurl = "https://www.alibaba.com/trade/search"

    @classmethod
    @override
    def produce(
        cls,
        search_text: str,
        *,
        tab: AlibabaSearchTab = AlibabaSearchTab.All,
        country: ItemOrIterable[AlibabaSupplierCountry] | None = None,
    ) -> str:
        """
        Produces Alibaba-recognizable search URL.

        :param search_text: The text to type into the search bar of Alibaba.
        :param tab: The tab to display a specific kind of search results. Defaults to
            ``AlibabaSearchTab.All``.
        :param country: The country (or countries) in which the search results' suppliers
            are located. None, one ``AlibabaSupplierCountry`` or an Iterable object of
            that are acceptable.
        """
        params: dict[str, str] = {
            "SearchText": search_text,
            "tab": tab.value,
        }
        if country is not None:
            if isinstance(country, Iterable):
                countries = ",".join([c.value for c in country])
                params["country"] = countries
            else:
                params["country"] = country.value
        return __class__._baseurl + "?" + urlencode(params)
