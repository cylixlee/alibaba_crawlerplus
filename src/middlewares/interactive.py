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

    def __del__(self) -> None:
        self.driver.quit()  # quits the driver.
