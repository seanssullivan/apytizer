# -*- coding: utf-8 -*-
# src/apytizer/abstracts/abstract_api.py
"""Abstract API class interface.

This module defines an abstract API class which provides an interface
for subclasses to implement. Each of the abstract methods represents
a standard HTTP request method.

"""

# Standard Library Imports
from __future__ import annotations
import abc
from typing import Tuple, Union

# Third-Party Imports
from requests import Response
from requests.auth import AuthBase

__all__ = ["AbstractAPI"]


class AbstractAPI(abc.ABC):
    """Represents an abstract API."""

    url: str

    def __eq__(self, other: object) -> bool:
        return (
            other.url == self.url and other.auth == self.auth
            if isinstance(other, AbstractAPI)
            else False
        )

    def __hash__(self) -> int:
        return hash(self.url)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__!s} url={self.url!s}>"

    @property
    @abc.abstractmethod
    def auth(self) -> Union[AuthBase, Tuple[str, str], None]:
        """Authentication for API requests."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def url(self) -> str:
        """URL of API."""
        raise NotImplementedError

    @abc.abstractmethod
    def head(self, route: str, *args, **kwargs) -> Response:
        """Abstract method for sending an HTTP HEAD request.

        Args:
            route: API path to which the request will be sent.
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/HEAD

        """
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, route: str, *args, **kwargs) -> Response:
        """Abstract method for sending an HTTP GET request.

        Args:
            route: API path to which the request will be sent.
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/GET

        """
        raise NotImplementedError

    @abc.abstractmethod
    def post(self, route: str, *args, **kwargs) -> Response:
        """Abstract method for sending an HTTP POST request.

        Args:
            route: API path to which the request will be sent.
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST

        """
        raise NotImplementedError

    @abc.abstractmethod
    def put(self, route: str, *args, **kwargs) -> Response:
        """Abstract method for sending an HTTP PUT request.

        Args:
            route: API path to which the request will be sent.
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PUT

        """
        raise NotImplementedError

    @abc.abstractmethod
    def patch(self, route: str, *args, **kwargs) -> Response:
        """Abstract method for sending an HTTP PATCH request.

        Args:
            route: API path to which the request will be sent.
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PATCH

        """
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, route: str, *args, **kwargs) -> Response:
        """Abstract method for sending an HTTP DELETE request.

        Args:
            route: API path to which the request will be sent.
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/DELETE

        """
        raise NotImplementedError

    @abc.abstractmethod
    def options(self, route: str, *args, **kwargs) -> Response:
        """Abstract method for sending an HTTP OPTIONS request.

        Args:
            route: API path to which the request will be sent.
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/OPTIONS

        """
        raise NotImplementedError

    @abc.abstractmethod
    def trace(self, route: str, *args, **kwargs) -> Response:
        """Abstract method for sending an HTTP TRACE request.

        Args:
            route: API path to which the request will be sent.
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/TRACE

        """
        raise NotImplementedError
