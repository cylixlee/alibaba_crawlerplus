"""
Data Models.

This module contains class definitions of different types of data. More specifically, raw
data are parsed, through the parsers, into the form of class objects. Data models are the
classes of the parsed data.

Data models are defined as dataclasses.
"""

from dataclasses import dataclass

__all__ = ["AlibabaCompanyOffer"]


@dataclass
class AlibabaCompanyOffer(object):
    detail_url: str
    name: str
    provided_products: str
    domain: str
