import json
from typing import override

from bs4 import BeautifulSoup, PageElement, ResultSet

from ..conf import CONFIG
from ..datamodels import AlibabaCompanyOffer
from ..exceptions import ElementNotFoundException
from .abstract import AbstractDataParser

__all__ = [
    "AlibabaPageJsonParser",
    "AlibabaJsonOffersParser",
]


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
