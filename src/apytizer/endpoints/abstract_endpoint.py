# -*- coding: utf-8 -*-
# src/apytizer/endpoints/abstract_endpoint.py
"""Abstract endpoint class.

This module defines an abstract endpoint class which provides an interface
for subclasses to implement. Each of the abstract methods represents
a standard HTTP request method.

"""

# Standard Library Imports
import abc
from typing import Optional
from typing import TYPE_CHECKING

# Local Imports
from ..connections import AbstractConnection

if TYPE_CHECKING:
    from ..apis import AbstractAPI

__all__ = ["AbstractEndpoint"]


class AbstractEndpoint(abc.ABC):
    """Represents an abstract endpoint."""

    @property
    @abc.abstractmethod
    def api(self) -> "AbstractAPI":
        """API."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def connection(self) -> Optional[AbstractConnection]:
        """Connection with which to make requests."""
        raise NotImplementedError
