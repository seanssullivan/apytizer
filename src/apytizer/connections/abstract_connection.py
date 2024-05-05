# -*- coding: utf-8 -*-
# src/apytizer/connections/abstract_connection.py
"""Abstract connection class.

This module defines an abstract connection class which provides an interface
for subclasses to implement. Each of the abstract methods represents
a standard HTTP request method.

"""

# Standard Library Imports
from __future__ import annotations
import abc
from typing import Any
from typing import Dict
from typing import Optional
from typing import TYPE_CHECKING

# Third-Party Imports
import requests

if TYPE_CHECKING:
    from ..http_methods import HTTPMethod

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

    @abc.abstractmethod
    def head(
        self,
        route: str,
        *,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> requests.Response:
        """Abstract method for sending an HTTP HEAD request.

        Args:
            route: API route to which the request will be sent.
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Additional arguments to pass to request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/HEAD

        """
        raise NotImplementedError

    @abc.abstractmethod
    def get(
        self,
        route: str,
        *,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> requests.Response:
        """Abstract method for sending an HTTP GET request.

        Args:
            route: API route to which the request will be sent.
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Additional arguments to pass to request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/GET

        """
        raise NotImplementedError

    @abc.abstractmethod
    def post(
        self,
        route: str,
        *,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> requests.Response:
        """Abstract method for sending an HTTP POST request.

        Args:
            route: API route to which the request will be sent.
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Additional arguments to pass to request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST

        """
        raise NotImplementedError

    @abc.abstractmethod
    def put(
        self,
        route: str,
        *,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> requests.Response:
        """Abstract method for sending an HTTP PUT request.

        Args:
            route: API route to which the request will be sent.
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Additional arguments to pass to request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PUT

        """
        raise NotImplementedError

    @abc.abstractmethod
    def patch(
        self,
        route: str,
        *,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> requests.Response:
        """Abstract method for sending an HTTP PATCH request.

        Args:
            route: API route to which the request will be sent.
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Additional arguments to pass to request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PATCH

        """
        raise NotImplementedError

    @abc.abstractmethod
    def delete(
        self,
        route: str,
        *,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> requests.Response:
        """Abstract method for sending an HTTP DELETE request.

        Args:
            route: API route to which the request will be sent.
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Additional arguments to pass to request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/DELETE

        """
        raise NotImplementedError

    @abc.abstractmethod
    def options(
        self,
        route: str,
        *,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> requests.Response:
        """Abstract method for sending an HTTP OPTIONS request.

        Args:
            route: API route to which the request will be sent.
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Additional arguments to pass to request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/OPTIONS

        """
        raise NotImplementedError

    @abc.abstractmethod
    def trace(
        self,
        route: str,
        *,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> requests.Response:
        """Abstract method for sending an HTTP TRACE request.

        Args:
            route: API route to which the request will be sent.
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Additional arguments to pass to request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/TRACE

        """
        raise NotImplementedError

    @abc.abstractmethod
    def request(
        self,
        method: HTTPMethod,
        /,
        route: str,
        *,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> requests.Response:
        """Abstract method for sending an HTTP request.

        Args:
            method: HTTP request method to use.
            route: API route to which the request will be sent.
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Additional arguments to pass to request.

        Returns:
            Response object.

        .. _Requests Documentation:
            https://docs.python-requests.org/en/latest/api/

        """
        raise NotImplementedError

    @abc.abstractmethod
    def send(self, request: requests.Request) -> requests.Response:
        """Send an HTTP request."""
        raise NotImplementedError
