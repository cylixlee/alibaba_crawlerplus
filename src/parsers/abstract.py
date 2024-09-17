from abc import ABC, abstractmethod

__all__ = ["AbstractDataParser"]


class AbstractDataParser(ABC):
    """
    A parser of a certain type of data.

    This is the core functionality of a crawler: parsing useful parts from a lot of raw
    data and returns as objects. As for different types of data, we shall adopt different
    parsers, which implements the common interface.
    """

    @abstractmethod
    def parse(self, *args, **kwargs) -> object:
        pass
