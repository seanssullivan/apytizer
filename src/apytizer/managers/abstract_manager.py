# -*- coding: utf-8 -*-
# src/apytizer/managers/abstract_manager.py
"""Abstract manager class interface.

This module defines an abstract manager class which provides an interface for
subclasses to implement. Each of the abstract methods represents a standard
create, read, update or delete (CRUD) operation.

"""

# Standard Library Imports
import abc
from typing import Any
from typing import TYPE_CHECKING

# Local Imports
if TYPE_CHECKING:
    from ..models import AbstractModel

__all__ = ["AbstractManager"]


class AbstractManager(abc.ABC):
    """Represents an abstract model manager."""

    @abc.abstractmethod
    def create(self, obj: AbstractModel, /) -> None:
        """Abstract method to create an object.

        This method must call the `post` method on an associated endpoint to
        create the object.

        Args:
            obj: Instance of an abstract model subclass.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def read(self, ref: Any, /) -> AbstractModel:
        """Abstract method to 'read' an object.

        This method must call the `get` method on an associated endpoint to
        retrieve object data. The response is used to instantiate an instance
        of the managed object class.

        Args:
            ref: Reference to object on endpoint.

        Returns:
            Instance of an abstract model subclass.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, obj: AbstractModel) -> None:
        """Abstract method to update an object.

        This method must call the `put` method on an associated endpoint to
        update object data.

        Args:
            obj: Instance of an abstract model subclass.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, obj: AbstractModel) -> None:
        """Abstract method to delete an object.

        This method must call the `delete` method on an associated endpoint
        to delete the object.

        Args:
            obj: Instance of an abstract model subclass.

        """
        raise NotImplementedError
