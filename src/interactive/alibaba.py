import time
from dataclasses import asdict
from typing import override

from selenium.common import NoSuchElementException
from selenium.webdriver import Remote
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from ..conf import CONFIG
from ..datamodels import AlibabaCompanyDetail, AlibabaCompanyOffer
from ..misc.addressing import administrative_address_of
from .abstract import AbstractInteractiveBrowser

__all__ = ["AlibabaDetailPageBrowser"]


class AlibabaDetailPageBrowser(AbstractInteractiveBrowser):
    """
    A interactive browser of Alibaba's company detail page.

    As for now, Alibaba takes a strict watch on detail pages. We can use simple GET
    requests to crawl data from the search engine, but never the detail page. Captcha will
    catch 'ya.

    This class performs interactive crawling when a :class:`AlibabaCompanyOffer` is passed
    in, and waits for manual verification when "captcha" string is found in the source of
    the current page. :class:`ActionChain` of Selenium framework was adopted but couldn't
    bypass the detection of Alibaba.

    According to the data model of :class:`AlibabaCompanyDetail`, it just needs to crawl 2
    more items in the detail page: the bill flow and the administrative address. The Xpath
    of the 2 elements are described in configuration file, and the 2 items are left empty
    when not found.
    """

    def __init__(self, driver: Remote) -> None:
        self._driver = driver

    @override
    def perform(self, offer: AlibabaCompanyOffer) -> AlibabaCompanyDetail:
        self._driver.maximize_window()
        # open detail page
        self._driver.get(offer.detail_url)
        while self._driver.current_url != offer.detail_url:
            # error detection
            if "error" in self._driver.current_url:
                return AlibabaCompanyDetail("", "", "", "", None, "", "")
            # captcha detection
            if "captcha" in self._driver.page_source:
                print("(de-captcha) waiting for manual verification")
                time.sleep(5)
            # wait for the browser to get prepared
            time.sleep(1)

        # find bill, or set to an empty string
        bill = self._xpath_of(CONFIG["xpath"]["bill"])
        if bill:
            bill = bill.text
        else:
            bill = ""

        # find and parse address, or set to None
        address = self._xpath_of(CONFIG["xpath"]["address"])
        if address:
            address = administrative_address_of([address.text, offer.name])
        else:
            address = None

        # find orders
        orders = self._xpath_of(CONFIG["xpath"]["orders"])
        if orders:
            orders = orders.text
        else:
            orders = ""

        return AlibabaCompanyDetail(
            bill=bill,
            administrative_address=address,
            orders=orders,
            **asdict(offer),
        )

    def _xpath_of(self, xpaths: list[str]) -> WebElement | None:
        for xpath in xpaths:
            try:
                return self._driver.find_element(By.XPATH, xpath)
            except NoSuchElementException:
                print(f"(pass) element not found by {xpath}")
        return None
