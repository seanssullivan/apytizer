# -*- coding: utf-8 -*-

# Standard Library Imports
import logging
from urllib.parse import urljoin

# Third-Party Imports
import requests

# Local Imports
from ..abstracts.api import AbstractAPI
from ..base.adapters import TransportAdapter
from .decorators import confirm_connection
from .decorators import rate_limited


log = logging.getLogger(__name__)


class BasicAPI(AbstractAPI):
    """
    Implements a basic API.
    """

    def __init__(
            self,
            url: str,  # ----------------------------- Base URL for API.
            auth: tuple,  # -------------------------- API authorization (includes user's API token)
            headers: dict,  # ------------------------ Global headers (including content-type)
            rate_limit: int = 0,  # ------------------ Number of seconds to debounce requests
            timeout: int = 5,  # --------------------- Number of seconds to wait before timing out
            session: requests.Session = None,  # ----- Session object
    ):
        self.base_url = url
        self.auth = auth
        self.headers = headers
        self.timeout = timeout
        self.session = session

        # Request settings:
        self._time_of_previous_request = 0
        self._wait_between_requests = rate_limit


    @property
    def url(self):
        return self.base_url

    def start(self) -> None:
        """
        Begins an API session.
        """
        log.debug("Starting API session")

        self.session = requests.Session()
        self.session.auth = self.auth
        self.session.headers.update(self.headers)

        # Mount transport adapter
        adapter = self.adapter if self.adapter else TransportAdapter(timeout=self.timeout)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
        return

    def close(self) -> None:
        """
        Manually destroys the API session.
        """
        log.debug("Closing API session")
        self.session.close()
        return

    @confirm_connection
    @rate_limited
    def request(self, method: str, endpoint: str, headers: dict = None, **kwargs) -> requests.Response:
        """
        Sends an HTTP request.

        Args:
            method: HTTP request method to use (HEAD, GET, POST, PUT, DELETE, OPTIONS, or TRACE).
            endpoint: API path to which the request will be sent.
            headers: Request headers (overrides global headers).
            **kwargs: Data or parameters to include in request.

        Returns:
            Response object.

        """
        log.debug(f'Sending HTTP {method} request')

        url = urljoin(self.base_url, endpoint)
        log.info(f"Request: {method} {url}")

        headers = dict(self.headers, **headers) if headers else self.headers

        if self.session:
            response = self.session.request(method, url, headers=headers, **kwargs)
        else:
            response = requests.request(method, url, auth=self.auth, headers=headers, **kwargs)

        return response

    def head(self, endpoint: str, headers: dict = None, **kwargs) -> requests.Response:
        """
        Sends an HTTP HEAD request.

        Args:
            endpoint: API path to which the request will be sent.
            headers: Request headers (overrides global headers).
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
            headers: Request headers (overrides global headers).
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
            headers: Request headers (overrides global headers).
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
            headers: Request headers (overrides global headers).
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
            headers: Request headers (overrides global headers).
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
            headers: Request headers (overrides global headers).
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
            headers: Request headers (overrides global headers).
            **kwargs: Data or parameters to include in request.

        Returns:
            Response object.

        """
        response = self.request('TRACE', endpoint, headers=headers, **kwargs)
        return response

