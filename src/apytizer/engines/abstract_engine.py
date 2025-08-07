# -*- coding: utf-8 -*-
# src/apytizer/engines/abstract_engine.py
"""Abstract Engine Class.

This module defines an abstract engine class which provides an interface
for subclasses to implement.

"""

# Standard Library Imports
from __future__ import annotations
import abc
from typing import Optional

# Local Imports
from ..connections import AbstractConnection
from ..protocols import Protocol

__all__ = ["AbstractEngine"]


class AbstractEngine(abc.ABC):
    """Represents an abstract engine."""

    @property
    @abc.abstractmethod
    def protocol(self) -> Optional[Protocol]:
        """Protocol."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def url(self) -> str:
        """Base URL."""
        raise NotImplementedError

    @abc.abstractmethod
    def connect(self) -> AbstractConnection:
        """Establish connection.

        Returns:
            Connection.

        """
        raise NotImplementedError
