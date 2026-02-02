# -*- coding: utf-8 -*-
# src/apytizer/apis/abstract_api.py
"""Abstract API Class.

This module defines an abstract API class which provides an interface
for subclasses to implement.

"""

# Standard Library Imports
from __future__ import annotations
import abc
from typing import Optional

# Local Imports
from ..connections import AbstractConnection

__all__ = ["AbstractAPI"]


class AbstractAPI(abc.ABC):
    """Represents an abstract API."""

    @property
    @abc.abstractmethod
    def connection(self) -> Optional[AbstractConnection]:
        """Connection with which to make requests."""
        raise NotImplementedError

    @abc.abstractmethod
    def __eq__(self, other: object) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def __hash__(self) -> int:
        raise NotImplementedError
