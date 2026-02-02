# -*- coding: utf-8 -*-
# src/apytizer/managers/base_manager.py
"""Base manager class.

This module defines a base implementation of a manager class.

"""

# Standard Library Imports
from __future__ import annotations
import logging
from typing import Any
from typing import Type
from typing import TYPE_CHECKING

# Local Imports
from .abstract_manager import AbstractManager
from ..apis import AbstractAPI
from ..mappers import AbstractMapper

if TYPE_CHECKING:
    from ..models import AbstractModel

__all__ = ["BaseManager"]


# Initialize logger.
log = logging.getLogger(__name__)


class BaseManager(AbstractManager):
    """Base class from which all manager implementations are derived.

    Args:
        __api: API instance.

    Raises:
        TypeError: when argument is not type 'Endpoint'.

    """

    def __new__(
        cls: Type[BaseManager],
        __api: AbstractAPI,
        __mapper: AbstractMapper,
        /,
    ) -> BaseManager:
        if not isinstance(__api, AbstractAPI):  # type: ignore
            message = f"expected type 'WebAPI', got {type(__api)} instead"
            raise TypeError(message)

        if not isinstance(__mapper, AbstractMapper):  # type: ignore
            message = f"expected type 'Mapper', got {type(__mapper)} instead"
            raise TypeError(message)

        instance = super().__new__(cls)  # type: ignore
        return instance

    def __init__(
        self,
        __api: AbstractAPI,
        __mapper: AbstractMapper,
        /,
    ) -> None:
        self._api = __api
        self._mapper = __mapper

    def __repr__(self) -> str:
        result = "<{cls!s}>".format(cls=self.__class__.__name__)
        return result

    def create(self, obj: "AbstractModel", /) -> None:
        """Create an object.

        Args:
            obj: Object to create.

        """
        raise NotImplementedError

    def read(self, ref: Any, /) -> "AbstractModel":
        """Read an object.

        Calls `get` method on associated endpoint to retrieve object data.
        Uses response to instantiate an instance of the managed object class.

        Args:
            ref: Reference to object on endpoint.

        Returns:
            Object instance.

        """
        raise NotImplementedError

    def update(self, obj: "AbstractModel", /) -> None:
        """Update an object.

        Calls `put` method on associated endpoint to update object data.

        Args:
            obj: Object to update.

        """
        raise NotImplementedError

    def delete(self, obj: "AbstractModel", /) -> None:
        """Delete an object.

        Calls `delete` method on associated endpoint to delete the object.

        Args:
            obj: Object to delete.

        """
        raise NotImplementedError
