"""
Extractors of raw data.

This module is the core functionality of a crawler. We get raw page data from the server,
as the browser does; but we process the website data into structured form, instead of
rendering them into beautiful UIs.

For each page, or even the same page after a while, there may be a specific parser to
crawl all the data out.
"""

from .abstract import *  # noqa: F403
from .alibaba import *  # noqa: F403
from .compose import *  # noqa: F403
