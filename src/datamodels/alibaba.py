from dataclasses import dataclass

__all__ = ["AlibabaCompanyOffer", "AlibabaCompanyDetail"]


@dataclass
class AlibabaCompanyOffer(object):
    detail_url: str
    name: str
    provided_products: str
    domain: str


@dataclass
class AlibabaCompanyDetail(AlibabaCompanyOffer):
    administrative_address: list[str] | None
    bill: str
