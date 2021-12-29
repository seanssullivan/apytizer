# -*- coding: utf-8 -*-
# src/apytizer/abstracts/manager.py
"""Abstract manager class interface.

This module defines an abstract manager class which provides an interface for
subclasses to implement.

Managers are abstractions around API endpoints. They translate changes made to
objects in local state into requests to the API endpoint. Each of the abstract
methods represents a standard create, read, update or delete (CRUD) operation.

"""

# Standard Library Imports
import abc
from typing import List, Set

# Local Imports
from .endpoint import AbstractEndpoint
from .model import AbstractModel


class AbstractManager(abc.ABC):
    """
    Represents an abstract manager.

    """

    model = AbstractModel
    endpoint: AbstractEndpoint
    objects: Set[AbstractModel]

    def __hash__(self) -> int:
        return hash((self.model, self.endpoint))

    def __repr__(self) -> str:
        return "<{cls!s} endpoint={endpoint!s} model={model!s}>".format(
            cls=self.__class__.__name__,
            endpoint=self.endpoint,
            model=self.model.__class__.__name__,
        )

    @abc.abstractmethod
    def add(self, obj: AbstractModel) -> None:
        """
        Abstract method for adding an object.

        Args:
            obj: Instance of an abstract model subclass.

        """

        raise NotImplementedError

    @abc.abstractmethod
    def _create(self, obj: AbstractModel) -> None:
        """
        Abstract method for creating an object.

        Args:
            obj: Instance of an abstract model subclass.

        """

        raise NotImplementedError

    @abc.abstractmethod
    def get(self, *args, **kwargs) -> AbstractModel:
        """
        Abstract method for retrieving an object.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            Instance of an abstract model subclass.

        """

        raise NotImplementedError

    @abc.abstractmethod
    def list(self, *args, **kwargs) -> List[AbstractModel]:
        """
        Abstract method for retrieving multiple objects.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            List of abstract model subclass instances.

        """

        raise NotImplementedError

    @abc.abstractmethod
    def _update(self, obj: AbstractModel, *args, **kwargs) -> AbstractModel:
        """
        Abstract method for updating an object.

        Args:
            obj: Instance of an abstract model subclass.
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            Updated instance of an abstract model subclass.

        """

        raise NotImplementedError

    @abc.abstractmethod
    def remove(self, obj: AbstractModel) -> None:
        """
        Abstract method for removing an object.

        Args:
            obj: Instance of an abstract model subclass.

        """

        raise NotImplementedError

    @abc.abstractmethod
    def commit(self) -> None:
        """
        Abstract method for committing changes to objects.

        """

        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self) -> None:
        """
        Abstract method for rolling back changes to objects.

        """

        raise NotImplementedError
