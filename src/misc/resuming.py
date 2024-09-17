"""
State resuming module.

State resuming, similar to Breakpoint Resuming in downloaders, is a technique to recover
unfinished tasks when the service is suddenly down. In this project, we use this module to
declare crawler target lists in case of dying due to unexpected errors and exceptions.

This module declares interface and functions (decorators) to help forming a "resumable
state", which is the minimal unit to recover from storage. For more information, see
:class:`AbstractResumableState`.
"""

import pathlib
import pickle
from abc import ABC, abstractmethod
from functools import wraps
from typing import Self, override

__all__ = [
    "AbstractResumableState",
    "transaction",
    "DefaultResumableState",
]


class AbstractResumableState(ABC):
    """
    An interface of all resumable states.

    This is very useful when it comes to breakpoint resuming, storage and related topics.
    When the service is down, all of its states are stored somehow, and can be loaded back
    when restarted.
    """

    @classmethod
    @abstractmethod
    def load(cls, *args, **kwargs) -> Self:
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


def transaction(method):
    """
    Declare a method of subclass derived from :class:`AbstractResumableState` is a
    transaction.

    In the current implementation, transaction is resumable: every time the method is
    called, the :method:`store` is called once to sync the state locally.
    """

    @wraps(method)
    def action(self: AbstractResumableState, *args, **kwargs):
        result = method(self, *args, **kwargs)
        self.store()
        return result

    return action


class DefaultResumableState(AbstractResumableState):
    """
    The default implementation of a resumable state.

    Currently, this class uses :module:`pickle` to load and store its instances from and
    to binary files. It's the simplest and crudest way to cache data -- the whole Python
    object is cached.

    The modern object-oriented path-operation module :module:`pathlib` in stdlib is
    adopted.
    """

    def __init__(self, path: pathlib.Path) -> None:
        self._cache_path = path

    @classmethod
    @override
    def load(cls, path: pathlib.Path) -> Self:
        with open(path, "rb") as f:
            return pickle.load(f)

    @override
    def store(self) -> None:
        with open(self._cache_path, "wb") as f:
            pickle.dump(self, f)
