# -*- coding: utf-8 -*-
# src/apytizer/mappers/base_mapper.py
"""Base Mapper Class.

This module defines the base mapper class implementation.

"""

# Standard Library Imports
from __future__ import annotations
from types import MappingProxyType
from typing import Mapping
from typing import Type

# Local Imports
from .abstract_mapper import AbstractMapper
from ..models import AbstractModel
from ..routes import AbstractRoute

__all__ = ["Mapper"]


class Mapper(AbstractMapper):
    """Implements a mapper.

    Each mapper is an association between a Python class and an API endpoint,
    which allows ORM operations against the class.

    """

    def __new__(
        cls: Type[Mapper],
        __class: Type[AbstractModel],
        __route: AbstractRoute,
        __properties: Mapping[str, str],
        /,
    ) -> Mapper:
        if not issubclass(__class, AbstractModel):  # type: ignore
            message = f"{__class} is not a subclass of 'AbstractModel'"
            raise TypeError(message)

        if not isinstance(__route, AbstractRoute):  # type: ignore
            message = f"expected type 'Route', got {type(__route)} instead"
            raise TypeError(message)

        if not isinstance(__properties, Mapping):  # type: ignore
            expected = "expected type 'Mapping'"
            actual = f"got {type(__properties)} instead"
            message = ", ".join([expected, actual])
            raise TypeError(message)

        instance = super().__new__(cls)  # type: ignore
        return instance

    def __init__(
        self,
        __class: Type[AbstractModel],
        __route: AbstractRoute,
        __properties: Mapping[str, str],
    ) -> None:
        self._class = __class
        self._route = __route
        self._properties = MappingProxyType(__properties)

    @property
    def model(self) -> Type[AbstractModel]:
        """Model."""
        raise NotImplementedError

    @property
    def route(self) -> AbstractRoute:
        """Route."""
        raise NotImplementedError

    @property
    def properties(self) -> Mapping[str, str]:
        """Properties."""
        raise NotImplementedError
