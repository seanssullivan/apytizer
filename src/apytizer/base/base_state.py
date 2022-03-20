# -*- coding: utf-8 -*-
# src/apytizer/base/state.py
"""Base state class.

This module defines the implementation of a base state class.

"""

# Standard Library Imports
from __future__ import annotations
import collections
from typing import Any, Dict, Generator, Mapping

# Local Imports
from .. import abstracts, utils

__all__ = ["BaseState"]


class BaseState(abstracts.AbstractState):
    """Implements a base local state."""

    def __init__(
        self,
        base: Dict[str, Any] = None,
        default: Dict[str, Any] = None,
    ):
        self._state = collections.ChainMap(base or {}, default or {})

    def __contains__(self, key: str) -> bool:
        return key in self._state

    def __eq__(self, other: abstracts.AbstractState) -> bool:
        return (
            dict(other) == dict(self)
            if isinstance(other, self.__class__)
            else False
        )

    def __getitem__(self, key: str) -> Any:
        if not isinstance(key, str):
            raise TypeError(f"key must be str, not {type(key)}")

        result = utils.deep_get(self._state, key)
        return result

    def __setitem__(self, key: str, value: Any) -> None:
        if not isinstance(key, str):
            raise TypeError(f"key must be str, not {type(key)}")

        self._state[key] = value

    def __iter__(self) -> Generator:
        yield from self._state.items()

    @property
    def updates(self) -> Dict[str, Any]:
        """Unsaved changes to state."""
        return {
            key: value
            for key, value in self._state.maps[0].items()
            if value != self._state.parents.get(key)
        }

    def get(self, key: str) -> Any:
        """Get an item from state.

        Args:
            key: Key.

        Returns:
            Value of key in state.

        """
        result = self._state.get(key)
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
