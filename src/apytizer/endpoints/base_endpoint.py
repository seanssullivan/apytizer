# -*- coding: utf-8 -*-
# src/apytizer/endpoints/base_endpoint.py
"""Base endpoint class.

This module defines the base endpoint class implementation.

"""

# Standard Library Imports
from __future__ import annotations
import logging
from typing import Any, Dict, Iterable, MutableMapping, Optional, Union
from urllib.parse import urljoin

# Third-Party Imports
import requests

# Local Imports
from .. import abstracts
from ..decorators import cache_response
from ..http_methods import HTTPMethod
from ..utils import merge

__all__ = ["BaseEndpoint", "DEFAULT_METHODS"]


# Initialize logger.
log = logging.getLogger(__name__)

# Define custom types.
AllowedMethods = Iterable[HTTPMethod]
Cache = MutableMapping
Headers = Dict[str, str]
Parameters = Dict[str, Any]

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


class BaseEndpoint(abstracts.AbstractEndpoint):
    """Base class from which all endpoint implementations are derived.

    Args:
        api: API instance.
        path: Relative path to endpoint.
        methods (optional): List of HTTP methods accepted by endpoint.
        headers (optional): Headers to set globally for endpoint.
        params (optional): Parameters to set globally for endpoint.
        cache (optional): Mutable mapping for caching responses.

    Attributes:
        api: Instance of an API subclass.

    Raises:
        TypeError: if path argument is not type 'str'.

    """

    def __init__(
        self,
        api: abstracts.AbstractAPI,
        path: Union[int, str],
        *,
        methods: Optional[AllowedMethods] = DEFAULT_METHODS,
        headers: Optional[Headers] = None,
        params: Optional[Parameters] = None,
        cache: Optional[Cache] = None,
    ):
        self.api = api
        self.path = str(path)
        self.methods = set(methods)
        self.headers = headers
        self.params = params
        self.cache = cache

    @property
    def path(self) -> str:
        """Relative URL path."""
        return self._path

    @path.setter
    def path(self, path: str) -> None:
        if not isinstance(path, str):
            message = f"expected type 'str', got {type(path)} instead"
            raise TypeError(message)

        self._path = path.strip("/")

    @property
    def uri(self) -> str:
        """Retrieve the endpoint URI."""
        return urljoin(self.api.url, self.path)

    def __eq__(self, other: object) -> bool:
        return (
            other.path == self.path
            if isinstance(other, BaseEndpoint)
            else False
        )

    def __hash__(self) -> int:
        return hash(self.path)

    @cache_response
    def head(
        self,
        headers: Optional[Headers] = None,
        params: Optional[Parameters] = None,
        **kwargs,
    ) -> requests.Response:
        """Sends an HTTP HEAD request to API endpoint.

        Args:
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Data or parameters to include in request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/HEAD

        """
        if HTTPMethod.HEAD not in self.methods:
            raise NotImplementedError

        response = self.api.head(
            self.path,
            headers=merge(self.headers, headers, overwrite=True),
            params=merge(self.params, params, overwrite=True),
            **kwargs,
        )
        return response

    @cache_response
    def get(
        self,
        headers: Optional[Headers] = None,
        params: Optional[Parameters] = None,
        **kwargs,
    ) -> requests.Response:
        """Sends an HTTP GET request to API endpoint.

        Args:
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Data or parameters to include in request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/GET

        """
        if HTTPMethod.GET not in self.methods:
            raise NotImplementedError

        response = self.api.get(
            self.path,
            headers=merge(self.headers, headers, overwrite=True),
            params=merge(self.params, params, overwrite=True),
            **kwargs,
        )
        return response

    @cache_response
    def post(
        self,
        headers: Optional[Headers] = None,
        params: Optional[Parameters] = None,
        **kwargs,
    ) -> requests.Response:
        """Sends an HTTP POST request to API endpoint.

        Args:
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Data or parameters to include in request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST

        """
        if HTTPMethod.POST not in self.methods:
            raise NotImplementedError

        response = self.api.post(
            self.path,
            headers=merge(self.headers, headers, overwrite=True),
            params=merge(self.params, params, overwrite=True),
            **kwargs,
        )
        return response

    @cache_response
    def put(
        self,
        headers: Optional[Headers] = None,
        params: Optional[Parameters] = None,
        **kwargs,
    ) -> requests.Response:
        """Sends an HTTP PUT request to API endpoint.

        Args:
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Data or parameters to include in request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PUT

        """
        if HTTPMethod.PUT not in self.methods:
            raise NotImplementedError

        response = self.api.put(
            self.path,
            headers=merge(self.headers, headers, overwrite=True),
            params=merge(self.params, params, overwrite=True),
            **kwargs,
        )
        return response

    @cache_response
    def patch(
        self,
        headers: Optional[Headers] = None,
        params: Optional[Parameters] = None,
        **kwargs,
    ) -> requests.Response:
        """Sends an HTTP PATCH request to API endpoint.

        Args:
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Data or parameters to include in request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PATCH

        """
        if HTTPMethod.PATCH not in self.methods:
            raise NotImplementedError

        response = self.api.patch(
            self.path,
            headers=merge(self.headers, headers, overwrite=True),
            params=merge(self.params, params, overwrite=True),
            **kwargs,
        )
        return response

    @cache_response
    def delete(
        self,
        headers: Optional[Headers] = None,
        params: Optional[Parameters] = None,
        **kwargs,
    ) -> requests.Response:
        """Sends an HTTP DELETE request to API endpoint.

        Args:
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Data or parameters to include in request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/DELETE

        """
        if HTTPMethod.DELETE not in self.methods:
            raise NotImplementedError

        response = self.api.delete(
            self.path,
            headers=merge(self.headers, headers, overwrite=True),
            params=merge(self.params, params, overwrite=True),
            **kwargs,
        )
        return response

    @cache_response
    def options(
        self,
        headers: Optional[Headers] = None,
        params: Optional[Parameters] = None,
        **kwargs,
    ) -> requests.Response:
        """Sends an HTTP OPTIONS request to API endpoint.

        Args:
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Data or parameters to include in request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/OPTIONS

        """
        if HTTPMethod.OPTIONS not in self.methods:
            raise NotImplementedError

        response = self.api.options(
            self.path,
            headers=merge(self.headers, headers, overwrite=True),
            params=merge(self.params, params, overwrite=True),
            **kwargs,
        )
        return response

    @cache_response
    def trace(
        self,
        headers: Optional[Headers] = None,
        params: Optional[Parameters] = None,
        **kwargs,
    ) -> requests.Response:
        """Sends an HTTP TRACE request to API endpoint.

        Args:
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Data or parameters to include in request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/TRACE

        """
        if HTTPMethod.TRACE not in self.methods:
            raise NotImplementedError

        response = self.api.trace(
            self.path,
            headers=merge(self.headers, headers, overwrite=True),
            params=merge(self.params, params, overwrite=True),
            **kwargs,
        )
        return response
