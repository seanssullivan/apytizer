# -*- coding: utf-8 -*-
"""Basic manager class.

This module defines the implementation of a basic manager class.

"""

# Standard Library Imports
import logging
from typing import Any, Set, Type

# Local Imports
from .. import abstracts


# Initialize logger.
log = logging.getLogger(__name__)


class BasicManager(abstracts.AbstractManager):
    """
    Implements a basic object manager.

    Args:
        endpoint: Endpoint.
        model: Model class.

    """

    def __init__(
        self,
        endpoint: abstracts.AbstractEndpoint,
        model: Type[abstracts.AbstractModel],
    ):
        self.endpoint = endpoint
        self.model_class = model

    def create(self, obj: abstracts.AbstractModel) -> None:
        """
        Create an object.

        Args:
            obj: Object.

        """

        data = dict(obj.state)
        self.endpoint.post(data)

    def get(self, ref: Any, *args, **kwargs) -> abstracts.AbstractModel:
        """
        Retrieving an object.

        Args:
            ref: Reference to object.

        Returns:
            Instance of an abstract model subclass.

        """

        try:
            result = next(
                obj
                for obj in self._objects
                if getattr(obj, self._index) == ref
            )
        except StopIteration:
            result = self._endpoint.get(ref, *args, **kwargs)
            return result
        else:
            return result

    def remove(self, obj: abstracts.AbstractModel) -> None:
        """
        Abstract method for removing an object.

        Args:
            obj: Instance of an abstract model subclass.

        """

        self._objects.discard(obj)
