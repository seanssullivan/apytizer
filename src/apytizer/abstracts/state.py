# -*- coding: utf-8 -*-
# src/apytizer/abstracts/state.py
"""Abstract state class interface.

This module defines an abstract state class which provides an interface
for subclasses to implement.

"""

# Standard Library Imports
from __future__ import annotations
import abc
from typing import Any, Dict, Generator, Mapping


class AbstractState(abc.ABC):
    """
    Represents an abstract state.

    """

    @abc.abstractmethod
    def __contains__(self, key: str) -> bool:
        """
        Abstract method for checking whether a key exists in state.

        Args:
            key: Key.

        Returns:
            Whether key exists.

        """

        raise NotImplementedError

    @abc.abstractmethod
    def __eq__(self, other: AbstractState) -> bool:
        """
        Abstract method for determining whether state is equal to another.

        Returns:
            Whether states are equal.

        """

        raise NotImplementedError

    @abc.abstractmethod
    def __getitem__(self, key: str) -> Any:
        """
        Abstract method for getting an item from state.

        Args:
            key: Key.

        Returns:
            Value of item.

        """

        raise NotImplementedError

    @abc.abstractmethod
    def __setitem__(self, key: str, value: Any) -> None:
        """
        Abstract method for setting an item in state.

        Args:
            key: Key.
            value: Value.

        """

        raise NotImplementedError

    @abc.abstractmethod
    def __iter__(self) -> Generator:
        """Abstract method for iterating over key-value pairs in state."""

        raise NotImplementedError

    @property
    @abc.abstractmethod
    def updates(self) -> Dict[str, Any]:
        """Abstract property for unsaved changes to state."""

        raise NotImplementedError

    @abc.abstractmethod
    def get(self, key: str) -> Any:
        """
        Abstract method for getting an item from state.

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
        """
        Abstract method for updating state.

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
