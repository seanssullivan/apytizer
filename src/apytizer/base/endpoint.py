# -*- coding: utf-8 -*-
"""Basic endpoint class.

This module defines a basic endpoint class implementation.

"""

# Standard Library Imports
from __future__ import annotations
import logging
from typing import Dict, List, MutableMapping, Union

# Third-Party Imports
import requests

# Local Imports
from ..abstracts.api import AbstractAPI
from ..abstracts.endpoint import AbstractEndpoint
from ..decorators.caching import cache_response
from ..utils import merge


# Initialize logger.
log = logging.getLogger(__name__)


class BasicEndpoint(AbstractEndpoint):
    """
    Class for interacting with an API endpoint.

    Args:
        path: Relative URL path for endpoint.
        headers (optional): Headers to set globally for endpoint.
        params (optional): Parameters to set globally for endpoint.
        methods (optional): List of HTTP methods accepted by endpoint.
        cache (optional): Mutable mapping for caching responses.

    Attributes:
        uri: Endpoint URL.

    """

    def __init__(
        self,
        api: AbstractAPI,
        path: str,
        *,
        headers: Dict = None,
        params: Dict = None,
        methods: List[str] = None,
        cache: MutableMapping = None,
    ):
        self.api = api
        self.path = path if path[0] != "/" else path[1:]
        self.headers = headers
        self.params = params
        self.methods = methods
        self.cache = cache

    def __call__(
        self,
        ref: Union[int, str],
        *,
        headers: Dict = None,
        params: Dict = None,
        methods: List[str] = None,
        cache: MutableMapping = None
    ) -> BasicEndpoint:
        """
        Returns a new endpoint with the appended reference.

        This method is a shortcut for accessing HTTP methods on a
        child endpoint or a nested resource.

        Args:
            ref: Reference for a collection or nested resource.
            headers (optional) : Headers to set globally for endpoint.
            params (optional) : Parameters to set globally for endpoint.
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
                params=params,
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
            ref: Reference for a collection or nested resource.

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

    def __add__(self, path: Union[int, str]) -> BasicEndpoint:
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

    def __truediv__(self, path: Union[int, str]) -> BasicEndpoint:
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

    @cache_response
    def head(
        self,
        headers: Dict = None,
        params: Dict = None,
        **kwargs
    ) -> requests.Response:
        """
        Sends an HTTP HEAD request to API endpoint.

        Args:
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Data or parameters to include in request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/HEAD

        """

        if self.methods and 'HEAD' not in self.methods:
            raise NotImplementedError

        response = self.api.head(
            self.path,
            headers=merge(self.headers, headers),
            params=merge(self.params, params),
            **kwargs
        )
        return response

    @cache_response
    def get(
        self,
        headers: Dict = None,
        params: Dict = None,
        **kwargs
    ) -> requests.Response:
        """
        Sends an HTTP GET request to API endpoint.

        Args:
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Data or parameters to include in request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/GET

        """

        if self.methods and 'GET' not in self.methods:
            raise NotImplementedError

        response = self.api.get(
            self.path,
            headers=merge(self.headers, headers),
            params=merge(self.params, params),
            **kwargs
        )
        return response

    @cache_response
    def post(
        self,
        headers: Dict = None,
        params: Dict = None,
        **kwargs
    ) -> requests.Response:
        """
        Sends an HTTP POST request to API endpoint.

        Args:
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Data or parameters to include in request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST

        """

        if self.methods and 'POST' not in self.methods:
            raise NotImplementedError

        response = self.api.post(
            self.path,
            headers=merge(self.headers, headers),
            params=merge(self.params, params),
            **kwargs
        )
        return response

    @cache_response
    def put(
        self,
        headers: Dict = None,
        params: Dict = None,
        **kwargs
    ) -> requests.Response:
        """
        Sends an HTTP PUT request to API endpoint.

        Args:
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Data or parameters to include in request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PUT

        """

        if self.methods and 'PUT' not in self.methods:
            raise NotImplementedError

        response = self.api.put(
            self.path,
            headers=merge(self.headers, headers),
            params=merge(self.params, params),
            **kwargs
        )
        return response

    @cache_response
    def patch(
        self,
        headers: Dict = None,
        params: Dict = None,
        **kwargs
    ) -> requests.Response:
        """
        Sends an HTTP PATCH request to API endpoint.

        Args:
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Data or parameters to include in request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PATCH

        """

        if self.methods and 'PATCH' not in self.methods:
            raise NotImplementedError

        response = self.api.patch(
            self.path,
            headers=merge(self.headers, headers),
            params=merge(self.params, params),
            **kwargs
        )
        return response

    @cache_response
    def delete(
        self,
        headers: Dict = None,
        params: Dict = None,
        **kwargs
    ) -> requests.Response:
        """
        Sends an HTTP DELETE request to API endpoint.

        Args:
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Data or parameters to include in request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/DELETE

        """

        if self.methods and 'DELETE' not in self.methods:
            raise NotImplementedError

        response = self.api.delete(
            self.path,
            headers=merge(self.headers, headers),
            params=merge(self.params, params),
            **kwargs
        )
        return response

    @cache_response
    def options(
        self,
        headers: Dict = None,
        params: Dict = None,
        **kwargs
    ) -> requests.Response:
        """
        Sends an HTTP OPTIONS request to API endpoint.

        Args:
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Data or parameters to include in request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/OPTIONS

        """
        if self.methods and 'OPTIONS' not in self.methods:
            raise NotImplementedError

        response = self.api.options(
            self.path,
            headers=merge(self.headers, headers),
            params=merge(self.params, params),
            **kwargs
        )
        return response

    @cache_response
    def trace(
        self,
        headers: Dict = None,
        params: Dict = None,
        **kwargs
    ) -> requests.Response:
        """
        Sends an HTTP TRACE request to API endpoint.

        Args:
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Data or parameters to include in request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/TRACE

        """

        if self.methods and 'TRACE' not in self.methods:
            raise NotImplementedError

        response = self.api.trace(
            self.path,
            headers=merge(self.headers, headers),
            params=merge(self.params, params),
            **kwargs
        )
        return response
