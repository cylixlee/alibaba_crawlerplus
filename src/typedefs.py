"""
Common helper type definitions.

This module contains several useful type definitions, in order to reduce the length type
annotation and increase flexibility.
"""

from typing import Iterable, TypeVar

__all__ = ["ItemOrIterable"]

# Generic type parameters. No need to export.
T = TypeVar("T")

type ItemOrIterable[T] = T | Iterable[T]
