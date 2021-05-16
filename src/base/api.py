# -*- coding: utf-8 -*-
"""Basic API class.

This module defines a basic API class implementation.

"""

# Standard Library Imports
import logging
from typing import Dict, MutableMapping, Tuple, Union
from urllib.parse import urljoin

# Third-Party Imports
import requests
from requests.adapters import HTTPAdapter
from requests.auth import HTTPBasicAuth

# Local Imports
from ..abstracts.api import AbstractAPI


log = logging.getLogger(__name__)


class BasicAPI(AbstractAPI):
    """
    Implements a basic API.

    The BasicAPI class provides an interface for interacting with a REST API.
    It implements the standard HTTP methods (HEAD, GET, POST, PUT, PATCH, DELETE, OPTIONS and TRACE)
    as well as a `requests` method for sending a custom HTTP request.

    Args:
        url: Base URL for API.
        auth: Authorization or credentials.
        headers (optional): Headers to set globally for API.
        cache (optional): Mutable mapping for caching responses.

    .. Requests Documentation:
        https://docs.python-requests.org/en/latest/

    """

    def __init__(
        self,
        url: str,
        auth: Union[HTTPBasicAuth, Tuple] = None,
        *,
        headers: Dict = None,
        cache: MutableMapping = None
    ):
        self.url = url
        self.auth = auth
        self.headers = headers
        self.cache = cache

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__!s} url={self.url!s}>'

    def request(
        self,
        method: str,
        route: str,
        headers: Dict = None,
        **kwargs
    ) -> requests.Response:
        """
        Sends an HTTP request.

        Args:
            method: HTTP request method to use (HEAD, GET, POST, PUT, DELETE, OPTIONS, or TRACE).
            route: API path to which the request will be sent.
            headers (optional): Request headers (overrides global headers).
            **kwargs: Data or parameters to include in request.

        Returns:
            Response object.

        .. Requests Documentation:
            https://docs.python-requests.org/en/latest/api/

        """
        log.debug("Sending HTTP %(method)s request", {'method': method})

        uri = urljoin(self.url, route)
        log.info("Request: %(method)s %(uri)s", {'method': method, 'uri': uri})

        headers = dict(self.headers, **headers) if self.headers and headers \
            else headers if headers and not self.headers \
            else self.headers

        response = requests.request(method, uri, auth=self.auth, headers=headers, **kwargs)
        return response

    def head(
        self,
        route: str,
        headers: Dict = None,
        **kwargs
    ) -> requests.Response:
        """
        Sends an HTTP HEAD request.

        Args:
            route: API path to which the request will be sent.
            headers (optional): Request headers (overrides global headers).
            **kwargs: Data or parameters to include in request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/HEAD

        """
        response = self.request('HEAD', route, headers=headers, **kwargs)
        return response

    def get(self, route: str, headers: Dict = None, **kwargs) -> requests.Response:
        """
        Sends an HTTP GET request.

        Args:
            route: API path to which the request will be sent.
            headers (optional): Request headers (overrides global headers).
            **kwargs: Data or parameters to include in request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/GET

        """
        response = self.request('GET', route, headers=headers, **kwargs)
        return response

    def post(self, route: str, data: Dict = None, headers: Dict = None, **kwargs) -> requests.Response:
        """
        Sends an HTTP POST request.

        Args:
            route: API path to which the request will be sent.
            headers (optional): Request headers (overrides global headers).
            **kwargs: Data or parameters to include in request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST

        """
        response = self.request('POST', route, data=data, headers=headers, **kwargs)
        return response

    def put(self, route: str, data: Dict = None, headers: Dict = None, **kwargs) -> requests.Response:
        """
        Sends an HTTP PUT request.

        Args:
            route: API path to which the request will be sent.
            headers (optional): Request headers (overrides global headers).
            **kwargs: Data or parameters to include in request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PUT

        """
        response = self.request('PUT', route, data=data, headers=headers, **kwargs)
        return response

    def patch(self, route: str, data: Dict = None, headers: Dict = None, **kwargs) -> requests.Response:
        """
        Sends an HTTP PATCH request.

        Args:
            route: API path to which the request will be sent.
            headers (optional): Request headers (overrides global headers).
            **kwargs: Data or parameters to include in request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PATCH

        """
        response = self.request('PATCH', route, data=data, headers=headers, **kwargs)
        return response

    def delete(self, route: str, headers: Dict = None, **kwargs) -> requests.Response:
        """
        Sends an HTTP DELETE request.

        Args:
            route: API path to which the request will be sent.
            headers (optional): Request headers (overrides global headers).
            **kwargs: Data or parameters to include in request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/DELETE

        """
        response = self.request('DELETE', route, headers=headers, **kwargs)
        return response

    def options(self, route: str, headers: Dict = None, **kwargs) -> requests.Response:
        """
        Sends an HTTP OPTIONS request.

        Args:
            route: API path to which the request will be sent.
            headers (optional): Request headers (overrides global headers).
            **kwargs: Data or parameters to include in request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/OPTIONS

        """
        response = self.request('OPTIONS', route, headers=headers, **kwargs)
        return response

    def trace(self, route: str, headers: Dict = None, **kwargs) -> requests.Response:
        """
        Sends an HTTP TRACE request.

        Args:
            route: API path to which the request will be sent.
            headers (optional): Request headers (overrides global headers).
            **kwargs: Data or parameters to include in request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/TRACE

        """
        response = self.request('TRACE', route, headers=headers, **kwargs)
        return response



class SessionAPI(BasicAPI):
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
        adapter (optional): Instance of an HTTPAdapter.
        session (optional): Instance of a requests.Session.
        cache (optional): Mutable mapping for caching responses.

    .. Requests Documentation:
        https://docs.python-requests.org/en/latest/api/#request-sessions

    """

    def __init__(
            self,
            url: str,
            auth: Union[HTTPBasicAuth, Tuple] = None,
            *,
            headers: Dict = None,
            adapter: HTTPAdapter = None,
            session: requests.Session = None,
            cache: MutableMapping = None,
    ):
        super().__init__(url, auth, headers=headers, cache=cache)
        self.adapter = adapter
        self.session = session

    def __enter__(self):
        """
        Starts the API session as a context manager.
        """
        self.start()

    def __exit__(self, *args):
        """
        Closes the API session as a context manager.
        """
        self.close()

    def start(self) -> None:
        """
        Begins an API session.
        """
        log.debug("Starting API session")

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

    def close(self) -> None:
        """
        Manually destroys the API session.
        """
        log.debug("Closing API session")
        self.session.close()
        return

    def request(self, method: str, route: str, headers: Dict = None, **kwargs) -> requests.Response:
        """
        Sends an HTTP request.

        Args:
            method: HTTP request method to use (HEAD, GET, POST, PUT, DELETE, OPTIONS, or TRACE).
            route: API path to which the request will be sent.
            headers (optional): Request headers (overrides global headers).
            **kwargs: Data or parameters to include in request.

        Returns:
            Response object.

        .. Requests Documentation:
            https://docs.python-requests.org/en/latest/api/

        """
        log.debug("Sending HTTP %(method)s request", {'method': method})

        uri = urljoin(self.url, route)
        log.info("Request: %(method)s %(url)s", {'method': method, 'uri': uri})

        if self.session:
            headers = dict(self.headers, **headers) if self.headers and headers \
                else headers if headers and not self.headers \
                else self.headers

            response = self.session.request(method, uri, headers=headers, **kwargs)

        else:
            log.warning("session not started: start() method not called before sending request")
            response = super().request(method, uri, headers=headers, **kwargs)

        return response
