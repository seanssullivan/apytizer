# -*- coding: utf-8 -*-
"""Abstract model class interface.

This module defines an abstract model class which provides an interface
for subclasses to implement.

"""

# Standard Library Imports
from __future__ import annotations
import abc
from typing import Mapping


class AbstractModel(abc.ABC):
    """
    Represents an abstract model.

    """

    state: Mapping

    @abc.abstractmethod
    def __eq__(self, other: AbstractModel) -> bool:
        """
        Abstract method for determining whether model is equal to another.

        Returns:
            Whether models are equal.

        """

        raise NotImplementedError

    @abc.abstractmethod
    def __getattr__(self, name: str):
        """
        Abstract method for getting a attribute from state.

        Returns:
            Value of attribute.

        """

        raise NotImplementedError

    @abc.abstractmethod
    def __getitem__(self, name: str):
        """
        Abstract method for getting an item from state.

        Returns:
            Value of item.

        """

        raise NotImplementedError

    @abc.abstractmethod
    def __repr__(self) -> str:
        """
        Abstract method for returning the string representation of the model.

        """

        raise NotImplementedError

    @abc.abstractmethod
    def update(self, __m: Mapping = None, **kwargs) -> None:
        """
        Abstract method for updating model state.

        """

        raise NotImplementedError
