from typing import ClassVar

from fake_useragent import UserAgent
from scrapy import Request, Spider


class RandomUserAgentMiddleware(object):
    """
    Replaces ``User-Agent`` fields of all requests using :module:`fake-useragent`.

    Currently, we limit the platform of user-agents to PC, in case the target sites return
    different page sources.
    """

    ua: ClassVar[UserAgent] = UserAgent(platforms="pc")

    def __init__(self) -> None:
        print("RandomUA ready")

    def process_request(self, request: Request, spider: Spider):
        request.headers["User-Agent"] = __class__.ua.random
