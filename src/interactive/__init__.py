"""
An interactive way to crawl data.

Currently, this package contains Selenium-based means to crawl the data, which are very
useful when the captcha verification of the target site is hard to bypass. Adopting
browser manipulating utilities is a good choice.
"""

from .abstract import *  # noqa: F403
from .alibaba import *  # noqa: F403
