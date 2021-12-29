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
from .state import BaseState


# Initialize logger.
log = logging.getLogger(__name__)


class BaseModel(abstracts.AbstractModel):
    """
    Implements a base object model.

    Args:
        **kwargs: Data with which to set model state.

    """

    reference: Union[int, str]
    state: BaseState

    def __init__(self, **kwargs):
        self.state = BaseState(kwargs)

    def __contains__(self, key: str) -> bool:
        """
        Check whether key exists in model state.

        Args:
            key: Key.

        Returns:
            Whether key exists.

        """

        return key in self.state

    def __eq__(self, other: abstracts.AbstractModel) -> bool:
        """
        Check whether two models are equal.

        Args:
            other: Another instance of a model.

        Returns:
            Whether models are equal.

        """

        return other.reference == self.reference

    def __hash__(self) -> str:
        return hash(self.reference)

    def __getattr__(self, name: str) -> Any:
        """
        Get attribute from local state.

        Args:
            name: Name of attribute.

        Returns:
            Value of attribute in state.

        """

        if not isinstance(name, str):
            raise TypeError("attribute name must be a string")

        attr = self.state.get(name)
        if not attr:
            cls = self.__class__.__name__
            message = f"type object '{cls!s}' has no attribute '{name!s}'"
            raise AttributeError(message)

        return attr

    def __getitem__(self, key: str) -> Any:
        """
        Get item from local state.

        Function allows lookups even within nested dictionaries. When passed
        multiple keys, separated by periods, the function looks up each key
        in sequence.

        Args:
            key: Key(s) to use to retrieve value.

        Returns:
            Value for key in state.

        """

        if not isinstance(key, str):
            raise TypeError("argument must be a string")

        value = self.state[key]
        return value

    def __iter__(self):
        yield from self.state.items()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.state!s})"

    def rollback(self) -> None:
        """
        Rollback changes to local state.

        """

        self.state.rollback()

    def save(self) -> None:
        """Save changes to local state."""

        self.state.save()

    def update(self, __m: Mapping = None, **kwargs) -> None:
        """
        Update local state of model with provided data.

        Args:
            __m (optional): Mapping with which to update local state.
            **kwargs: Data with which to update local state.

        """

        self.state.update(__m, **kwargs)

        return self
