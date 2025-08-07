# -*- coding: utf-8 -*-
# src/apytizer/connections/abstract_connection.py
"""Abstract Connection Class.

This module defines an abstract connection class which provides an
interface for subclasses to implement.

"""

# Standard Library Imports
from __future__ import annotations
import abc

__all__ = ["AbstractConnection"]


class AbstractConnection(abc.ABC):
    """Represents an abstract connection."""

    @abc.abstractmethod
    def start(self) -> None:
        """Start connection."""
        raise NotImplementedError

    @abc.abstractmethod
    def close(self) -> None:
        """Close connection."""
        raise NotImplementedError
