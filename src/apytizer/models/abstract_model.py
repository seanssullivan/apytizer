# -*- coding: utf-8 -*-
# src/apytizer/models/abstract_model.py
"""Abstract model class interface.

This module defines an abstract model class which provides an interface
for subclasses to implement.

"""

# Standard Library Imports
from __future__ import annotations
import abc
from typing import Any
from typing import Mapping
from typing import TYPE_CHECKING

# Local Imports
if TYPE_CHECKING:
    from ..managers import AbstractManager
    from ..states import AbstractState

__all__ = ["AbstractModel"]


class AbstractModel(abc.ABC):
    """Represents an abstract model."""

    @property
    def manager(self) -> AbstractManager:
        """Manager for model."""
        return getattr(self, "__manager__")

    @manager.setter
    def manager(self, manager: AbstractManager, /) -> None:
        setattr(self, "__manager__", manager)

    @manager.deleter
    def manager(self) -> None:
        delattr(self, "__manager__")

    @abc.abstractmethod
    def __eq__(self, other: object) -> bool:
        """Abstract method for determining whether model is equal to another.

        Returns:
            Whether models are equal.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def __hash__(self) -> int:
        """Abstract method for returning the hash value of a model.

        Returns:
            Hash value.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def __repr__(self) -> str:
        """Abstract method for returning string representation of model."""
        raise NotImplementedError


class AbstractStatefulModel(AbstractModel):
    """Class represents an abstract stateful model."""

    @property
    @abc.abstractmethod
    def state(self) -> AbstractState:
        """State."""
        raise NotImplementedError

    @abc.abstractmethod
    def __contains__(self, other: object) -> bool:
        """Abstract method for determining whether object in state.

        Returns:
            Whether object in state.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def __getattr__(self, name: str) -> Any:
        """Abstract method for getting an attribute from state.

        Returns:
            Value of attribute.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def __getitem__(self, name: str) -> Any:
        """Abstract method for getting an item from state.

        Returns:
            Value of item.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, __m: Mapping[str, Any], **kwargs: Any) -> None:
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
