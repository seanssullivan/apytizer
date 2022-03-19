# -*- coding: utf-8 -*-
# src/apytizer/abstracts/abstract_model.py
"""Abstract model class interface.

This module defines an abstract model class which provides an interface
for subclasses to implement.

"""

# Standard Library Imports
from __future__ import annotations
import abc
from typing import Mapping, Union

# Local Imports
from .abstract_state import AbstractState


class AbstractModel(abc.ABC):
    """Represents an abstract model.

    Attributes:
        reference: Unique reference to model.
        state: Local state of model.

    """

    reference: Union[int, str]
    state: AbstractState

    @abc.abstractmethod
    def __eq__(self, other: AbstractModel) -> bool:
        """Abstract method for determining whether model is equal to another.

        Returns:
            Whether models are equal.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def __hash__(self) -> str:
        """Abstract method for returning the hash value of a model.

        Returns:
            Hash value.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def __getattr__(self, name: str):
        """Abstract method for getting an attribute from state.

        Returns:
            Value of attribute.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def __getitem__(self, name: str):
        """Abstract method for getting an item from state.

        Returns:
            Value of item.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def __repr__(self) -> str:
        """Abstract method for returning string representation of model."""
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, __m: Mapping = None, **kwargs) -> None:
        """Abstract method for updating state of model."""
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self) -> None:
        """Abstract method for rolling back changes to state of model."""
        raise NotImplementedError

    @abc.abstractmethod
    def save(self) -> None:
        """Abstract method for saving changes to state of model."""
        raise NotImplementedError
