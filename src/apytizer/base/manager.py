# -*- coding: utf-8 -*-
# src/apytizer/base/manager.py
"""Base manager class.

This module defines the implementation of a base manager class.

"""

# Standard Library Imports
import logging
from typing import Any, List, Set, Type

# Local Imports
from .. import abstracts
from .. import utils


# Initialize logger.
log = logging.getLogger(__name__)


class BaseManager(abstracts.AbstractManager):
    """
    Implements a base object manager.

    Args:
        endpoint: Endpoint.
        model: Model class.
        objects: Instances of model class.

    """

    def __init__(
        self,
        model: Type[abstracts.AbstractModel],
        endpoint: abstracts.AbstractEndpoint,
        objects: List[abstracts.AbstractModel] = None,
    ):
        if not utils.allinstance(objects, model):
            raise TypeError(f"objects must all be instances of {model}")

        self.model = model
        self.endpoint = endpoint

        # Components
        self.objects = set(objects or [])  # type: Set[abstracts.AbstractModel]

    def add(self, obj: abstracts.AbstractModel) -> None:
        """
        Add an object.

        Args:
            obj: Object to add.

        """

        self.objects.add(obj)

    def _create(self, obj: abstracts.AbstractModel) -> None:
        """
        Create an object.

        Args:
            obj: Object to create.

        """

        data = dict(obj.state)
        self.endpoint.post(data)

    def get(self, ref: Any, *args, **kwargs) -> abstracts.AbstractModel:
        """
        Retrieving an object.

        Args:
            ref: Reference to object.

        Returns:
            Object.

        """

        try:
            result = next(obj for obj in self.objects if obj.reference == ref)
        except StopIteration:
            result = self.endpoint.get(ref, *args, **kwargs)
            self.objects.add(result)
            return result
        else:
            return result

    def list(self, *args, **kwargs) -> List[abstracts.AbstractModel]:
        """
        Retrieving all objects.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            List of objects.

        """

        raise NotImplementedError

    def _update(
        self, obj: abstracts.AbstractModel, *args, **kwargs
    ) -> abstracts.AbstractModel:
        """
        Update object.

        Args:
            obj: Object to update.
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            Updated object.

        """

        raise NotImplementedError

    def remove(self, obj: abstracts.AbstractModel) -> None:
        """
        Remove an object.

        Args:
            obj: Object to remove.

        """

        self.objects.discard(obj)

    def commit(self) -> None:
        """
        Commit changes to objects.

        """

        raise NotImplementedError

    def rollback(self) -> None:
        """
        Roll back changes to objects.

        """

        raise NotImplementedError
