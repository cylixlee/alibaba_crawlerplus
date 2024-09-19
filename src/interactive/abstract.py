from abc import ABC, abstractmethod

__all__ = ["AbstractInteractiveBrowser"]


class AbstractInteractiveBrowser(ABC):
    """
    An interactive browser.

    Instead of imitating browsers to send requests, an instance of interactive browser
    directly manipulates the browser to visit some sites and do some tasks. Compared to
    request hubs, interactive browsers can show captcha page to the user and continue to
    do the scheduled task when the user finish captcha verification.

    Currently, this is implemented using Selenium.
    """

    @abstractmethod
    def perform(self, *args, **kwargs) -> object:
        pass
