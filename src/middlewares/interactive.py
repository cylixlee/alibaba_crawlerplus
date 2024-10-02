import time
import weakref

from scrapy import Request, Spider
from scrapy.http import HtmlResponse, Response
from selenium.webdriver import Chrome, ChromeOptions, ChromeService, Remote

from ..conf import CONFIG

__all__ = ["InteractiveMiddleware"]


class InteractiveMiddleware(object):
    """
    Interactively opens requested pages and returns the desired page to the engine.

    Currently, Selenium is adopted to do so.

    NOTE: This middleware needs the scrapy to be non-concurrent, because we cannot operate
    multiple browser tabs concurrently (for humans and Selenium).
    """

    driver: Remote

    def __init__(self) -> None:
        # add arguments and experimental options.
        options = ChromeOptions()
        for argument in CONFIG["chrome-driver"]["arguments"]:
            options.add_argument(argument)
        for name, value in CONFIG["chrome-driver"]["experimental-options"].items():
            options.add_experimental_option(name, value)

        # create chrome driver and execute Chrome DevTools Protocol (CDP) command
        #
        # which is possibly some magic script to bypass target sites' crawler check.
        service = ChromeService(executable_path=CONFIG["chrome-driver"]["path"])
        self.driver = Chrome(options, service)
        for cmd, args in CONFIG["chrome-driver"]["cdp-command"].items():
            self.driver.execute_cdp_cmd(cmd, args)

        # implicitly waits for dynamically rendered elements.
        self.driver.implicitly_wait(5)
        # maximize window to get the page rendered correctly.
        self.driver.maximize_window()
        weakref.finalize(self, lambda d: d.quit(), self.driver)

    def process_request(self, request: Request, spider: Spider) -> Response:
        self.driver.maximize_window()
        self.driver.get(request.url)
        # detect whether the captcha has caught us
        while "punish" in self.driver.current_url:
            print("(de-captcha) waiting for manual verification...")
            time.sleep(5)
        return HtmlResponse(
            url=request.url,
            body=self.driver.page_source,
            encoding="utf-8",
        )
