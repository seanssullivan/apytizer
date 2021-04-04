# -*- coding: utf-8 -*-

# Third-Party Imports
import logging
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
            url: str,  # --------------- Base URL for API.
            auth: str or tuple,  # ----- API authorization (includes user's API token)
            headers: dict,  # ---------- Global headers (including content-type)
            rate_limit: int = 0,  # ---- Number of seconds to debounce requests
            timeout: int = 5,  # ------- Number of seconds to wait before timing out
    ):
        self.base_url = url
        self.auth = auth
        self.headers = headers

        # Request settings:
        self._time_of_previous_request = 0
        self._wait_between_requests = rate_limit
        self._timeout_after = timeout

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
        response = requests.get(endpoint, auth=self.auth, headers=headers, **kwargs)
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
        response = requests.post(endpoint, auth=self.auth, headers=headers, **kwargs)
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
        response = requests.put(endpoint, auth=self.auth, headers=headers, **kwargs)
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
        response = requests.delete(endpoint, auth=self.auth, headers=headers, **kwargs)
        return response
