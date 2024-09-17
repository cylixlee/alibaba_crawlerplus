from abc import ABC, abstractmethod
from urllib.parse import urlencode

__all__ = ["AbstractUrl"]


class AbstractUrl(ABC):
    """
    A URL object.

    Since we're writing crawlers, using URL queries are much easier and intuitive than
    using browser drivers (e.g. Selenium). We can take advantage of RESTless WebAPI to
    obtain certain pages.
    """

    @abstractmethod
    def baseurl(self) -> str:
        """
        Provide a baseurl for requests.

        For example, when we use Baidu to search contents about "China", with some rubbish
        queries trimmed, the URL will be "https://www.baidu.com/s?wd=China".

        Let's break it into two parts ::

            baseurl = "https://www.baidu.com/s"
            queries = {
                "wd": "China",
            }

        :class:`AbstractUrl`s' work is to form the complete URLs from ``baseurl`` and
        ``queries``. These two parts are required and cannot be absent.
        """
        pass

    @abstractmethod
    def params(self) -> dict:
        """
        Form a dictionary that can be transformed into URL queries.

        For more detail, see :method:`baseurl`.
        """
        pass

    def __str__(self) -> str:
        """
        Produce a complete URL, with queries appended to baseurl.

        This function is not necessary when using 3rd-party libraries like ``requests``.
        :func:`request.get` automatically handles URL production and only requires baseurl
        (to be passed as parameter ``url``) and query dictionary (to be passed as
        parameter ``params``). In that case, just call :method:`baseurl` and
        :method:`params` separately.
        """
        return self.baseurl() + "?" + urlencode(self.params())
