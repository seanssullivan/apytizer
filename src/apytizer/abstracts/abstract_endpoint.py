# -*- coding: utf-8 -*-
# src/apytizer/abstracts/abstract_endpoint.py
"""Abstract endpoint class interface.

This module defines an abstract endpoint class which provides an interface
for subclasses to implement. Each of the abstract methods represents
a standard HTTP request method.

"""

# Standard Library Imports
import abc

# Third-Party Imports
from requests import Response

# Local Imports
from .abstract_api import AbstractAPI

__all__ = ["AbstractEndpoint"]


class AbstractEndpoint(abc.ABC):
    """Represents an abstract endpoint."""

    api: AbstractAPI

    @property
    @abc.abstractmethod
    def path(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def __eq__(self, other: object) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def __hash__(self) -> int:
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__!s} path={self.path!s}>"

    def __str__(self) -> str:
        return self.path

    @abc.abstractmethod
    def head(self, *args, **kwargs) -> Response:
        """Abstract method for sending an HTTP HEAD request.

        This method must call the `head` method on the component API instance.

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

        This method must call the `get` method on the component API instance.

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

        This method must call the `post` method on the component API instance.

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

        This method must call the `put` method on the component API instance.

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

        This method must call the `patch` method on the component API instance.

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

        This method must call the `delete` method on the component API instance.

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

        This method must call the `options` method on the component API instance.

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

        This method must call the `trace` method on the component API instance.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/TRACE

        """
        raise NotImplementedError
