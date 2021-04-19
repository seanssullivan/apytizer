# -*- coding: utf-8 -*-

# Standard Library Imports
import logging
from urllib.parse import urljoin

# Third-Party Imports
import requests
from requests.adapters import HTTPAdapter

# Local Imports
from ..abstracts.api import AbstractAPI


log = logging.getLogger(__name__)


class BasicAPI(AbstractAPI):
    """
    Implements a basic API.

    Args:
        url: Base URL for API.
        auth: Authorization or credentials.
        headers (optional): Headers to set globally for API.

    """

    def __init__(
            self,
            url: str,
            auth: tuple = None,
            headers: dict = None
    ):
        self.url = url
        self.auth = auth
        self.headers = headers

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__!s} url={self.url!s}>'

    def request(self, method: str, endpoint: str, headers: dict = None, **kwargs) -> requests.Response:
        """
        Sends an HTTP request.

        Args:
            method: HTTP request method to use (HEAD, GET, POST, PUT, DELETE, OPTIONS, or TRACE).
            endpoint: API path to which the request will be sent.
            headers (optional): Request headers (overrides global headers).
            **kwargs: Data or parameters to include in request.

        Returns:
            Response object.

        """
        log.debug(f'Sending HTTP {method} request')

        url = urljoin(self.url, endpoint)
        log.info(f"Request: {method} {url}")

        headers = dict(self.headers, **headers) if headers else self.headers
        response = requests.request(method, url, auth=self.auth, headers=headers, **kwargs)
        return response

    def head(self, endpoint: str, headers: dict = None, **kwargs) -> requests.Response:
        """
        Sends an HTTP HEAD request.

        Args:
            endpoint: API path to which the request will be sent.
            headers (optional): Request headers (overrides global headers).
            **kwargs: Data or parameters to include in request.

        Returns:
            Response object.

        """
        response = self.request('HEAD', endpoint, headers=headers, **kwargs)
        return response

    def get(self, endpoint: str, headers: dict = None, **kwargs) -> requests.Response:
        """
        Sends an HTTP GET request.

        Args:
            endpoint: API path to which the request will be sent.
            headers (optional): Request headers (overrides global headers).
            **kwargs: Data or parameters to include in request.

        Returns:
            Response object.

        """
        response = self.request('GET', endpoint, headers=headers, **kwargs)
        return response

    def post(self, endpoint: str, data: dict = None, headers: dict = None, **kwargs) -> requests.Response:
        """
        Sends an HTTP POST request.

        Args:
            endpoint: API path to which the request will be sent.
            headers (optional): Request headers (overrides global headers).
            **kwargs: Data or parameters to include in request.

        Returns:
            Response object.

        """
        response = self.request('POST', endpoint, data=data, headers=headers, **kwargs)
        return response

    def put(self, endpoint: str, data: dict = None, headers: dict = None, **kwargs) -> requests.Response:
        """
        Sends an HTTP PUT request.

        Args:
            endpoint: API path to which the request will be sent.
            headers (optional): Request headers (overrides global headers).
            **kwargs: Data or parameters to include in request.

        Returns:
            Response object.

        """
        response = self.request('PUT', endpoint, data=data, headers=headers, **kwargs)
        return response

    def delete(self, endpoint: str, headers: dict = None, **kwargs) -> requests.Response:
        """
        Sends an HTTP DELETE request.

        Args:
            endpoint: API path to which the request will be sent.
            headers (optional): Request headers (overrides global headers).
            **kwargs: Data or parameters to include in request.

        Returns:
            Response object.

        """
        response = self.request('DELETE', endpoint, headers=headers, **kwargs)
        return response

    def options(self, endpoint: str, headers: dict = None, **kwargs) -> requests.Response:
        """
        Sends an HTTP OPTIONS request.

        Args:
            endpoint: API path to which the request will be sent.
            headers (optional): Request headers (overrides global headers).
            **kwargs: Data or parameters to include in request.

        Returns:
            Response object.

        """
        response = self.request('OPTIONS', endpoint, headers=headers, **kwargs)
        return response

    def trace(self, endpoint: str, headers: dict = None, **kwargs) -> requests.Response:
        """
        Sends an HTTP TRACE request.

        Args:
            endpoint: API path to which the request will be sent.
            headers (optional): Request headers (overrides global headers).
            **kwargs: Data or parameters to include in request.

        Returns:
            Response object.

        """
        response = self.request('TRACE', endpoint, headers=headers, **kwargs)
        return response



class SessionAPI(BasicAPI):
    """
    Implements a session-based API.

    Args:
        url: Base URL for API.
        auth: Authorization or credentials.
        headers (optional): Headers to set globally for API.
        adapter (optional): Instance of an HTTPAdapter.
        session (optional): Instance of a requests.Session.

    """

    def __init__(
            self,
            url: str,
            auth: tuple = None,
            headers: dict = None,
            adapter: HTTPAdapter = None,
            session: requests.Session = None,
    ):
        super().__init__(url, auth, headers)
        self.adapter = adapter
        self.session = session

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__!s} url={self.url!s}>'

    def __enter__(self):
        """
        Starts the API session as a context manager.
        """
        self.start()
        return super().__enter__()

    def __exit__(self, *args):
        """
        Closes the API session as a context manager.
        """
        super().__exit__(*args)
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

    def request(self, method: str, endpoint: str, headers: dict = None, **kwargs) -> requests.Response:
        """
        Sends an HTTP request.

        Args:
            method: HTTP request method to use (HEAD, GET, POST, PUT, DELETE, OPTIONS, or TRACE).
            endpoint: API path to which the request will be sent.
            headers (optional): Request headers (overrides global headers).
            **kwargs: Data or parameters to include in request.

        Returns:
            Response object.

        """
        log.debug(f'Sending HTTP {method} request')

        url = urljoin(self.url, endpoint)
        log.info(f"Request: {method} {url}")

        headers = dict(self.headers, **headers) if headers else self.headers

        if self.session:
            response = self.session.request(method, url, headers=headers, **kwargs)
        else:
            log.warning("session not started: start() method not called before sending request")
            response = super().request(method, url, headers=headers, **kwargs)

        return response
