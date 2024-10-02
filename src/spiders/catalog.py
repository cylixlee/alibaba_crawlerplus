from typing import Iterable, override

from scrapy import Request, Spider
from scrapy.http import Response

from ..conf import CONFIG
from ..items import Catalog, CatalogItem
from ..util import AdministrativeArea, administrative_nodes, alibaba_search_url

__all__ = ["CatalogSpider"]


class CatalogSpider(Spider):
    """
    Crawls the search results of all nodes of administrative area trees.
    """

    name = "catalog"
    allowed_domains = ["alibaba.com"]

    @override
    def start_requests(self) -> Iterable[Request]:
        # search all node elements of administrative area trees
        #
        # for each area, there should be more requests yielded by the `parse` method, as
        # we only starts with the first pages of a single area's search results.
        for node in administrative_nodes():
            yield Request(alibaba_search_url(node.address), meta={"area": node})

    @override
    def parse(self, response: Response) -> Iterable[Request | CatalogItem]:
        xpaths: dict[str, str] = CONFIG["xpath"]["catalog"]
        area: AdministrativeArea = response.meta["area"]

        # checks if there's next page
        next_page = response.xpath(xpaths["next-page-link"]).extract_first()
        if next_page:
            yield Request(url="https://alibaba.com" + next_page, meta={"area": area})

        # every card contains some information about the supplier
        cards = response.xpath(xpaths["card"])
        for card in cards:
            detail_url = card.xpath(xpaths["detail-url"]).extract_first()
            name = card.xpath(xpaths["name"]).extract_first()
            products = card.xpath(xpaths["products"]).extract_first()  # may be None

            # validate data
            if detail_url is None or name is None:
                continue
            if products is None:
                products = ""

            domain = detail_url.split(".")[0].split("/")[-1]  # the last domain name
            detail_url = "https:" + detail_url
            yield CatalogItem(
                {
                    "catalog": Catalog(detail_url, domain, name, products),
                    "area": area,
                }
            )
