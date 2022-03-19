# -*- coding: utf-8 -*-
# src/apytizer/base/api.py
"""Base API class.

This module defines a base API class implementation.

"""

# Standard Library Imports
import logging
from typing import Any, Dict, List, MutableMapping, Tuple, Union, final
from urllib.parse import urljoin

# Third-Party Imports
import requests
from requests.adapters import HTTPAdapter
from requests.auth import AuthBase

# Local Imports
from .. import abstracts
from ..decorators.caching import cache_response
from ..decorators.connection import confirm_connection
from ..utils import merge


# Initialize logger.
log = logging.getLogger(__name__)

# Define custom types.
Authentication = Union[AuthBase, Tuple]
Cache = MutableMapping
Headers = Dict[str, str]
Parameters = Dict[str, Any]

# Define constants.
PROTOCOLS = ["https", "http"]


class BaseAPI(abstracts.AbstractAPI):
    """Implements the base API.

    The BaseAPI class provides an interface for interacting with a REST API.
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
        auth: Authentication = None,
        *,
        headers: Headers = None,
        params: Parameters = None,
        cache: Cache = None,
    ):
        self.url = url + "/" if url[-1] != "/" else url
        self.auth = auth
        self.headers = headers
        self.params = params
        self.cache = cache

    @property
    def auth(self) -> Union[AuthBase, Tuple]:
        """Authentication for API requests.

        Raises:
            TypeError: when set to a value other than an AuthBase or tuple.

        """
        return self._auth

    @auth.setter
    def auth(self, value: Union[AuthBase, Tuple[str, str], None]) -> None:
        if value and not isinstance(value, (AuthBase, tuple)):
            message = f"expected either AuthBase or tuple, not {type(value)}"
            raise TypeError(message)

        self._auth = value

    @confirm_connection
    def request(
        self,
        method: str,
        route: str,
        headers: Headers = None,
        params: Parameters = None,
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
            {"method": method, "uri": uri},
        )

        response = requests.request(
            method,
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
        headers: Headers = None,
        params: Parameters = None,
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
            "HEAD", route, headers=headers, params=params, **kwargs
        )
        return response

    @cache_response
    def get(
        self,
        route: str,
        headers: Headers = None,
        params: Parameters = None,
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
            "GET", route, headers=headers, params=params, **kwargs
        )
        return response

    @cache_response
    def post(
        self,
        route: str,
        headers: Headers = None,
        params: Parameters = None,
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
            "POST", route, headers=headers, params=params, **kwargs
        )
        return response

    @cache_response
    def put(
        self,
        route: str,
        headers: Headers = None,
        params: Parameters = None,
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
            "PUT", route, headers=headers, params=params, **kwargs
        )
        return response

    @cache_response
    def patch(
        self,
        route: str,
        headers: Headers = None,
        params: Parameters = None,
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
            "PATCH", route, headers=headers, params=params, **kwargs
        )
        return response

    @cache_response
    def delete(
        self,
        route: str,
        headers: Headers = None,
        params: Parameters = None,
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
            "DELETE", route, headers=headers, params=params, **kwargs
        )
        return response

    @cache_response
    def options(
        self,
        route: str,
        headers: Headers = None,
        params: Parameters = None,
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
            "OPTIONS", route, headers=headers, params=params, **kwargs
        )
        return response

    @cache_response
    def trace(
        self,
        route: str,
        headers: Headers = None,
        params: Parameters = None,
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
            "TRACE", route, headers=headers, params=params, **kwargs
        )
        return response


class SessionAPI(abstracts.AbstractSession, BaseAPI):
    """Implements a session-based API.

    The SessionAPI class implements the same interface as the BasicAPI; however, it
    overrides the `request` method to use requests.Session. In addition, the class
    provides `start` and `stop` methods to allow manual control of the session.

    An instance of SessionAPI can also be used as a context manager.

    Args:
        url: Base URL for API.
        auth (optional): Authentication or credentials.
        headers (optional): Headers to set globally for API.
        params (optional): Parameters to set globally for API.
        adapter (optional): Instance of an HTTPAdapter.
        cache (optional): Mutable mapping for caching responses.

    .. Requests Documentation:
        https://docs.python-requests.org/en/latest/api/#request-sessions

    """

    def __init__(
        self,
        url: str,
        auth: Authentication = None,
        *,
        headers: Headers = None,
        params: Parameters = None,
        adapter: HTTPAdapter = None,
        cache: MutableMapping = None,
    ):
        super().__init__(
            url,
            auth,
            headers=headers,
            params=params,
            cache=cache,
        )
        self.adapter = adapter
        self.session = None  # type: requests.Session

    @final
    def __enter__(self):
        self.start()
        return self

    @final
    def __exit__(self, *args):
        self.close()

    @property
    def adapter(self) -> HTTPAdapter:
        """Adapter for API requests.

        Raises:
            TypeError: if set to value of type other than HTTPAdapter.

        """
        return self._adapter

    @adapter.setter
    def adapter(self, value: HTTPAdapter) -> None:
        if value and not isinstance(value, HTTPAdapter):
            message = f"expected HTTPAdapter, not {type(value)}"
            raise TypeError(message)

        self._adapter = value

    def start(self) -> None:
        """Starts the session."""
        log.debug("Starting API session...")

        factory = _RequestsSessionFactory()
        self.session = factory.make_session(
            self.adapter,
            self.auth,
            self.headers,
        )

    def close(self, *args) -> None:
        """Destroys the session."""
        log.debug("Closing API session...")
        self.session.close()
        self.session = None

    @confirm_connection
    def request(
        self,
        method: str,
        route: str,
        headers: Headers = None,
        params: Parameters = None,
        **kwargs,
    ) -> requests.Response:
        """Sends an HTTP request.

        Args:
            method: HTTP request method to use (HEAD, GET, POST, PUT, DELETE,
                OPTIONS, or TRACE).
            route: API path to which the request will be sent.
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Additional arguments to pass to request.

        Returns:
            Response object.

        .. Requests Documentation:
            https://docs.python-requests.org/en/latest/api/

        """
        uri = urljoin(self.url, route)
        if self.session:
            log.debug(
                "Sending HTTP %(method)s request to %(uri)s",
                {"method": method, "uri": uri},
            )

            response = self.session.request(
                method,
                uri,
                headers=merge(self.headers, headers),
                params=merge(self.params, params),
                **kwargs,
            )

            log.debug(
                "Received response with status code %(status)s",
                {"status": response.status_code},
            )

        else:
            log.warning(
                "%(event)s: %(reason)s",
                {
                    "event": "Session not started",
                    "reason": "start() was not called before sending request",
                },
            )
            response = super().request(
                method,
                uri,
                headers=headers,
                params=params,
                **kwargs,
            )

        return response


class _RequestsSessionBuilder:
    """Implements a builder for requests sessions."""

    _session: requests.Session

    def __init__(self) -> None:
        self.reset()

    @property
    def session(self) -> requests.Session:
        """Constructed session."""
        result = self._session
        self.reset()
        return result

    def reset(self) -> None:
        """Reset build cycle."""
        self._session = requests.Session()

    def include_adapter(
        self,
        adapter: HTTPAdapter,
        *,
        protocols: List[str] = PROTOCOLS,
    ) -> None:
        """Add adapter to session.

        Args:
            adapter: Adapter to mount to session.
            protocols (optional): Protocols on which to mount adapter.

        """
        for protocol in protocols:
            prefix = f"{protocol!s}://"
            self._session.mount(prefix, adapter)

    def include_auth(self, auth: Authentication) -> None:
        """Add authentication to session."""
        self._session.auth = auth

    def include_default_headers(self, headers: Headers) -> None:
        """Add default headers to session."""
        self._session.headers.update(headers)


class _RequestsSessionFactory:
    """Implements a factory for requests sessions."""

    def __init__(self) -> None:
        self.builder = _RequestsSessionBuilder()

    def make_session(
        self,
        adapter: HTTPAdapter = None,
        auth: Authentication = None,
        headers: Headers = None,
    ) -> requests.Session:
        """Make requests session.

        Args:
            adapter (optional): Instance of an HTTPAdapter.
            auth (optional): Authentication or credentials.
            headers (optional): Headers to set for all requests.

        Returns:
            Requests Session.

        """
        if adapter is not None:
            self.builder.include_adapter(adapter)

        if auth is not None:
            self.builder.include_auth(auth)

        if headers is not None:
            self.builder.include_default_headers(headers)

        result = self.builder.session
        return result
