import time
from datetime import datetime, timedelta
from typing import override

import requests
from bs4 import BeautifulSoup, PageElement, ResultSet

from ..conf import CONFIG
from ..exceptions import CaptchaException, RequestNotSuccessfulException
from ..urls import AbstractUrl
from .abstract import AbstractRequestHub

__all__ = ["DefaultRequestHub"]


def _captcha_blocked(source: str) -> bool:
    for landmark in CONFIG["captcha-detect"]["landmarks"]:
        if landmark not in source:
            return False


class DefaultRequestHub(AbstractRequestHub):
    """
    A single-threaded, interval-based request hub.

    When :method:`request` is called, the request hub checks if the interval between the
    current request and the last one has exceeded the :var:`self.request_interval`. If
    not, the hub sleeps until then.

    Concurrent requesting is not introduced since we don't mind the performance that much.
    If the crawler got banned, it will take much longer to recover.
    """

    def __init__(self, request_interval: timedelta) -> None:
        self.request_interval = request_interval
        self.last_request_time = datetime.now()

    @override
    def request(self, url: AbstractUrl | str) -> str:
        """
        Sends a request to the specified URL. The configured ``disguise-headers`` are used
        as request headers.

        :param url: an instance of :class:`AbstractUrl`, or str representing the URL to
            send a GET request.
        :returns: a str of the response text.
        """

        # if the interval between the current request and the last one does not fulfill
        # the request_interval, sleep some seconds
        next_request_time = self.last_request_time + self.request_interval
        now = datetime.now()
        if now < next_request_time:
            interval = next_request_time - now
            time.sleep(interval.total_seconds() + 1)  # in case the interval is 0.99999s
        self.last_request_time = datetime.now()

        # send request through requests library
        if isinstance(url, AbstractUrl):
            response = requests.get(
                url.baseurl(),
                url.params(),
                headers=CONFIG["disguise-headers"],
            )
        else:
            response = requests.get(url=url)

        if response.status_code != 200:
            raise RequestNotSuccessfulException(url)

        # captcha detection
        html = BeautifulSoup(response.text, "html.parser")
        scripts: ResultSet[PageElement] = html.find_all("script")
        for script in scripts:
            if _captcha_blocked(script.text):
                raise CaptchaException(url)
        return response.text
