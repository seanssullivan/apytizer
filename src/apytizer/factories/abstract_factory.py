# -*- coding: utf-8 -*-
# src/apytizer/factories/abstract_factory.py
"""Abstract factory class interface.

This module defines an abstract factory class which provides an interface for
subclasses to implement.

"""

# Standard Library Imports
import abc

__all__ = ["AbstractFactory"]


class AbstractFactory(abc.ABC):
    """Represents an abstract factory."""
