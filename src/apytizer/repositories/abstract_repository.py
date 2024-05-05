# -*- coding: utf-8 -*-
# src/apytizer/repositories/abstract_repository.py
"""Abstract repository class interface.

This module defines an abstract repository class which provides an interface
for subclasses to implement.

"""

# Standard Library Imports
import abc
from typing import Any
from typing import List
from typing import TYPE_CHECKING

# Local Imports
if TYPE_CHECKING:
    from ..models import AbstractModel

__all__ = ["AbstractRepository"]


class AbstractRepository(abc.ABC):
    """Represents an abstract repository."""

    @property
    def objects(self) -> List[AbstractModel]:
        """Objects in repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def add(self, obj: AbstractModel) -> None:
        """Abstract method to add an object to repository.

        This method only adds an object to the local state of the repository.
        New objects are not sent to the associated endpoint until the client
        commits changes to the repository.

        Args:
            obj: Instance of an abstract model subclass.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, ref: Any, *args, **kwargs) -> AbstractModel:
        """Abstract method to get an object from the repository.

        If the object is not found in local state, a request is send to the
        associated endpoint.

        Args:
            ref: Reference to object.
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            Instance of an abstract model subclass.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def remove(self, obj: AbstractModel) -> None:
        """Abstract method to remove an object from repository.

        Args:
            obj: Instance of an abstract model subclass.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def commit(self) -> None:
        """Abstract method for committing changes to objects."""
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self) -> None:
        """Abstract method for rolling back changes to objects."""
        raise NotImplementedError
