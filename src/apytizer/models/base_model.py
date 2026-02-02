# -*- coding: utf-8 -*-
# src/apytizer/base/model.py
"""Base model class.

This module defines the implementation of a base model class.

"""

# Standard Library Imports
from __future__ import annotations
from typing import Any
from typing import Generator
from typing import Hashable
from typing import Mapping
from typing import Tuple

# Local Imports
from .abstract_model import AbstractModel
from .. import states

__all__ = ["BaseModel"]


class BaseModel(AbstractModel):
    """Implements a stateful model.

    Args:
        **kwargs: Data with which to set model state.

    """

    reference: Hashable

    def __init__(self, **kwargs: Any):
        self._state = states.LocalState(kwargs)

    def __contains__(self, key: str) -> bool:
        return key in self._state

    def __eq__(self, other: object) -> bool:
        return (
            other.reference == self.reference
            if isinstance(other, BaseModel)
            else False
        )

    def __hash__(self) -> int:
        return hash(self.reference)

    def __getattr__(self, name: str) -> Any:
        attr = self._state.get(name)
        if not attr:
            cls = self.__class__.__name__
            message = f"type object '{cls!s}' has no attribute '{name!s}'"
            raise AttributeError(message)

        return attr

    def __getitem__(self, key: str) -> Any:
        value = self._state[key]
        return value

    def __iter__(self) -> Generator[Tuple[str, Any], None, None]:
        yield from self._state.items()

    def __repr__(self) -> str:
        return self.__class__.__name__

    def update(self, __m: Mapping[str, Any], **kwargs: Any) -> None:
        """Update local state with provided data.

        Args:
            __m (optional): Mapping with which to update local state.
            **kwargs: Data with which to update local state.

        """
        self._state.update(__m, **kwargs)

    def rollback(self) -> None:
        """Rollback changes to local state."""
        self._state.rollback()

    def save(self) -> None:
        """Save changes to local state."""
        self._state.save()
