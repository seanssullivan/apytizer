# -*- coding: utf-8 -*-
# src/apytizer/base/manager.py
"""Base manager class.

This module defines the implementation of a base manager class.

"""

# Standard Library Imports
import logging
from typing import Any, Callable, List, Set

# Local Imports
from .. import abstracts


# Initialize logger.
log = logging.getLogger(__name__)


class BaseManager(abstracts.AbstractManager):
    """Implements a base object manager.

    Args:
        endpoint: Endpoint.
        factory: Factory which creates objects.

    """

    def __init__(
        self,
        endpoint: abstracts.AbstractEndpoint,
        factory: Callable[..., abstracts.AbstractModel],
    ):
        self.endpoint = endpoint
        self.factory = factory

        # Components
        self.objects = set()  # type: Set[abstracts.AbstractModel]

    def add(self, obj: abstracts.AbstractModel) -> None:
        """Add an object.

        Args:
            obj: Object to add.

        """
        self.objects.add(obj)

    def _create(self, obj: abstracts.AbstractModel) -> None:
        """Create an object.

        Args:
            obj: Object to create.

        """
        data = dict(obj.state)
        self.endpoint.post(data)

    def get(self, ref: Any, *args, **kwargs) -> abstracts.AbstractModel:
        """Retrieving an object.

        Args:
            ref: Reference to object.

        Returns:
            Object.

        """
        try:
            result = next(obj for obj in self.objects if obj.reference == ref)

        except StopIteration:
            response = self.endpoint.get(ref, *args, **kwargs)
            result = self.factory(response)
            self.objects.add(result)
            return result

        else:
            return result

    def list(self, *args, **kwargs) -> List[abstracts.AbstractModel]:
        """Retrieving all objects.

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
        """Update object.

        Args:
            obj: Object to update.
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            Updated object.

        """
        raise NotImplementedError

    def remove(self, obj: abstracts.AbstractModel) -> None:
        """Remove an object.

        Args:
            obj: Object to remove.

        """
        self.objects.discard(obj)

    def commit(self) -> None:
        """Commit changes to objects."""
        raise NotImplementedError

    def rollback(self) -> None:
        """Roll back changes to objects."""
        raise NotImplementedError
