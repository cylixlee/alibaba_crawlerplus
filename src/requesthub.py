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

from .conf import CONFIG
from .exceptions import RequestNotSuccessfulException
from .locators import AbstractUrlLocator


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
    def request(self, locator: AbstractUrlLocator) -> str:
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
            time.sleep(interval.seconds + 1)  # incase the interval is 0.99999s
        self.last_request_time = datetime.now()

        # send request through requests library
        response = requests.get(
            locator.baseurl(),
            locator.params(),
            headers=CONFIG["disguise-headers"],
        )
        if response.status_code != 200:
            raise RequestNotSuccessfulException(locator)
        return response.text
