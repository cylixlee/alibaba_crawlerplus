import time
from datetime import timedelta
from typing import override

from tqdm import trange

from ..exceptions import CaptchaException, RequestNotSuccessfulException
from ..urls import AbstractUrl
from .abstract import AbstractRequestHub
from .default import CaptchaDetector, DefaultRequestHub

__all__ = ["SleepyRequestHub"]


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
        captcha_detector: CaptchaDetector | None = None,
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
        self._hub = DefaultRequestHub(request_interval, captcha_detector)
        self._interval = min_sleep

    def sleep(self) -> None:
        seconds = int(self._interval.total_seconds())
        print(f"captcha detected. sleeping for {seconds}s...")
        for _ in trange(seconds, desc="Zz Zz~", leave=False):
            time.sleep(1)

    @override
    def request(self, url: AbstractUrl | str) -> str:
        try:
            return self._hub.request(url)
        except CaptchaException as e:
            print(e)
            while self._interval < self.max_sleep:
                self.sleep()
                try:
                    content = self._hub.request(url)
                    return content
                except CaptchaException:
                    self._interval *= 2
            raise RequestNotSuccessfulException(url, "asleep forever")
