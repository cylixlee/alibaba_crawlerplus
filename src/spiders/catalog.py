from typing import Iterable

from scrapy import Request, Spider
from scrapy.http import Response

from ..util import administrative_nodes, alibaba_search_url

__all__ = ["CatalogSpider"]


class CatalogSpider(Spider):
    name = "catalog"
    allowed_domains = ["alibaba.com"]

    def start_requests(self) -> Iterable[Request]:
        for node in administrative_nodes():
            yield Request(alibaba_search_url(node.address), dont_filter=True)

    def parse(self, response: Response):
        pass
