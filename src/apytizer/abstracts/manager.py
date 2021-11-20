# -*- coding: utf-8 -*-
"""Abstract manager class interface.

This module defines an abstract manager class which provides an interface for
subclasses to implement.

Managers are abstractions around API endpoints. They translate changes made to
objects in local state into requests to the API endpoint. Each of the abstract
methods represents a standard create, read, update or delete (CRUD) operation.

"""

# Standard Library Imports
import abc
from typing import List

# Local Imports
from .endpoint import AbstractEndpoint
from .model import AbstractModel


class AbstractManager(abc.ABC):
    """
    Represents an abstract manager.

    """

    endpoint: AbstractEndpoint
    model_class = AbstractModel

    def __hash__(self) -> int:
        return hash(self.endpoint)

    def __repr__(self) -> str:
        return '<{cls!s} endpoint={endpoint!s} model={model!s}>'.format(
            cls=self.__class__.__name__,
            endpoint=self.endpoint,
            model=self.model_class.__class__.__name__,
        )

    @abc.abstractmethod
    def create(self, obj: AbstractModel) -> None:
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
    def select(self, *args, **kwargs) -> List[AbstractModel]:
        """
        Abstract method for selecting multiple objects.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            List of abstract model subclass instances.

        """

        raise NotImplementedError

    @abc.abstractmethod
    def update(self, obj: AbstractModel, *args, **kwargs) -> AbstractModel:
        """
        Abstract method for updating objects.

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
