# -*- coding: utf-8 -*-
# src/apytizer/base/model.py
"""Base model class.

This module defines the implementation of a base model class.

"""

# Standard Library Imports
from __future__ import annotations
import logging
from typing import Any, Mapping, Union

# Local Imports
from .. import abstracts
from .base_state import BaseState

__all__ = ["BaseModel"]


# Initialize logger.
log = logging.getLogger(__name__)


class BaseModel(abstracts.AbstractModel):
    """Implements a base object model.

    Args:
        **kwargs: Data with which to set model state.

    """

    reference: Union[int, str]
    state: BaseState

    def __init__(self, **kwargs):
        self.state = BaseState(kwargs)

    def __contains__(self, key: str) -> bool:
        return key in self.state

    def __eq__(self, other: abstracts.AbstractModel) -> bool:
        return (
            other.reference == self.reference
            if isinstance(other, BaseModel)
            else False
        )

    def __hash__(self) -> str:
        return hash(self.reference)

    def __getattr__(self, name: str) -> Any:
        if not isinstance(name, str):
            message = "attribute name must be a string"
            raise TypeError(message)

        attr = self.state.get(name)
        if not attr:
            cls = self.__class__.__name__
            message = f"type object '{cls!s}' has no attribute '{name!s}'"
            raise AttributeError(message)

        return attr

    def __getitem__(self, key: str) -> Any:
        if not isinstance(key, str):
            message = "argument must be a string"
            raise TypeError(message)

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
        return self

    def rollback(self) -> None:
        """Rollback changes to local state."""
        self.state.rollback()

    def save(self) -> None:
        """Save changes to local state."""
        self.state.save()
