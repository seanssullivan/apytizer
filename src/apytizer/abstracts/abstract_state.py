# -*- coding: utf-8 -*-
# src/apytizer/abstracts/abstract_state.py
"""Abstract state class interface.

This module defines an abstract state class which provides an interface
for subclasses to implement.

"""

# Standard Library Imports
from __future__ import annotations
import abc
from typing import Any, Generator, Mapping

__all__ = ["AbstractState"]


class AbstractState(abc.ABC):
    """Represents an abstract state."""

    @abc.abstractmethod
    def __contains__(self, key: str) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def __eq__(self, other: object) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def __getitem__(self, key: str) -> Any:
        raise NotImplementedError

    @abc.abstractmethod
    def __setitem__(self, key: str, value: Any) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def __iter__(self) -> Generator:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, key: str) -> Any:
        """Abstract method for getting an item from state.

        Args:
            key: Key.

        Returns:
            Value of item.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def items(self) -> Any:
        """Abstract method for getting items from state."""
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, __m: Mapping = None, **kwargs) -> None:
        """Abstract method for updating state.

        Args:
            __m: Mapping.
            **kwargs: Keyword arguments.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self) -> None:
        """Abstract method for rolling back changes to state."""
        raise NotImplementedError

    @abc.abstractmethod
    def save(self) -> None:
        """Abstract method for saving changes to state."""
        raise NotImplementedError
