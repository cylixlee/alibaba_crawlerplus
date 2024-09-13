from typing import Iterable, TypeVar

__all__ = ["ItemOrIterable"]

# Generic type parameters. No need to export.
T = TypeVar("T")

type ItemOrIterable[T] = T | Iterable[T]
