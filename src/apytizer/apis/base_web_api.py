# -*- coding: utf-8 -*-
# src/apytizer/apis/base_api.py
"""Base Web API class.

This module defines the base web API class implementation.

"""

# Standard Library Imports
from __future__ import annotations
from typing import Any
from typing import Dict
from typing import final
from typing import Optional
from typing import Type

# Third-Party Imports
import requests

# Local Imports
from .abstract_web_api import AbstractWebAPI
from ..connections import AbstractHttpConnection
from ..endpoints import AbstractEndpoint
from ..endpoints import BaseEndpoint
from ..engines import AbstractEngine
from ..routes import AbstractRoute
from .. import errors

__all__ = ["BaseWebAPI"]


class BaseWebAPI(AbstractWebAPI):
    """Base class from which all web API implementations are derived.

    Args:
        __engine: Engine.
        endpoints (optional): Endpoints. Default ``None``.

    """

    def __new__(cls, __engine: object, /, endpoints: Any = None) -> BaseWebAPI:
        if not isinstance(__engine, AbstractEngine):
            message = f"expected type 'Engine', got {type(__engine)} instead"
            raise TypeError(message)

        if endpoints and not isinstance(endpoints, dict):
            message = f"expected type 'dict', got {type(endpoints)} instead"
            raise TypeError(message)

        instance = super().__new__(cls)
        return instance

    def __init__(
        self,
        __engine: AbstractEngine,
        /,
        endpoints: Optional[Dict[AbstractRoute, Type[BaseEndpoint]]] = None,
    ) -> None:
        self._engine = __engine
        self._endpoints = endpoints.copy() if endpoints else {}

    @property
    def connection(self) -> Optional[AbstractHttpConnection]:
        """Connection with which to make requests."""
        result = getattr(self, "_connection", None)
        return result

    @property
    def url(self) -> str:
        """Base URL."""
        return self._engine.url

    @final
    def __enter__(self) -> AbstractWebAPI:
        """Starts API as context manager."""
        self.connect()
        return self

    @final
    def __exit__(self, *_) -> None:
        """Ends API as context manager."""
        self.close()

    def __eq__(self, other: object) -> bool:
        result = (
            other.url.strip("/").lower() == self.url.strip("/").lower()
            if isinstance(other, AbstractWebAPI)
            else False
        )
        return result

    def __hash__(self) -> int:
        result = hash(self.url)
        return result

    def __repr__(self) -> str:
        result = f"<{self.__class__.__name__!s} url={self.url!s}>"
        return result

    def __getitem__(self, path: str) -> AbstractEndpoint:
        """Get endpoint.

        Args:
            path: Relative path of endpoint.

        Returns:
            Endpoint.

        """
        result = self._get_endpoint(path)
        return result

    def __truediv__(self, path: str) -> AbstractEndpoint:
        """Get endpoint.

        Args:
            path: Relative path of endpoint.

        Returns:
            Endpoint.

        """
        result = self._get_endpoint(path)
        return result

    def _get_endpoint(self, path: str) -> AbstractEndpoint:
        """Get endpoint.

        Arhs:
            path: Relative path of endpoint.

        Returns:
            Endpoint.

        """
        try:
            matches = sorted(
                (route, endpoint)
                for route, endpoint in self._endpoints.items()
                if route == path
            )
            _, endpoint = next(iter(matches))

        except StopIteration:
            endpoint = BaseEndpoint

        result = endpoint(self, path)
        return result

    def connect(self) -> None:
        """Start connection to web API."""
        setattr(self, "_connection", self._engine.connect())
        self.connection.start()

    def close(self) -> None:
        """Close connection to web API."""
        self.connection.close()
        delattr(self, "_connection")

    @final
    def head(
        self,
        *,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> requests.Response:
        """Sends an HTTP HEAD request to the API.

        Args:
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Keyword arguments to include in request.

        Returns:
            Response object.

        Raises:
            ConnectionNotStarted: when connection not started.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/HEAD

        """
        if self.connection is None:
            message = "connection not started before making HEAD request"
            raise errors.ConnectionNotStarted(message)

        response = self.connection.head(
            headers=headers,
            params=params,
            **kwargs,
        )
        return response

    @final
    def get(
        self,
        *,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> requests.Response:
        """Sends an HTTP GET request to the API.

        Args:
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Keyword arguments to include in request.

        Returns:
            Response object.

        Raises:
            ConnectionNotStarted: when connection not started.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/GET

        """
        if self.connection is None:
            message = "connection not started before making GET request"
            raise errors.ConnectionNotStarted(message)

        response = self.connection.get(
            headers=headers,
            params=params,
            **kwargs,
        )
        return response

    @final
    def post(
        self,
        *,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> requests.Response:
        """Sends an HTTP POST request to the API.

        Args:
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Keyword arguments to include in request.

        Returns:
            Response object.

        Raises:
            ConnectionNotStarted: when connection not started.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST

        """
        if self.connection is None:
            message = "connection not started before making POST request"
            raise errors.ConnectionNotStarted(message)

        response = self.connection.post(
            headers=headers,
            params=params,
            **kwargs,
        )
        return response

    @final
    def put(
        self,
        *,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> requests.Response:
        """Sends an HTTP PUT request to the API.

        Args:
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Keyword arguments to include in request.

        Returns:
            Response object.

        Raises:
            ConnectionNotStarted: when connection not started.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PUT

        """
        if self.connection is None:
            message = "connection not started before making PUT request"
            raise errors.ConnectionNotStarted(message)

        response = self.connection.put(
            headers=headers,
            params=params,
            **kwargs,
        )
        return response

    @final
    def patch(
        self,
        *,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> requests.Response:
        """Sends an HTTP PATCH request to the API.

        Args:
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Keyword arguments to include in request.

        Returns:
            Response object.

        Raises:
            ConnectionNotStarted: when connection not started.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PATCH

        """
        if self.connection is None:
            message = "connection not started before making PATCH request"
            raise errors.ConnectionNotStarted(message)

        response = self.connection.patch(
            headers=headers,
            params=params,
            **kwargs,
        )
        return response

    @final
    def delete(
        self,
        *,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> requests.Response:
        """Sends an HTTP DELETE request to the API.

        Args:
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Keyword arguments to include in request.

        Returns:
            Response object.

        Raises:
            ConnectionNotStarted: when connection not started.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/DELETE

        """
        if self.connection is None:
            message = "connection not started before making DELETE request"
            raise errors.ConnectionNotStarted(message)

        response = self.connection.delete(
            headers=headers,
            params=params,
            **kwargs,
        )
        return response

    @final
    def options(
        self,
        *,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> requests.Response:
        """Sends an HTTP OPTIONS request to the API.

        Args:
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Keyword arguments to include in request.

        Returns:
            Response object.

        Raises:
            ConnectionNotStarted: when connection not started.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/OPTIONS

        """
        if self.connection is None:
            message = "connection not started before making OPTIONS request"
            raise errors.ConnectionNotStarted(message)

        response = self.connection.options(
            headers=headers,
            params=params,
            **kwargs,
        )
        return response

    @final
    def trace(
        self,
        *,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> requests.Response:
        """Sends an HTTP TRACE request to the API.

        Args:
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Keyword arguments to include in request.

        Returns:
            Response object.

        Raises:
            ConnectionNotStarted: when connection not started.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/TRACE

        """
        if self.connection is None:
            message = "connection not started before making TRACE request"
            raise errors.ConnectionNotStarted(message)

        response = self.connection.trace(
            headers=headers,
            params=params,
            **kwargs,
        )
        return response
