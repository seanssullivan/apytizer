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


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# logging.disable(logging.CRITICAL)'


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

    def start_session(self) -> None:
        """
        Begins an API session.
        """
        logging.debug("Starting API session")

        self.session = requests.Session()
        self.session.auth = self.auth
        self.session.headers.update(self.headers)

        # Mount transport adapter
        adapter = TransportAdapter(timeout=self.timeout)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
        return

    def end_session(self) -> None:
        """
        Manually destroys the API session.
        """
        logging.debug("Closing API session")

        self.session.close()
        return

    @confirm_connection
    @rate_limited
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
        logging.debug("Sending HTTP GET request")

        url = urljoin(self.base_url, endpoint)
        headers = dict(self.headers, **headers) if headers else self.headers

        logging.info(f"Request: GET {url}")

        if self.session:
            response = self.session.get(url, headers=headers, **kwargs)
        else:
            response = requests.get(url, auth=self.auth, headers=headers, **kwargs)

        return response

    @confirm_connection
    @rate_limited
    def post(self, endpoint: str, headers: dict = None, **kwargs) -> requests.Response:
        """
        Sends an HTTP POST request.

        Args:
            endpoint: API path to which the request will be sent.
            headers: Request headers (overrides global headers).
            **kwargs: Data or parameters to include in request.

        Returns:
            Response object.

        """
        logging.debug("Sending HTTP POST request")

        url = urljoin(self.base_url, endpoint)
        headers = dict(self.headers, **headers) if headers else self.headers

        logging.info(f"Request: POST {url}")

        if self.session:
            response = self.session.post(url, headers=headers, **kwargs)
        else:
            response = requests.post(url, auth=self.auth, headers=headers, **kwargs)

        return response

    @confirm_connection
    @rate_limited
    def put(self, endpoint: str, headers: dict = None, **kwargs) -> requests.Response:
        """
        Sends an HTTP PUT request.

        Args:
            endpoint: API path to which the request will be sent.
            headers: Request headers (overrides global headers).
            **kwargs: Data or parameters to include in request.

        Returns:
            Response object.

        """
        logging.debug("Sending HTTP PUT request")

        url = urljoin(self.base_url, endpoint)
        headers = dict(self.headers, **headers) if headers else self.headers

        logging.info(f"Request: PUT {url}")

        if self.session:
            response = self.session.put(url, headers=headers, **kwargs)
        else:
            response = requests.put(url, auth=self.auth, headers=headers, **kwargs)

        return response

    @confirm_connection
    @rate_limited
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
        logging.debug("Sending HTTP DELETE request")

        url = urljoin(self.base_url, endpoint)
        headers = dict(self.headers, **headers) if headers else self.headers

        logging.info(f"Request: DELETE {url}")

        if self.session:
            response = self.session.delete(url, headers=headers, **kwargs)
        else:
            response = requests.delete(url, auth=self.auth, headers=headers, **kwargs)

        return response
