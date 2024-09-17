"""
Module of producing URLs.

Instead of putting hard-coded URLs all around, producing one according to specific needs
is much more flexible and clear. Additionally, we've preserved some abstract API interface
for possible future extension of this program.

Note that the URL rule of a server may vary from times to times. If the WebAPI of the site
has changed, make sure to adapt the corresponding source to the current situation.
"""

from .abstract import *  # noqa: F403
from .alibaba import *  # noqa: F403
