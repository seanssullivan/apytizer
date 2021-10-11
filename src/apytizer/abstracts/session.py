# -*- coding: utf-8 -*-
"""Abstract session class interface.

This module defines an abstract session class which provides an interface
for subclasses to implement.

"""

# Third-Party Imports
from __future__ import annotations
import abc


class AbstractSession(abc.ABC):
    """
    Represents an abstract session.
    """

    def __enter__(self):
        """
        Starts the session as a context manager.
        """
        self.start()

    def __exit__(self, *args):
        """
        Closes the session as context manager.
        """
        self.close(*args)

    @abc.abstractmethod
    def start(self):
        """Starts the session."""
        raise NotImplementedError

    @abc.abstractmethod
    def close(self):
        """Closes the session."""
        raise NotImplementedError
