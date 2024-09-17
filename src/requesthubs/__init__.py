"""
Request handlers.

This module contains interface and corresponding implementation of ``RequestHub``s, which
is a concept introduced to resist from banning. The essense of it is to limit the
frequency of requesting (along with disguise headers) to lower down the possibility to get
banned from the host.
"""

from .abstract import *  # noqa: F403
from .default import *  # noqa: F403
from .sleepy import *  # noqa: F403
