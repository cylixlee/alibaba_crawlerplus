"""
Extractors of raw data.

This module is the core functionality of a crawler. We get raw page data from the server,
as the browser does; but we process the website data into structured form, instead of
rendering them into beautiful UIs.

For each page, or even the same page after a while, there may be a specific parser to
crawl all the data out.
"""

import json
from abc import ABC, abstractmethod
from dataclasses import asdict
from typing import override

from bs4 import BeautifulSoup, PageElement, ResultSet
from lxml.etree import HTML, _Element

from .addressing import administrative_address_of
from .configuration import CONFIG
from .datamodels import AlibabaCompanyDetail, AlibabaCompanyOffer
from .exceptions import ElementNotFoundException

__all__ = [
    "AbstractDataParser",
    "ComposeParser",
    "AlibabaPageJsonParser",
    "AlibabaJsonOffersParser",
]


class AbstractDataParser(ABC):
    """
    A parser of a certain type of data.

    This is the core functionality of a crawler: parsing useful parts from a lot of raw
    data and returns as objects. As for different types of data, we shall adopt different
    parsers, which implements the common interface.
    """

    @abstractmethod
    def parse(self, *args, **kwargs) -> object:
        pass


class ComposeParser(AbstractDataParser):
    """
    A utility parser that compose several parsers.

    For example, if the parser is composed of two parsers: :class:`AlibabaPageJsonParser`
    and :class:`AlibabaJsonOffersParser`, then it parses json from the argument (through
    the first parser), and parses offers from JSON returned by the first parser (through
    the second parser).
    """

    def __init__(self, *parsers: AbstractDataParser) -> None:
        self.__parsers = parsers

    @override
    def parse(self, *args, **kwargs) -> object:
        result = self.__parsers[0].parse(*args, **kwargs)
        for parser in self.__parsers[1:]:
            result = parser.parse(result)
        return result


class AlibabaPageJsonParser(AbstractDataParser):
    """
    Parse JSON from Alibaba search page.

    As the legacy code does, we try to extract JSON data from one of the requested HTML's
    script. This is much easier and intuitive than using XPath or Selenium to find
    elements and parse them.

    WARNING: This technique relies on the JSON data, which is more unstable than page
    elements. Please re-check the JSON data when this is not working.

    NOTE: This class is named PageJsonParser, is because it parses JSON from a page.
    """

    @override
    def parse(self, data: bytes | str) -> dict:
        # create html parser
        if isinstance(data, bytes):
            data = data.decode()
        html = BeautifulSoup(data, "html.parser")

        # find the <script> element that contains page data (JSON)
        scripts: ResultSet[PageElement] = html.find_all("script")
        desired_script = None
        for script in scripts:
            if CONFIG["json-parser"]["landmark"] in script.text:
                desired_script = script
                break
        if desired_script is None:
            raise ElementNotFoundException("script", CONFIG["json-parser"]["landmark"])

        # split JSON from JavaScript
        prefix = CONFIG["json-parser"]["prefix"]
        suffix = CONFIG["json-parser"]["suffix"]
        start = desired_script.text.find(prefix) + len(prefix)
        end = desired_script.text.find(suffix)
        # The prefix and suffix contains braces that wrap the JSON content. We need to put
        # them back.
        jsonstr = f"{{{desired_script.text[start:end]}}}"

        return json.loads(jsonstr)


class AlibabaJsonOffersParser(AbstractDataParser):
    """
    Parse offer data from JSON.

    Offers, according to the legacy code, is an important item of page JSON data that we
    rely on. It contains company name, ID, management time and more data accessible from
    company detail pages' URL.

    NOTE: This class is named JsonOffersParser, is because it parses offers from JSON.
    """

    @override
    def parse(self, jsonobj: dict) -> list[AlibabaCompanyOffer]:
        template = CONFIG["json-parser"]["offer-template"]
        offers = []

        # retrieve the offer list JSON
        offerlist = jsonobj
        for path in CONFIG["json-parser"]["offer-list-path"]:
            offerlist = offerlist[path]

        # iterate over JSON list and parse `AlibabaCompanyOffer`s out.
        for offer in offerlist:
            # detail url need to be added with "https" scheme
            detail_url = "https:" + offer[template["detail-url"]]
            obj = AlibabaCompanyOffer(
                detail_url=detail_url,
                name=offer[template["name"]],
                provided_products=offer[template["provided-products"]],
                # domain need to be parsed out
                domain=detail_url.split(".en")[0].split("//")[1],
            )
            # append offer object
            offers.append(obj)
        return offers


def _content_of(html: _Element, xpaths: list[str]) -> str:
    for xpath in xpaths:
        elements: list[_Element] = html.xpath(xpath)
        if elements is not None and len(elements) > 0:
            return elements[0].text
    return ""


class AlibabaXpathCompanyParser(AbstractDataParser):
    """
    Parses :class:`AlibabaCompanyDetail` from pages using XPath.

    There's only several additional fields we need to parse: bills, and administrative
    address.
    """

    @override
    def parse(
        self,
        offer: AlibabaCompanyOffer,
        data: bytes | str,
    ) -> AlibabaCompanyDetail:
        # create LXML parser
        if isinstance(data, bytes):
            data = data.decode()
        html = HTML(data)

        # parse elements
        bill = _content_of(html, CONFIG["xpath"]["bill"])
        address = _content_of(html, CONFIG["xpath"]["address"])
        address_list = administrative_address_of([address, offer.name])

        return AlibabaCompanyDetail(
            administrative_address=address_list,
            bill=bill,
            **asdict(offer),
        )
