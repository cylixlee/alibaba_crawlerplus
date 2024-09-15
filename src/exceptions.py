"""
All possible exceptions the crawler may raise on its own initiative.

Despite the exceptions that may be raised by the standard libraries of Python and
3rd-party libraries, the crawler raises some when encountered with problems. All new
exceptions should be defined here intensively.
"""

from .locators import AbstractUrlLocator

__all__ = ["ElementNotFoundException", "RequestNotSuccessfulException"]


class ElementNotFoundException(Exception):
    """
    Indicates that a desired element of data is not found.
    """

    def __init__(self, name: str, landmark: str | None) -> None:
        """
        :param name: the name of element.
        :param landmark: optional, indicating the uniqueness of this element.
        """
        self.name = name
        self.landmark = landmark

    def __str__(self) -> str:
        builder = [f"element {self.name}"]
        if self.landmark is not None:
            builder.append(f"with {self.landmark}")
        builder.append("is not found")
        return " ".join(builder)


class RequestNotSuccessfulException(Exception):
    """
    Indicates a request to a specific URL is not successful.
    """

    def __init__(self, locator: AbstractUrlLocator) -> None:
        self.locator = locator

    def __str__(self) -> str:
        return f"request of URL {self.locator.locate()} is not successful"
