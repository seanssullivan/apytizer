# -*- coding: utf-8 -*-

# Standard Library Imports
import logging

# Third-Party Imports
import requests

# Local Imports
from ..abstracts.api import AbstractAPI
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
        self.session = session

        # Request settings:
        self._time_of_previous_request = 0
        self._wait_between_requests = rate_limit
        self._timeout_after = timeout

    @property
    def url(self):
        return self.base_url

    def start_session(self) -> None:
        """
        Begins an API session.
        """
        logging.debug("Beginning API session")

        self.session = requests.Session()
        self.session.auth = self.auth
        self.session.headers.update(self.headers)
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
        :param endpoint: URL to which the request will be sent.
        :param headers: Request headers (overrides global headers).
        :return: Response object.
        """
        logging.debug("Sending HTTP GET request")

        headers = dict(self.headers, **headers) if headers else self.headers

        if not self.session:
            response = requests.get(endpoint, auth=self.auth, headers=headers, **kwargs)
        else:
            response = self.session.get(endpoint, headers=headers, **kwargs)

        return response

    @confirm_connection
    @rate_limited
    def post(self, endpoint: str, headers: dict = None, **kwargs) -> requests.Response:
        """
        Sends an HTTP POST request.
        :param endpoint: URL to which the request will be sent.
        :param headers: Request headers (overrides global headers).
        :param kwargs: Data to include in request.
        :return: Response object.
        """
        logging.debug("Sending HTTP POST request")

        headers = dict(self.headers, **headers) if headers else self.headers

        if not self.session:
            response = requests.post(endpoint, auth=self.auth, headers=headers, **kwargs)
        else:
            response = self.session.post(endpoint, headers=headers, **kwargs)

        return response

    @confirm_connection
    @rate_limited
    def put(self, endpoint: str, headers: dict = None, **kwargs) -> requests.Response:
        """
        Sends an HTTP PUT request.
        :param endpoint: URL to which the request will be sent.
        :param headers: Request headers (overrides global headers).
        :param kwargs: Data to include in request.
        :return: Response object.
        """
        logging.debug("Sending HTTP PUT request")

        headers = dict(self.headers, **headers) if headers else self.headers

        if not self.session:
            response = requests.put(endpoint, auth=self.auth, headers=headers, **kwargs)
        else:
            response = self.session.put(endpoint, headers=headers, **kwargs)

        return response

    @confirm_connection
    @rate_limited
    def delete(self, endpoint: str, headers: dict = None, **kwargs) -> requests.Response:
        """
        Sends an HTTP DELETE request.
        :param endpoint: URL to which the request will be sent.
        :param headers: Request headers (overrides global headers).
        :return: Response object.
        """
        logging.debug("Sending HTTP DELETE request")

        headers = dict(self.headers, **headers) if headers else self.headers

        if not self.session:
            response = requests.delete(endpoint, auth=self.auth, headers=headers, **kwargs)
        else:
            response = self.session.delete(endpoint, headers=headers, **kwargs)

        return response
