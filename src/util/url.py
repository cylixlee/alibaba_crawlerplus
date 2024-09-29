from enum import StrEnum
from typing import Iterable
from urllib.parse import urlencode

__all__ = ["AlibabaSearchTab", "AlibabaSupplierCountry", "alibaba_search_url"]

_BASEURL = "https://www.alibaba.com/trade/search"


class AlibabaSearchTab(StrEnum):
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


class AlibabaSupplierCountry(StrEnum):
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


def alibaba_search_url(
    text: str,
    *,
    tab: AlibabaSearchTab = AlibabaSearchTab.Suppliers,
    country: AlibabaSupplierCountry | None = AlibabaSupplierCountry.China,
    page: int | None = None,
) -> str:
    """
    Creates a search URL of alibaba.

    The form of URL queries may change with time. Please make sure this logic is
    up-to-date.
    """

    # `SearchText` and `tab` fields are necessary.
    params: dict[str, str] = {"SearchText": text, "tab": tab}

    # country can be specified
    if country is not None:
        if isinstance(country, Iterable):
            params["country"] = ",".join(country)
        else:
            params["country"] = country

    # page can be specified
    if page is not None:
        assert page != 0, "page count of alibaba search URL starts from 1"
        params["page"] = page
    return _BASEURL + "?" + urlencode(params)
