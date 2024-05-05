# -*- coding: utf-8 -*-
# src/apytizer/sessions/abstract_session.py
"""Abstract session class.

This module defines an abstract session class which provides an interface
for subclasses to implement.

"""

# Standard Library Imports
import abc
from typing import TYPE_CHECKING

# Third-Party Imports
import requests
from requests.adapters import HTTPAdapter

if TYPE_CHECKING:
    from ..protocols import Protocol

__all__ = ["AbstractSession"]


class AbstractSession(abc.ABC):
    """Represents an abstract session."""

    @abc.abstractmethod
    def start(self) -> None:
        """Starts session."""
        raise NotImplementedError

    @abc.abstractmethod
    def close(self) -> None:
        """Destroys session."""
        raise NotImplementedError

    @abc.abstractmethod
    def mount(self, protocol: "Protocol", adapter: HTTPAdapter) -> None:
        """Registers a connection adapter to a protocol prefix.

        Args:
            protocol: Protocol prefix on which to mount adapter.
            adapter: HTTP adapter to apply to connection.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def send(
        self, __request: requests.Request, /, **kwargs
    ) -> requests.Response:
        """Send an HTTP request.

        Args:
            __request: Request to send.
            **kwargs: Keyword arguments.

        Returns:
            Response.

        """
        raise NotImplementedError
