import json
from abc import ABC, abstractmethod
from typing import override

from bs4 import BeautifulSoup, PageElement, ResultSet

from src.conf import CONFIG
from src.exceptions import ElementNotFoundException

__all__ = [
    "AbstractPageParser",
    "AlibabaPageJsonParser",
]


class AbstractPageParser(ABC):
    """
    A parser of a certain page.

    This is the core functionality of a crawler: parsing useful data from a lot of page
    source and returns as objects. As for different pages, we shall adopt different
    parsers, which implements a common interface.
    """

    @abstractmethod
    def parse(self, *args, **kwargs) -> object:
        pass


class AlibabaPageJsonParser(AbstractPageParser):
    """
    Parse Alibaba data from JSON.

    As the legacy code does, we try to extract JSON data from one of the requested HTML's
    script. This is much easier and intuitive than using XPath or Selenium to find
    elements and parse them.

    WARNING: This technique relies on the JSON data, which is more unstable than page
    elements. Please re-check the JSON data when this is not working.
    """

    @override
    def parse(self, data: bytes | str) -> object:
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
