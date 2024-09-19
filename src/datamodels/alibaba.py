from dataclasses import dataclass

__all__ = ["AlibabaCompanyOffer", "AlibabaCompanyDetail"]


@dataclass
class AlibabaCompanyOffer(object):
    """
    An structure representing a brief introduction of a company.

    When we crawl data from the search engine of Alibaba, it gives some records, coded as
    ``offerResultList``. We just adopt there naming convention and call this structure
    ``offer``s.
    """

    detail_url: str
    name: str
    provided_products: str
    domain: str


@dataclass
class AlibabaCompanyDetail(AlibabaCompanyOffer):
    """
    A more detailed information of a certain company on Alibaba.

    We can navigate to the :field:`detail_url` of :class:`AlibabaCompanyOffer`s, which
    will open the detail page of a company. Currently, we just collect the administrative
    address and bill flow of the company from this page.
    """

    administrative_address: list[str] | None
    bill: str
