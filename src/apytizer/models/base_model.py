# -*- coding: utf-8 -*-
# src/apytizer/base/model.py
"""Base model class.

This module defines the implementation of a base model class.

"""

# Standard Library Imports
from __future__ import annotations
import collections
import logging
from typing import Any, Dict, Generator, Mapping, Union

# Local Imports
from .. import abstracts
from .. import utils

__all__ = ["BaseModel"]


# Initialize logger.
log = logging.getLogger(__name__)


class BaseModel(abstracts.AbstractModel):
    """Implements a base object model.

    Args:
        **kwargs: Data with which to set model state.

    """

    reference: Union[int, str]
    state: abstracts.AbstractState

    def __init__(self, **kwargs):
        self.state = _State(kwargs)

    def __contains__(self, key: str) -> bool:
        return key in self.state

    def __eq__(self, other: object) -> bool:
        return (
            other.reference == self.reference
            if isinstance(other, BaseModel)
            else False
        )

    def __hash__(self) -> int:
        return hash(self.reference)

    def __getattr__(self, name: str) -> Any:
        attr = self.state.get(name)
        if not attr:
            cls = self.__class__.__name__
            message = f"type object '{cls!s}' has no attribute '{name!s}'"
            raise AttributeError(message)

        return attr

    def __getitem__(self, key: str) -> Any:
        value = self.state[key]
        return value

    def __iter__(self):
        yield from self.state.items()

    def __repr__(self) -> str:
        return self.__class__.__name__

    def update(self, __m: Mapping = None, **kwargs) -> None:
        """Update local state with provided data.

        Args:
            __m (optional): Mapping with which to update local state.
            **kwargs: Data with which to update local state.

        """
        self.state.update(__m, **kwargs)

    def rollback(self) -> None:
        """Rollback changes to local state."""
        self.state.rollback()

    def save(self) -> None:
        """Save changes to local state."""
        self.state.save()


class _State(abstracts.AbstractState):
    """Implements a base local state."""

    def __init__(
        self,
        base: Dict[str, Any] = None,
        default: Dict[str, Any] = None,
    ):
        self._state = collections.ChainMap(base or {}, default or {})

    def __contains__(self, key: str) -> bool:
        return key in self._state

    def __eq__(self, other: object) -> bool:
        return (
            dict(other) == dict(self)
            if isinstance(other, abstracts.AbstractState)
            else False
        )

    def __getitem__(self, key: str) -> Any:
        result = utils.deep_get(self._state, key)
        return result

    def __setitem__(self, key: str, value: Any) -> None:
        self._state = utils.deep_set(self._state, key, value)

    def __iter__(self) -> Generator:
        yield from self._state.items()

    def get(self, key: str) -> Any:
        """Get an item from state.

        Args:
            key: Key.

        Returns:
            Value of key in state.

        """
        result = utils.deep_get(self._state, key)
        return result

    def items(self) -> Any:
        """Get items from state."""
        results = self._state.items()
        return results

    def update(self, __m: Mapping = None, **kwargs) -> None:
        """Update state.

        Args:
            __m: Mapping.
            **kwargs: Keyword arguments.

        """
        self._state.update(__m or {}, **kwargs)

    def rollback(self) -> None:
        """Roll back changes to state."""
        self._state.clear()

    def save(self) -> None:
        """Save changes to state."""
        if self._state.maps[0]:
            self._state = self._state.new_child()
