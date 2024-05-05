# -*- coding: utf-8 -*-
# src/apytizer/states/base_state.py
"""Base state class.

This module defines the implementation of a base state class.

"""

# Standard Library Imports
from __future__ import annotations
import collections
from typing import Any
from typing import Dict
from typing import Generator
from typing import Mapping

# Local Imports
from ..states import AbstractState
from .. import utils

__all__ = ["BaseState"]


class BaseState(AbstractState):
    """Implements a base local state."""

    def __init__(
        self,
        base: Dict[str, Any] = None,
        default: Dict[str, Any] = None,
    ) -> None:
        self._state = collections.ChainMap(base or {}, default or {})

    def __contains__(self, key: str) -> bool:
        return key in self._state

    def __eq__(self, other: object) -> bool:
        return (
            dict(other) == dict(self)
            if isinstance(other, AbstractState)
            else False
        )

    def __getitem__(self, key: str) -> Any:
        result = self.get(key)
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
        if not isinstance(key, str):
            message = f"expected type 'str', got {type(key)} instead"
            raise TypeError(message)

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
