# -*- coding: utf-8 -*-
"""Abstract model class interface.

This module defines an abstract model class which provides an interface
for subclasses to implement.

"""

# Standard Library Imports
from __future__ import annotations
import abc
from typing import Dict


class AbstractModel(abc.ABC):
    """
    Represents an abstract model.
    """
    state: Dict

    @abc.abstractmethod
    def __eq__(self, other: AbstractModel) -> bool:
        """
        Abstract method for determining whether model is equal to another.

        Returns:
            Whether models are equal.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, keys: str, default = None):
        """
        Abstract method for getting model property from state.

        Returns:
            Value of property in model state.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, data: Dict) -> AbstractModel:
        """
        Abstract method for updating model state.

        Returns:
            Updated instance of model.

        """
        raise NotImplementedError
