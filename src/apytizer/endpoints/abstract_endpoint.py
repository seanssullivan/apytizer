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

# Third-Party Imports
from requests import Response

# Local Imports
from ..connections import AbstractHttpConnection

if TYPE_CHECKING:
    from ..apis import AbstractWebAPI

__all__ = ["AbstractEndpoint"]


class AbstractEndpoint(abc.ABC):
    """Represents an abstract endpoint."""

    @property
    @abc.abstractmethod
    def api(self) -> "AbstractWebAPI":
        """API."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def connection(self) -> Optional[AbstractHttpConnection]:
        """Connection with which to make requests."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def path(self) -> str:
        """Endpoint path."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def url(self) -> str:
        """Endpoint URL."""
        raise NotImplementedError

    @abc.abstractmethod
    def head(self, *args, **kwargs) -> Response:
        """Abstract method for sending an HTTP HEAD request.

        This method must call the `get` method on the parent `API` instance.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/HEAD

        """
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, *args, **kwargs) -> Response:
        """Abstract method for sending an HTTP GET request.

        This method must call the `get` method on the parent `API` instance.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/GET

        """
        raise NotImplementedError

    @abc.abstractmethod
    def post(self, *args, **kwargs) -> Response:
        """Abstract method for sending an HTTP POST request.

        This method must call the `post` method on the parent `API` instance.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST

        """
        raise NotImplementedError

    @abc.abstractmethod
    def put(self, *args, **kwargs) -> Response:
        """Abstract method for sending an HTTP PUT request.

        This method must call the `put` method on the parent `API` instance.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PUT

        """
        raise NotImplementedError

    @abc.abstractmethod
    def patch(self, *args, **kwargs) -> Response:
        """Abstract method for sending an HTTP PATCH request.

        This method must call the `patch` method on the parent `API` instance.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PATCH

        """
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, *args, **kwargs) -> Response:
        """Abstract method for sending an HTTP DELETE request.

        This method must call the `delete` method on the parent `API` instance.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/DELETE

        """
        raise NotImplementedError

    @abc.abstractmethod
    def options(self, *args, **kwargs) -> Response:
        """Abstract method for sending an HTTP OPTIONS request.

        This method must call the `options` method on the parent `API` instance.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/OPTIONS

        """
        raise NotImplementedError

    @abc.abstractmethod
    def trace(self, *args, **kwargs) -> Response:
        """Abstract method for sending an HTTP TRACE request.

        This method must call the `trace` method on the parent `API` instance.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/TRACE

        """
        raise NotImplementedError
