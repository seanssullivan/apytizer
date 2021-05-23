# -*- coding: utf-8 -*-
"""Basic endpoint class.

This module defines a basic endpoint class implementation.

"""

# Standard Library Imports
from __future__ import annotations
import logging
import operator
from typing import Dict, List, MutableMapping, Union
from urllib.parse import urljoin

# Third-Party Imports
from cachetools import cachedmethod
import requests

# Local Imports
from src.abstracts.api import AbstractAPI
from src.abstracts.endpoint import AbstractEndpoint
from .utils import generate_key
from .utils import merge_headers


log = logging.getLogger(__name__)


class BasicEndpoint(AbstractEndpoint):
    """
    Class for interacting with an API endpoint.

    Args:
        path: Relative URL path for endpoint.
        headers (optional): Headers to set globally for API.
        methods (optional): List of HTTP methods accepted by endpoint.
        cache (optional): Mutable mapping for caching responses.

    """

    def __init__(
        self,
        api: AbstractAPI,
        path: str,
        *,
        headers: Dict = None,
        methods: List[str] = None,
        cache: MutableMapping = None,
    ):
        self.api = api
        self.path = path if path[0] != "/" else path[1:]
        self.headers = headers
        self.methods = methods
        self.cache = cache

    @property
    def uri(self) -> str:
        return urljoin(self.api.url, self.path)

    @property
    def url(self) -> str:
        return self.uri

    def __hash__(self) -> int:
        return hash(self.uri)

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__!s} methods={self.methods!s} uri={self.uri!s}>'

    def __str__(self) -> str:
        return f'{self.uri!s}'

    def __call__(
        self,
        ref: Union[int, str],
        *,
        headers: Dict = None,
        methods: List[str] = None,
        cache: MutableMapping = None
    ) -> BasicEndpoint:
        """
        Returns a new endpoint with the appended reference.

        This method is a shortcut for accessing HTTP methods on a
        child endpoint or a nested resource.

        Args:
            ref: Reference for a nested resource or an object
                available through a resource collection endpoint.
            headers (optional) : Headers to set globally for endpoint.
            methods (optional): List of HTTP methods accepted by endpoint.
            cache (optional): Mutable mapping for caching responses.

        Returns:
            BasicEndpoint instance.

        """
        if isinstance(ref, (int, str)):
            endpoint = BasicEndpoint(
                self.api,
                f'{self.path!s}/{ref!s}',
                headers=headers,
                methods=methods,
                cache=cache,
            )
        else:
            raise TypeError

        return endpoint

    def __getitem__(self, ref: Union[int, str]) -> BasicEndpoint:
        """
        Returns a new endpoint with the appended reference.

        This method is a shortcut for accessing HTTP methods on a
        child endpoint or a nested resource.

        Args:
            ref: Reference for a nested resource or an object
                available through a resource collection endpoint.

        Returns:
            BasicEndpoint instance.

        """
        if isinstance(ref, (int, str)):
            endpoint = BasicEndpoint(
                self.api,
                f'{self.path!s}/{ref!s}'
            )
        else:
            raise TypeError

        return endpoint

    def __add__(self, path: int or str) -> BasicEndpoint:
        """
        Returns a new endpoint after combining both paths.

        This is a method for quickly accessing HTTP methods for
        child endpoints or nested resources. It behaves the same
        as the __truediv__ method.

        Args:
            path: Value to append to the current path.

        Returns:
            BasicEndpoint instance.

        """
        if isinstance(path, (int, str)):
            endpoint = BasicEndpoint(
                self.api,
                f'{self.path!s}/{path!s}'
            )
        else:
            raise TypeError

        return endpoint

    def __truediv__(self, path: str) -> BasicEndpoint:
        """
        Returns a new endpoint after combining both paths.

        This is a method for quickly accessing HTTP methods for
        child endpoints or nested resources. It behaves the same
        as the __add__ method.

        Args:
            path: Value to append to the current path.

        Returns:
            BasicEndpoint instance.

        """
        if isinstance(path, (int, str)):
            endpoint = BasicEndpoint(
                self.api,
                f'{self.path!s}/{path!s}'
            )
        else:
            raise TypeError

        return endpoint

    @cachedmethod(operator.attrgetter('cache'), key=generate_key('HEAD'))
    def head(self, headers: Dict = None, **kwargs) -> requests.Response:
        """
        Sends an HTTP HEAD request to API endpoint.

        Args:
            headers (optional): Request headers (overrides global headers).
            **kwargs: Data or parameters to include in request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/HEAD

        """

        if self.methods and 'HEAD' not in self.methods:
            raise NotImplementedError

        headers = merge_headers(self.headers, headers)
        response = self.api.head(self.path, headers=headers, **kwargs)
        return response

    @cachedmethod(operator.attrgetter('cache'), key=generate_key('GET'))
    def get(self, headers: Dict = None, **kwargs) -> requests.Response:
        """
        Sends an HTTP GET request to API endpoint.

        Args:
            headers (optional): Request headers (overrides global headers).
            **kwargs: Data or parameters to include in request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/GET

        """

        if self.methods and 'GET' not in self.methods:
            raise NotImplementedError

        headers = merge_headers(self.headers, headers)
        response = self.api.get(self.path, headers=headers, **kwargs)
        return response

    @cachedmethod(operator.attrgetter('cache'), key=generate_key('POST'))
    def post(self, data: Dict, headers: Dict = None, **kwargs) -> requests.Response:
        """
        Sends an HTTP POST request to API endpoint.

        Args:
            headers (optional): Request headers (overrides global headers).
            **kwargs: Data or parameters to include in request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST

        """

        if self.methods and 'POST' not in self.methods:
            raise NotImplementedError

        headers = merge_headers(self.headers, headers)
        response = self.api.post(self.path, headers=headers, data=data, **kwargs)
        return response

    @cachedmethod(operator.attrgetter('cache'), key=generate_key('PUT'))
    def put(self, data: Dict, headers: Dict = None, **kwargs) -> requests.Response:
        """
        Sends an HTTP PUT request to API endpoint.

        Args:
            headers (optional): Request headers (overrides global headers).
            **kwargs: Data or parameters to include in request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PUT

        """

        if self.methods and 'PUT' not in self.methods:
            raise NotImplementedError

        headers = merge_headers(self.headers, headers)
        response = self.api.put(self.path, headers=headers, data=data, **kwargs)
        return response

    @cachedmethod(operator.attrgetter('cache'), key=generate_key('PATCH'))
    def patch(self, data: Dict, headers: Dict = None, **kwargs) -> requests.Response:
        """
        Sends an HTTP PATCH request to API endpoint.

        Args:
            headers (optional): Request headers (overrides global headers).
            **kwargs: Data or parameters to include in request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PATCH

        """

        if self.methods and 'PATCH' not in self.methods:
            raise NotImplementedError

        headers = merge_headers(self.headers, headers)
        response = self.api.patch(self.path, headers=headers, data=data, **kwargs)
        return response

    @cachedmethod(operator.attrgetter('cache'), key=generate_key('DELETE'))
    def delete(self, headers: Dict = None, **kwargs) -> requests.Response:
        """
        Sends an HTTP DELETE request to API endpoint.

        Args:
            headers (optional): Request headers (overrides global headers).
            **kwargs: Data or parameters to include in request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/DELETE

        """

        if self.methods and 'DELETE' not in self.methods:
            raise NotImplementedError

        headers = merge_headers(self.headers, headers)
        response = self.api.delete(self.path, headers=headers, **kwargs)
        return response

    @cachedmethod(operator.attrgetter('cache'), key=generate_key('OPTIONS'))
    def options(self, headers: Dict = None, **kwargs) -> requests.Response:
        """
        Sends an HTTP OPTIONS request to API endpoint.

        Args:
            headers (optional): Request headers (overrides global headers).
            **kwargs: Data or parameters to include in request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/OPTIONS

        """
        if self.methods and 'OPTIONS' not in self.methods:
            raise NotImplementedError

        headers = merge_headers(self.headers, headers)
        response = self.api.options(self.path, headers=headers, **kwargs)
        return response

    @cachedmethod(operator.attrgetter('cache'), key=generate_key('TRACE'))
    def trace(self, headers: Dict = None, **kwargs) -> requests.Response:
        """
        Sends an HTTP TRACE request to API endpoint.

        Args:
            headers (optional): Request headers (overrides global headers).
            **kwargs: Data or parameters to include in request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/TRACE

        """

        if self.methods and 'TRACE' not in self.methods:
            raise NotImplementedError

        headers = merge_headers(self.headers, headers)
        response = self.api.trace(self.path, headers=headers, **kwargs)
        return response
