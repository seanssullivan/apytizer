# -*- coding: utf-8 -*-
"""Basic API class.

This module defines a basic API class implementation.

"""

# Standard Library Imports
import logging
from typing import Dict, MutableMapping, Tuple, Union, final
from urllib.parse import urljoin

# Third-Party Imports
import requests
from requests.adapters import HTTPAdapter
from requests.auth import AuthBase

# Local Imports
from .. import abstracts
from ..decorators.caching import cache_response
from ..utils import merge


# Initialize logger.
log = logging.getLogger(__name__)


class BasicAPI(abstracts.AbstractAPI):
    """
    Implements a basic API.

    The BasicAPI class provides an interface for interacting with a REST API.
    It implements the standard HTTP methods (HEAD, GET, POST, PUT, PATCH, DELETE, OPTIONS and TRACE)
    as well as a `request` method for sending a custom HTTP request.

    Args:
        url: Base URL for API.
        auth: Authorization or credentials.
        headers (optional): Headers to set globally for API.
        params (optional): Parameters to set globally for API.
        cache (optional): Mutable mapping for caching responses.

    Attributes:
        url: API URL.

    """

    def __init__(
        self,
        url: str,
        auth: Union[AuthBase, Tuple] = None,
        *,
        headers: Dict = None,
        params: Dict = None,
        cache: MutableMapping = None
    ):
        self.url = url + "/" if url[-1] != "/" else url
        self.auth = auth
        self.headers = headers
        self.params = params
        self.cache = cache

    def request(
        self,
        method: str,
        route: str,
        headers: Dict = None,
        params: Dict = None,
        **kwargs
    ) -> requests.Response:
        """
        Sends an HTTP request.

        Args:
            method: HTTP request method to use (HEAD, GET, POST, PUT, DELETE, OPTIONS, or TRACE).
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
            {'method': method, 'uri': uri}
        )

        response = requests.request(
            method,
            uri,
            auth=self.auth,
            headers=merge(self.headers, headers),
            params=merge(self.params, params),
            **kwargs
        )
        return response

    @cache_response
    def head(
        self,
        route: str,
        headers: Dict = None,
        params: Dict = None,
        **kwargs
    ) -> requests.Response:
        """
        Sends an HTTP HEAD request.

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
            'HEAD',
            route,
            headers=headers,
            params=params,
            **kwargs
        )
        return response

    @cache_response
    def get(
        self,
        route: str,
        headers: Dict = None,
        params: Dict = None,
        **kwargs
    ) -> requests.Response:
        """
        Sends an HTTP GET request.

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
            'GET',
            route,
            headers=headers,
            params=params,
            **kwargs
        )
        return response

    @cache_response
    def post(
        self,
        route: str,
        headers: Dict = None,
        params: Dict = None,
        **kwargs
    ) -> requests.Response:
        """
        Sends an HTTP POST request.

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
            'POST',
            route,
            headers=headers,
            params=params,
            **kwargs
        )
        return response

    @cache_response
    def put(
        self,
        route: str,
        headers: Dict = None,
        params: Dict = None,
        **kwargs
    ) -> requests.Response:
        """
        Sends an HTTP PUT request.

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
            'PUT',
            route,
            headers=headers,
            params=params,
            **kwargs
        )
        return response

    @cache_response
    def patch(
        self,
        route: str,
        headers: Dict = None,
        params: Dict = None,
        **kwargs
    ) -> requests.Response:
        """
        Sends an HTTP PATCH request.

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
            'PATCH',
            route,
            headers=headers,
            params=params,
            **kwargs
        )
        return response

    @cache_response
    def delete(
        self,
        route: str,
        headers: Dict = None,
        params: Dict = None,
        **kwargs
    ) -> requests.Response:
        """
        Sends an HTTP DELETE request.

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
            'DELETE',
            route,
            headers=headers,
            params=params,
            **kwargs
        )
        return response

    @cache_response
    def options(
        self,
        route: str,
        headers: Dict = None,
        params: Dict = None,
        **kwargs
    ) -> requests.Response:
        """
        Sends an HTTP OPTIONS request.

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
            'OPTIONS',
            route,
            headers=headers,
            params=params,
            **kwargs
        )
        return response

    @cache_response
    def trace(
        self,
        route: str,
        headers: Dict = None,
        params: Dict = None,
        **kwargs
    ) -> requests.Response:
        """
        Sends an HTTP TRACE request.

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
            'TRACE',
            route,
            headers=headers,
            params=params,
            **kwargs
        )
        return response


class SessionAPI(abstracts.AbstractSession, BasicAPI):
    """
    Implements a session-based API.

    The SessionAPI class implements the same interface as the BasicAPI; however, it
    overrides the `request` method to use requests.Session. In addition, the class
    provides `start` and `stop` methods to allow manual control of the session.

    The SessionAPI class can also be used as a context manager.

    Args:
        url: Base URL for API.
        auth: Authorization or credentials.
        headers (optional): Headers to set globally for API.
        params (optional): Parameters to set globally for API.
        adapter (optional): Instance of an HTTPAdapter.
        session (optional): Instance of a requests.Session.
        cache (optional): Mutable mapping for caching responses.

    .. Requests Documentation:
        https://docs.python-requests.org/en/latest/api/#request-sessions

    """

    def __init__(
            self,
            url: str,
            auth: Union[AuthBase, Tuple] = None,
            *,
            headers: Dict = None,
            params: Dict = None,
            adapter: HTTPAdapter = None,
            session: requests.Session = None,
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
        self.session = session

    @final
    def __enter__(self):
        """
        Starts the API session as a context manager.
        """
        self.start()

    @final
    def __exit__(self, *args):
        """
        Closes the API session as a context manager.
        """
        self.close()

    def start(self) -> None:
        """
        Begins an API session.
        """
        log.debug("Starting API session...")

        # Create session
        if not self.session:
            self.session = requests.Session()

        # Set autherization
        if self.auth and not self.session.auth:
            self.session.auth = self.auth

        # Add default headers
        if self.headers:
            self.session.headers.update(self.headers)

        # Mount transport adapter
        if self.adapter:
            self.session.mount("https://", self.adapter)
            self.session.mount("http://", self.adapter)

        return self.session

    def close(self, *args) -> None:
        """
        Manually destroys the API session.
        """
        log.debug("Closing API session...")
        self.session.close()

    def request(
        self,
        method: str,
        route: str,
        headers: Dict = None,
        params: Dict = None,
        **kwargs
    ) -> requests.Response:
        """
        Sends an HTTP request.

        Args:
            method: HTTP request method to use (HEAD, GET, POST, PUT, DELETE, OPTIONS, or TRACE).
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
        log.debug(
            "Sending HTTP %(method)s request to %(uri)s",
            {'method': method, 'uri': uri}
        )

        if self.session:
            response = self.session.request(
                method,
                uri,
                headers=merge(self.headers, headers),
                params=merge(self.params, params),
                **kwargs
            )

        else:
            log.warning("Session not started: start() method not called before sending request")
            response = super().request(
                method,
                uri,
                headers=headers,
                params=params,
                **kwargs
            )

        return response
