"""
Data models.

This module contains class definitions of different types of data. More specifically, raw
data are parsed, through the parsers, into the form of class objects. Data models are the
classes of the parsed data.

Data models are defined as dataclasses.
"""

from dataclasses import dataclass
from typing import Optional

__all__ = [
    "AlibabaCompanyOffer",
    "AlibabaCompanyDetail",
    "AdministrativeArea",
]


@dataclass
class AlibabaCompanyOffer(object):
    detail_url: str
    name: str
    provided_products: str
    domain: str


@dataclass
class AlibabaCompanyDetail(AlibabaCompanyOffer):
    city: str
    district: str
    bill: str


@dataclass
class AdministrativeArea(object):
    address: str
    name: str
    parent: Optional["AdministrativeArea"]
    children: list["AdministrativeArea"]
