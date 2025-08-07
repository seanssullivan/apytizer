# -*- coding: utf-8 -*-
# src/apytizer/endpoints/base_endpoint.py
"""WEb Endpoint Class.

This module defines the web endpoint class implementation.

"""

# Standard Library Imports
from __future__ import annotations
import logging
from typing import Any
from typing import Collection
from typing import Dict
from typing import MutableMapping
from typing import Optional
from typing import Set
from typing import Union
from typing import TYPE_CHECKING
from urllib.parse import urljoin

# Third-Party Imports
from requests import Response

# Local Imports
from .abstract_endpoint import AbstractEndpoint
from ..connections import HttpConnection
from ..decorators import cache_response
from ..http_methods import HTTPMethod
from ..routes import Route
from .. import errors
from .. import utils

if TYPE_CHECKING:
    from ..apis import WebAPI

__all__ = ["WebEndpoint"]


log = logging.getLogger("apytizer")

# Define constants.
DEFAULT_METHODS = (
    HTTPMethod.HEAD,
    HTTPMethod.GET,
    HTTPMethod.POST,
    HTTPMethod.PUT,
    HTTPMethod.PATCH,
    HTTPMethod.DELETE,
    HTTPMethod.OPTIONS,
    HTTPMethod.TRACE,
)


class WebEndpoint(AbstractEndpoint):
    """Implements an endpoint for web APIs.

    Args:
        __api: API instance.
        path: Relative path to endpoint.
        methods (optional): List of HTTP methods accepted by endpoint.
        headers (optional): Headers to set globally for endpoint.
        params (optional): Parameters to set globally for endpoint.
        cache (optional): Mutable mapping for caching responses.

    Attributes:
        connection: Connection with which to make requests.

    """

    __slots__ = (
        "_api",
        "_path",
        "_methods",
        "_headers",
        "_params",
        "_cache",
    )

    def __init__(
        self,
        __api: "WebAPI",
        /,
        path: Union[int, Route, str],
        *,
        methods: Collection[HTTPMethod] = DEFAULT_METHODS,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        cache: Optional[MutableMapping[str, Any]] = None,
    ) -> None:
        self._api = __api
        self._path = str(path).strip("/")
        self._methods = set(methods)
        self._headers = headers
        self._params = params
        self._cache = cache

    @property
    def api(self) -> "WebAPI":
        """API."""
        return self._api

    @property
    def connection(self) -> Optional[HttpConnection]:
        """Connection with which to make requests."""
        return self._api.connection

    @property
    def path(self) -> str:
        """Endpoint path."""
        return self._path

    @property
    def url(self) -> str:
        """Endpoint URL."""
        result = urljoin(self.api.url, self.path)
        return result

    @property
    def methods(self) -> Set[HTTPMethod]:
        """Endpoint methods."""
        return self._methods

    @property
    def headers(self) -> Optional[Dict[str, str]]:
        """Headers."""
        return self._headers

    @property
    def params(self) -> Optional[Dict[str, Any]]:
        """Parameters."""
        return self._params

    @property
    def cache(self) -> Optional[MutableMapping[str, Any]]:
        """Cache."""
        return self._cache

    def __eq__(self, other: object) -> bool:
        result = (
            other.path.lower() == self.path.lower()
            if isinstance(other, WebEndpoint)
            else False
        )
        return result

    def __hash__(self) -> int:
        return hash(self.path)

    def __repr__(self) -> str:
        result = f"<{self.__class__.__name__!s} (path={self.path!s})>"
        return result

    def __str__(self) -> str:
        return self.path

    def __getitem__(self, path: str) -> AbstractEndpoint:
        """Get endpoint.

        Args:
            path: Relative path of endpoint.

        Returns:
            Endpoint.

        """
        route = "/".join([self._path, path])
        result = self._api[route]
        return result

    def __truediv__(self, path: str) -> AbstractEndpoint:
        """Get endpoint.

        Args:
            path: Relative path of endpoint.

        Returns:
            Endpoint.

        """
        route = "/".join([self._path, path])
        result = self._api[route]
        return result

    @cache_response
    def head(
        self,
        *,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Optional[Response]:
        """Sends an HTTP HEAD request to the endpoint.

        Args:
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Keyword arguments to include in request.

        Returns:
            Response object.

        Raises:
            ConnectionNotStarted: when connection not started.
            MethodNotAllowed: when HTTP method not allowed on endpoint.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/HEAD

        """
        if self.connection is None:
            message = "connection not started before making HEAD request"
            raise errors.ConnectionNotStarted(message)

        if HTTPMethod.HEAD not in self.methods:
            message = f"HEAD method not allowed at {self.path!s} endpoint"
            raise errors.MethodNotAllowed(message)

        response = self.connection.head(
            self.path,
            headers=utils.merge(self.headers, headers),
            params=utils.merge(self.params, params),
            **kwargs,
        )
        return response

    @cache_response
    def get(
        self,
        *,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Optional[Response]:
        """Sends an HTTP GET request to the endpoint.

        Args:
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Keyword arguments to include in request.

        Returns:
            Response object.

        Raises:
            ConnectionNotStarted: when connection not started.
            MethodNotAllowed: when HTTP method not allowed on endpoint.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/GET

        """
        if self.connection is None:
            message = "connection not started before making GET request"
            raise errors.ConnectionNotStarted(message)

        if HTTPMethod.GET not in self.methods:
            message = f"GET method not allowed at {self.path!s} endpoint"
            raise errors.MethodNotAllowed(message)

        response = self.connection.get(
            self.path,
            headers=utils.merge(self.headers, headers),
            params=utils.merge(self.params, params),
            **kwargs,
        )
        return response

    @cache_response
    def post(
        self,
        *,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Optional[Response]:
        """Sends an HTTP POST request to the endpoint.

        Args:
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Keyword arguments to include in request.

        Returns:
            Response object.

        Raises:
            ConnectionNotStarted: when connection not started.
            MethodNotAllowed: when HTTP method not allowed on endpoint.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST

        """
        if self.connection is None:
            message = "connection not started before making POST request"
            raise errors.ConnectionNotStarted(message)

        if HTTPMethod.POST not in self.methods:
            message = f"POST method not allowed at {self.path!s} endpoint"
            raise errors.MethodNotAllowed(message)

        response = self.connection.post(
            self.path,
            headers=utils.merge(self.headers, headers),
            params=utils.merge(self.params, params),
            **kwargs,
        )
        return response

    @cache_response
    def put(
        self,
        *,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Optional[Response]:
        """Sends an HTTP PUT request to the endpoint.

        Args:
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Keyword arguments to include in request.

        Returns:
            Response object.

        Raises:
            ConnectionNotStarted: when connection not started.
            MethodNotAllowed: when HTTP method not allowed on endpoint.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PUT

        """
        if self.connection is None:
            message = "connection not started before making PUT request"
            raise errors.ConnectionNotStarted(message)

        if HTTPMethod.PUT not in self.methods:
            message = f"PUT method not allowed at {self.path!s} endpoint"
            raise errors.MethodNotAllowed(message)

        response = self.connection.put(
            self.path,
            headers=utils.merge(self.headers, headers),
            params=utils.merge(self.params, params),
            **kwargs,
        )
        return response

    @cache_response
    def patch(
        self,
        *,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Optional[Response]:
        """Sends an HTTP PATCH request to the endpoint.

        Args:
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Keyword arguments to include in request.

        Returns:
            Response object.

        Raises:
            ConnectionNotStarted: when connection not started.
            MethodNotAllowed: when HTTP method not allowed on endpoint.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PATCH

        """
        if self.connection is None:
            message = "connection not started before making PATCH request"
            raise errors.ConnectionNotStarted(message)

        if HTTPMethod.PATCH not in self.methods:
            message = f"PATCH method not allowed at {self.path!s} endpoint"
            raise errors.MethodNotAllowed(message)

        response = self.connection.patch(
            self.path,
            headers=utils.merge(self.headers, headers),
            params=utils.merge(self.params, params),
            **kwargs,
        )
        return response

    @cache_response
    def delete(
        self,
        *,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Optional[Response]:
        """Sends an HTTP DELETE request to the endpoint.

        Args:
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Keyword arguments to include in request.

        Returns:
            Response object.

        Raises:
            ConnectionNotStarted: when connection not started.
            MethodNotAllowed: when HTTP method not allowed on endpoint.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/DELETE

        """
        if self.connection is None:
            message = "connection not started before making DELETE request"
            raise errors.ConnectionNotStarted(message)

        if HTTPMethod.DELETE not in self.methods:
            message = f"DELETE method not allowed at {self.path!s} endpoint"
            raise errors.MethodNotAllowed(message)

        response = self.connection.delete(
            self.path,
            headers=utils.merge(self.headers, headers),
            params=utils.merge(self.params, params),
            **kwargs,
        )
        return response

    @cache_response
    def options(
        self,
        *,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Optional[Response]:
        """Sends an HTTP OPTIONS request to the endpoint.

        Args:
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Keyword arguments to include in request.

        Returns:
            Response object.

        Raises:
            ConnectionNotStarted: when connection not started.
            MethodNotAllowed: when HTTP method not allowed on endpoint.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/OPTIONS

        """
        if self.connection is None:
            message = "connection not started before making OPTIONS request"
            raise errors.ConnectionNotStarted(message)

        if HTTPMethod.OPTIONS not in self.methods:
            message = f"OPTIONS method not allowed at {self.path!s} endpoint"
            raise errors.MethodNotAllowed(message)

        response = self.connection.options(
            self.path,
            headers=utils.merge(self.headers, headers),
            params=utils.merge(self.params, params),
            **kwargs,
        )
        return response

    @cache_response
    def trace(
        self,
        *,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Optional[Response]:
        """Sends an HTTP TRACE request to the endpoint.

        Args:
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Keyword arguments to include in request.

        Returns:
            Response object.

        Raises:
            ConnectionNotStarted: when connection not started.
            MethodNotAllowed: when HTTP method not allowed on endpoint.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/TRACE

        """
        if self.connection is None:
            message = "connection not started before making TRACE request"
            raise errors.ConnectionNotStarted(message)

        if HTTPMethod.TRACE not in self.methods:
            message = f"TRACE method not allowed at {self.path!s} endpoint"
            raise errors.MethodNotAllowed(message)

        response = self.connection.trace(
            self.path,
            headers=utils.merge(self.headers, headers),
            params=utils.merge(self.params, params),
            **kwargs,
        )
        return response
