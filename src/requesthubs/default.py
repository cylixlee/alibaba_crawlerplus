import time
from datetime import datetime, timedelta
from typing import Callable, override

import requests
from fake_useragent import UserAgent

from ..exceptions import CaptchaException, RequestNotSuccessfulException
from ..urls import AbstractUrl
from .abstract import AbstractRequestHub

__all__ = [
    "CaptchaDetector",
    "default_captcha_detector",
    "DefaultRequestHub",
]

type CaptchaDetector = Callable[[str], bool]


def default_captcha_detector(content: str) -> bool:
    return "captcha" in content


class DefaultRequestHub(AbstractRequestHub):
    """
    A single-threaded, interval-based request hub.

    When :method:`request` is called, the request hub checks if the interval between the
    current request and the last one has exceeded the :var:`self.request_interval`. If
    not, the hub sleeps until then.

    Concurrent requesting is not introduced since we don't mind the performance that much.
    If the crawler got banned, it will take much longer to recover.
    """

    def __init__(
        self,
        request_interval: timedelta,
        captcha_detector: CaptchaDetector | None = None,
    ) -> None:
        self.request_interval = request_interval
        self.last_request_time = datetime.now()
        self.captcha_detector = captcha_detector
        self.ua = UserAgent()

    @override
    def request(self, url: AbstractUrl | str) -> str:
        """
        Sends a request to the specified URL.

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
                headers={"User-Agent": self.ua.random},
            )
        else:
            response = requests.get(url=url)

        # status code check
        if response.status_code != 200:
            raise RequestNotSuccessfulException(url)

        # (optional) captcha detection
        if self.captcha_detector is not None:
            if self.captcha_detector(response.text):
                raise CaptchaException(url)
        return response.text
