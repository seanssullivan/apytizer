# -*- coding: utf-8 -*-
# src/apytizer/base/model.py
"""Base model class.

This module defines the implementation of a base model class.

"""

# Standard Library Imports
from __future__ import annotations
from typing import Any
from typing import Mapping
from typing import Union
from typing import TYPE_CHECKING

# Local Imports
from .abstract_model import AbstractModel
from .. import states

if TYPE_CHECKING:
    from ..managers import AbstractManager

__all__ = ["BaseModel"]


class BaseModel(AbstractModel):
    """Implements a base object model.

    Args:
        **kwargs: Data with which to set model state.

    """

    reference: Union[int, str]

    def __init__(self, **kwargs):
        self._state = states.BaseState(kwargs)

    @property
    def manager(self) -> AbstractManager:
        """Manager for model."""
        return getattr(self, "_manager")

    @manager.setter
    def manager(self, manager: AbstractManager) -> None:
        setattr(self, "_manager", manager)

    @manager.deleter
    def manager(self) -> None:
        delattr(self, "_manager")

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

    def __iter__(self):
        yield from self._state.items()

    def __repr__(self) -> str:
        return self.__class__.__name__

    def update(self, __m: Mapping = None, **kwargs) -> None:
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
