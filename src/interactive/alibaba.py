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
    def __init__(self, driver: Remote) -> None:
        self._driver = driver

    @override
    def perform(self, offer: AlibabaCompanyOffer) -> AlibabaCompanyDetail:
        self._driver.maximize_window()
        # open detail page
        self._driver.get(offer.detail_url)
        time.sleep(2)
        # automation_trial = False
        while self._driver.current_url != offer.detail_url:
            # captcha detection
            if "captcha" in self._driver.page_source:
                print("(de-captcha) waiting for manual verification")
                time.sleep(15)
                # if automation_trial:
                #     print("(de-captcha) waiting for manual verification...")
                #     time.sleep(15)
                #     continue

                # retrial = 0
                # while retrial < CONFIG["captcha"]["retry"]:
                #     # try to automate several times.
                #     if "captcha" not in self._driver.page_source:
                #         break

                #     try:
                #         print("(de-captcha) trying to automate verification...")
                #         time.sleep(3)
                #         slider = self._driver.find_element(
                #             By.XPATH,
                #             CONFIG["captcha"]["slider"],
                #         )
                #         # hold the slider
                #         ActionChains(self._driver).click_and_hold(slider).perform()
                #         x = random.randint(
                #             CONFIG["captcha"]["min-slide"],
                #             CONFIG["captcha"]["max-slide"],
                #         )
                #         y = random.randint(-50, 50)
                #         ActionChains(self._driver).move_by_offset(
                #             x, y
                #         ).release().perform()
                #         retrial += 1
                #     except NoSuchElementException:
                #         while retrial < CONFIG["captcha"]["retry"]:
                #             try:
                #                 retry_button = self._driver.find_element(
                #                     By.XPATH,
                #                     CONFIG["captcha"]["retry-button"],
                #                 )
                #                 ActionChains(self._driver).click(retry_button).perform()
                #                 retrial += 1
                #             except NoSuchElementException:
                #                 break
                #         if retrial >= CONFIG["captcha"]["retry"]:
                #             print("sorry, failed to get slider item...")
                #             break
                # automation_trial = True
            # wait for the browser to get prepared
            time.sleep(3)

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

        return AlibabaCompanyDetail(
            bill=bill,
            administrative_address=address,
            **asdict(offer),
        )

    def _xpath_of(self, xpaths: list[str]) -> WebElement | None:
        for xpath in xpaths:
            try:
                return self._driver.find_element(By.XPATH, xpath)
            except NoSuchElementException:
                print(f"(pass) element not found by {xpath}")
        return None
