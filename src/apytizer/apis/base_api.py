# -*- coding: utf-8 -*-
# src/apytizer/apis/base_api.py
"""Base API class.

This module defines the base API class implementation.

"""

# Standard Library Imports
import logging
from typing import Any, Dict, MutableMapping, Optional, Tuple, Union
from urllib.parse import urljoin

# Third-Party Imports
import requests
from requests.auth import AuthBase

# Local Imports
from .. import abstracts
from ..decorators import cache_response
from ..decorators import confirm_connection
from ..http_methods import HTTPMethod
from ..utils import errors, merge

__all__ = ["BaseAPI"]


# Initialize logger.
log = logging.getLogger(__name__)

# Define custom types.
Authentication = Union[AuthBase, Tuple[str, str]]
Cache = MutableMapping
Headers = Dict[str, str]
Parameters = Dict[str, Any]


class BaseAPI(abstracts.AbstractAPI):
    """Base class from which all API implementations are derived.

    The BaseAPI class provides an interface for interacting with an API.
    It implements the standard HTTP methods (HEAD, GET, POST, PUT, PATCH,
    DELETE, OPTIONS and TRACE) as well as a `request` method for sending
    custom HTTP requests.

    Args:
        url: Base URL for API.
        auth (optional): Authorization or credentials.
        headers (optional): Headers to set globally for API.
        params (optional): Parameters to set globally for API.
        cache (optional): Mutable mapping for caching responses.

    """

    def __init__(
        self,
        url: str,
        auth: Optional[Authentication] = None,
        *,
        headers: Optional[Headers] = None,
        params: Optional[Parameters] = None,
        cache: Optional[Cache] = None,
    ):
        self.url = url
        self.auth = auth
        self.headers = headers or {}
        self.params = params or {}
        self.cache = cache

    @property
    def auth(self) -> Optional[Authentication]:
        """Authentication for API requests.

        Raises:
            TypeError: when set to a value other than an AuthBase or tuple.

        """
        return self._auth

    @auth.setter
    def auth(self, value: Optional[Authentication]) -> None:
        errors.raise_for_instance(value, (AuthBase, tuple, type(None)))
        self._auth = value

    @property
    def url(self) -> str:
        """URL of API."""
        return self._url

    @url.setter
    def url(self, url: str) -> None:
        errors.raise_for_instance(url, str)
        self._url = url + "/" if not url.endswith("/") else url

    @confirm_connection
    def request(
        self,
        method: HTTPMethod,
        route: str,
        headers: Optional[Headers] = None,
        params: Optional[Parameters] = None,
        **kwargs,
    ) -> requests.Response:
        """Sends an HTTP request.

        Args:
            method: HTTP request method to use.
            route: API path to which the request will be sent.
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Additional arguments to pass to request.

        Returns:
            Response object.

        .. _Requests Documentation:
            https://docs.python-requests.org/en/latest/api/

        """
        uri = urljoin(self.url, route)
        log.debug(
            "Sending HTTP %(method)s request to %(uri)s",
            {"method": method.name, "uri": uri},
        )

        response = requests.request(
            method.name,
            uri,
            auth=self.auth,
            headers=merge(self.headers, headers, overwrite=True),
            params=merge(self.params, params, overwrite=True),
            **kwargs,
        )

        log.debug(
            "Received response with status code %(status)s",
            {"status": response.status_code},
        )
        return response

    @cache_response
    def head(
        self,
        route: str,
        headers: Optional[Headers] = None,
        params: Optional[Parameters] = None,
        **kwargs,
    ) -> requests.Response:
        """Sends an HTTP HEAD request.

        Args:
            route: API path to which the request will be sent.
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Additional arguments to pass to request.

        Returns:
            Response object.

        .. _HTTP HEAD Method:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/HEAD

        """
        response = self.request(
            HTTPMethod.HEAD,
            route,
            headers=headers,
            params=params,
            **kwargs,
        )
        return response

    @cache_response
    def get(
        self,
        route: str,
        headers: Optional[Headers] = None,
        params: Optional[Parameters] = None,
        **kwargs,
    ) -> requests.Response:
        """Sends an HTTP GET request.

        Args:
            route: API path to which the request will be sent.
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Additional arguments to pass to request.

        Returns:
            Response object.

        .. _HTTP GET Method:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/GET

        """
        response = self.request(
            HTTPMethod.GET,
            route,
            headers=headers,
            params=params,
            **kwargs,
        )
        return response

    @cache_response
    def post(
        self,
        route: str,
        headers: Optional[Headers] = None,
        params: Optional[Parameters] = None,
        **kwargs,
    ) -> requests.Response:
        """Sends an HTTP POST request.

        Args:
            route: API path to which the request will be sent.
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Additional arguments to pass to request.

        Returns:
            Response object.

        .. _HTTP POST Method:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST

        """
        response = self.request(
            HTTPMethod.POST,
            route,
            headers=headers,
            params=params,
            **kwargs,
        )
        return response

    @cache_response
    def put(
        self,
        route: str,
        headers: Optional[Headers] = None,
        params: Optional[Parameters] = None,
        **kwargs,
    ) -> requests.Response:
        """Sends an HTTP PUT request.

        Args:
            route: API path to which the request will be sent.
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Additional arguments to pass to request.

        Returns:
            Response object.

        .. _HTTP PUT Method:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PUT

        """
        response = self.request(
            HTTPMethod.PUT,
            route,
            headers=headers,
            params=params,
            **kwargs,
        )
        return response

    @cache_response
    def patch(
        self,
        route: str,
        headers: Optional[Headers] = None,
        params: Optional[Parameters] = None,
        **kwargs,
    ) -> requests.Response:
        """Sends an HTTP PATCH request.

        Args:
            route: API path to which the request will be sent.
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Additional arguments to pass to request.

        Returns:
            Response object.

        .. _HTTP PATCH Method:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PATCH

        """
        response = self.request(
            HTTPMethod.PATCH,
            route,
            headers=headers,
            params=params,
            **kwargs,
        )
        return response

    @cache_response
    def delete(
        self,
        route: str,
        headers: Optional[Headers] = None,
        params: Optional[Parameters] = None,
        **kwargs,
    ) -> requests.Response:
        """Sends an HTTP DELETE request.

        Args:
            route: API path to which the request will be sent.
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Additional arguments to pass to request.

        Returns:
            Response object.

        .. _HTTP DELETE Method:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/DELETE

        """
        response = self.request(
            HTTPMethod.DELETE,
            route,
            headers=headers,
            params=params,
            **kwargs,
        )
        return response

    @cache_response
    def options(
        self,
        route: str,
        headers: Optional[Headers] = None,
        params: Optional[Parameters] = None,
        **kwargs,
    ) -> requests.Response:
        """Sends an HTTP OPTIONS request.

        Args:
            route: API path to which the request will be sent.
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Additional arguments to pass to request.

        Returns:
            Response object.

        .. _HTTP OPTIONS Method:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/OPTIONS

        """
        response = self.request(
            HTTPMethod.OPTIONS,
            route,
            headers=headers,
            params=params,
            **kwargs,
        )
        return response

    @cache_response
    def trace(
        self,
        route: str,
        headers: Optional[Headers] = None,
        params: Optional[Parameters] = None,
        **kwargs,
    ) -> requests.Response:
        """Sends an HTTP TRACE request.

        Args:
            route: API path to which the request will be sent.
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Additional arguments to pass to request.

        Returns:
            Response object.

        .. _HTTP TRACE Method:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/TRACE

        """
        response = self.request(
            HTTPMethod.TRACE,
            route,
            headers=headers,
            params=params,
            **kwargs,
        )
        return response
