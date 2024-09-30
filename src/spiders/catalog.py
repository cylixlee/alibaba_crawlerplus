from typing import Iterable

from scrapy import Request, Spider
from scrapy.exceptions import DropItem
from scrapy.http import Response

from ..conf import CONFIG
from ..items import CatalogItem
from ..util import AdministrativeArea, administrative_nodes, alibaba_search_url

__all__ = ["CatalogSpider"]


class CatalogSpider(Spider):
    """
    Crawls the search results of all nodes of administrative area trees.
    """

    name = "catalog"
    allowed_domains = ["alibaba.com"]

    def start_requests(self) -> Iterable[Request]:
        # search all node elements of administrative area trees
        #
        # for each area, there should be more requests yielded by the `parse` method, as
        # we only starts with the first pages of a single area's search results.
        for node in administrative_nodes():
            yield Request(alibaba_search_url(node.address))

    def parse(self, response: Response):
        xpaths: dict[str, str] = CONFIG["xpath"]["catalog"]

        # decide area
        area: AdministrativeArea = None
        for node in administrative_nodes():
            if node.address.lower() in response.request.url.lower():
                area = node
                break
        assert area is not None, "unrecognized area"

        # every card contains some information about the supplier
        cards = response.xpath(xpaths["card"])
        for card in cards:
            detail_url = card.xpath(xpaths["detail-url"]).extract_first()
            name = card.xpath(xpaths["name"]).extract_first()
            products = card.xpath(xpaths["products"]).extract_first()  # may be None

            # validate data, set products to an empty string if None
            if not detail_url and not name:
                raise DropItem()
            if not products:
                products = ""

            domain = detail_url.split(".")[0].split("/")[-1]  # the last domain name
            detail_url = "https:" + detail_url
            yield CatalogItem(
                {
                    "detail_url": detail_url,
                    "domain": domain,
                    "name": name,
                    "provided_products": products,
                    "area": area,
                }
            )

        # checks if there's next page
        next_page = response.xpath(xpaths["next-page-link"]).extract_first()
        if next_page:
            yield Request(url="https://alibaba.com" + next_page)
