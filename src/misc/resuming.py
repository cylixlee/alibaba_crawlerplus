"""
State resuming module.

State resuming, similar to Breakpoint Resuming in downloaders, is a technique to recover
unfinished tasks when the service is suddenly down. In this project, we use this module to
declare crawler target lists in case of dying due to unexpected errors and exceptions.

This module declares interface and functions (decorators) to help forming a "resumable
state", which is the minimal unit to recover from storage. For more information, see
:class:`AbstractResumableState`.
"""

from abc import ABC, abstractmethod
from functools import wraps
from typing import Self

__all__ = ["AbstractResumableState", "resumable"]


class AbstractResumableState(ABC):
    """
    An interface of all resumable states.

    This is very useful when it comes to breakpoint resuming, storage and related topics.
    When the service is down, all of its states are stored somehow, and can be loaded back
    when restarted.
    """

    @classmethod
    @abstractmethod
    def load(cls) -> Self | None:
        """
        Load the state from somewhere.

        This is a class method since we have no idea dealing with classes with no default
        constructors.
        """
        pass

    @abstractmethod
    def store(self) -> None:
        """
        Stores the current state.

        This function can be called when exiting the program, or finishing a transaction,
        depending on the implementation.
        """
        pass


def resumable(method):
    """
    Declare a method of subclass derived from :class:`AbstractResumableState` is
    resumable.

    In the current implementation, this turns the wrapped method a transaction: every time
    the method is called, the :method:`store` is called once to sync the state locally.
    """

    @wraps(method)
    def transaction(self: AbstractResumableState, *args, **kwargs):
        method(self, *args, **kwargs)
        self.store()

    return transaction
