from abc import ABC, abstractmethod

__all__ = ["AbstractRequestHub"]


class AbstractRequestHub(ABC):
    """
    Global manager of all requests that the crawler can send.

    Frequent requests is one of the reason the crawler to be detected and banned. Thus, a
    request manager (or request pool) is necessary. Each implementation of
    :class:`AbstractRequestHub` is responsible for sending request at a relatively low
    frequency.
    """

    @abstractmethod
    def request(self, *args, **kwargs) -> str:
        pass
