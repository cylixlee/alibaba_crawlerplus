from enum import Enum
from typing import Iterable, override

from ..typedefs import ItemOrIterable
from ..urls.abstract import AbstractUrl

__all__ = ["AlibabaSearchTab", "AlibabaSupplierCountry", "AlibabaSearchUrl"]


class AlibabaSearchTab(Enum):
    """
    Tabs of the search result page.

    When we use the search engine inside Alibaba.com, we can filter the results by
    categories. For example, we can only show the regional suppliers related to "smart
    phones" if we specify the tab of :class:`AlibabaSearchUrl` as ``ggs``.
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


class AlibabaSearchUrl(AbstractUrl):
    """
    Object representing Alibaba's search URL.
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
