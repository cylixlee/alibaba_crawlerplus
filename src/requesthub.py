"""
Request handlers.

This module contains interface and corresponding implementation of ``RequestHub``s, which
is a concept introduced to resist from banning. The essense of it is to limit the
frequency of requesting (along with disguise headers) to lower down the possibility to get
banned from the host.
"""

import time
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import override

import requests
from bs4 import BeautifulSoup, PageElement, ResultSet

from .conf import CONFIG
from .exceptions import CaptchaException, RequestNotSuccessfulException
from .locators import AbstractUrlLocator


def _captcha_blocked(source: str) -> bool:
    for landmark in CONFIG["captcha-detect"]["landmarks"]:
        if landmark not in source:
            return False


class AbstractRequestHub(ABC):
    """
    Global manager of all requests that the crawler can send.

    Frequent requests is one of the reason the crawler to be detected and banned. Thus, a
    request manager (or request pool) is necessary. Each implementation of
    :class:`AbstractRequestHub` is responsible for sending request at a relatively low
    frequency.
    """

    @abstractmethod
    def request(self, *args, **kwargs) -> str:
        pass


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
    def request(self, locator: AbstractUrlLocator | str) -> str:
        """
        Sends a request to the specified URL. The configured ``disguise-headers`` are used
        as request headers.

        :param locator: an instance of :class:`AbstractUrlLocator` to locate the URL.
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
        if isinstance(locator, AbstractUrlLocator):
            response = requests.get(
                locator.baseurl(),
                locator.params(),
                headers=CONFIG["disguise-headers"],
            )
        else:
            response = requests.get(url=locator)

        if response.status_code != 200:
            raise RequestNotSuccessfulException(locator)

        # captcha detection
        html = BeautifulSoup(response.text, "html.parser")
        scripts: ResultSet[PageElement] = html.find_all("script")
        for script in scripts:
            if _captcha_blocked(script.text):
                raise CaptchaException(locator)
        return response.text


class SleepyRequestHub(AbstractRequestHub):
    """
    Sleeps when received :class:`CaptchaException`, raises
    :class:`RequestNotSuccessfulException` if sleep time exceeds the maximum sleep period.

    This is a very simple and crude RequestHub: it does not use proxies to resist captcha,
    it just sleeps until that disappears. The sleep interval is self-adaptive.
    """

    def __init__(
        self,
        request_interval: timedelta,
        min_sleep: timedelta,
        max_sleep: timedelta,
    ) -> None:
        """
        :param request_interval: the interval between requests if it's not blocked.
        :param min_sleep: the mininum, **non-ZERO** time to sleep when encountered with
            captcha.
        :param max_sleep: the maximum time to sleep when encountered with captcha.
        """
        assert min_sleep.total_seconds() != 0
        self.request_interval = request_interval
        self.max_sleep = max_sleep
        self.__hub = DefaultRequestHub()
        self.__interval = min_sleep

    @override
    def request(self, locator: AbstractUrlLocator | str) -> str:
        try:
            return self.__hub.request(locator)
        except CaptchaException:
            while self.__interval < self.max_sleep:
                time.sleep(self.__interval.total_seconds())
                try:
                    content = self.__hub.request(locator)
                    return content
                except CaptchaException:
                    self.__interval *= 2
            raise RequestNotSuccessfulException(locator, "asleep forever")
