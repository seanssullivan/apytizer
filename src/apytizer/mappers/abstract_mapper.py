# -*- coding: utf-8 -*-
# src/apytizer/mappers/abstract_mapper.py
"""Abstract mapper class interface.

This module defines an abstract mapper class which provides an interface for
subclasses to implement.

"""

# Standard Library Imports
import abc
from typing import Mapping
from typing import Type
from typing import TYPE_CHECKING

# Local Imports
if TYPE_CHECKING:
    from ..models import AbstractModel
    from ..routes import AbstractRoute

__all__ = ["AbstractMapper"]


class AbstractMapper(abc.ABC):
    """Represents an abstract mapper.

    Each mapper is an association between a Python class and an API endpoint,
    which allows ORM operations against the class.

    """

    @property
    @abc.abstractmethod
    def model(self) -> Type["AbstractModel"]:
        """Model class."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def route(self) -> "AbstractRoute":
        """Routes."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def properties(self) -> Mapping[str, str]:
        """Properties."""
        raise NotImplementedError
