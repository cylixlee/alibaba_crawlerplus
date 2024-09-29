import time
import weakref

from scrapy import Request, Spider
from scrapy.http import HtmlResponse, Response
from selenium.webdriver import Chrome, ChromeOptions, ChromeService, Remote

from ..conf import CONFIG

__all__ = ["InteractiveCaptchaMiddleware"]


class InteractiveCaptchaMiddleware(object):
    """
    Interactively handles captcha pages (manually or automatically), and returns the
    desired page to the engine.

    Currently, Selenium is adopted to do so. When a captcha page is encountered, this
    middleware controls the browser driver to show the captcha page and verify.
    """

    driver: Remote
    abnormal_state: bool = False

    def __init__(self) -> None:
        # add arguments and experimental options.
        options = ChromeOptions()
        for argument in CONFIG["chrome-driver"]["arguments"]:
            options.add_argument(argument)
        for name, value in CONFIG["chrome-driver"]["experimental-options"].items():
            options.add_experimental_option(name, value)

        # create chrome driver and execute Chrome DevTools Protocol
        #
        # which is possibly some magic script to bypass target sites' crawler check.
        service = ChromeService(executable_path=CONFIG["chrome-driver"]["path"])
        self.driver = Chrome(options, service)
        for cmd, args in CONFIG["chrome-driver"]["cdp-command"]:
            self.driver.execute_cdp_cmd(cmd, args)

        # maximize window to get the page rendered correctly.
        self.driver.maximize_window()
        weakref.finalize(self, lambda d: d.quit(), self.driver)

    def process_response(self, request: Request, response: Response, spider: Spider):
        """
        The core logic of this class.

        When the response contains captcha features, Selenium is used to re-request the
        URL, and get the correct response.
        """
        if _is_captcha(response.body):
            return self._process_captcha(request.url)

    def process_request(self, request: Request, spider: Spider):
        """
        Additional logic to reduce duplicate visit of one page.

        When the captcha catch us, we set the flag :var:`abnormal_state` to ``True``; and
        the next request is handled by Selenium directly. Without this logic, every
        captcha page will be visited twice, which will increase the opportunity to be
        captcha-ed.

        :var:`abnormal_state` is set back to ``False`` when the Selenium does not
        recognize any captcha features.
        """
        if self.abnormal_state:
            return self._process_captcha(request.url)

    def _process_captcha(self, url: str) -> Response:
        self.driver.maximize_window()
        self.driver.get(url)
        while self.driver.current_url != url:
            # detect whether the captcha has caught us
            if _is_captcha(self.driver.page_source):
                self.abnormal_state = True
                print("(de-captcha) waiting for manual verification...")
                time.sleep(5)
            else:
                self.abnormal_state = False
            # wait for the browser to load
            time.sleep(1)
        return HtmlResponse(url=url, body=self.driver.page_source, encoding="utf-8")


def _is_captcha(page_source: str) -> bool:
    return "captcha" in page_source
