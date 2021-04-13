# -*- coding: utf-8 -*-

# Standard Library Imports
# import logging
from urllib.parse import urljoin

# Third-Party Imports
import requests

# Local Imports
from ..abstracts.api import AbstractAPI
from ..abstracts.endpoint import AbstractEndpoint


# log = logging.getLogger(__name__)


class BasicEndpoint(AbstractEndpoint):
    """
    Class for interacting with an API endpoint.
    """

    def __init__(self, api: AbstractAPI, path: str, headers: dict = None, methods: list = None):
        self.api = api
        self.path = path if path[0] != "/" else path[1:]
        self.headers = headers
        self.methods = methods

    def __call__(self, ref: int or str = None, headers: dict = None, **kwargs) -> requests.Response:
        """
        Calling an instance of an endpoint performs a simple HTTP GET request.
        """
        return self.get(ref, headers, **kwargs)

    # def __getitem__(self, ref: int or str):
    #     """
    #     Returns a new endpoint with the appended reference.
    #     """
    #     return BasicEndpoint(self.api, f'{self.path!s}/{ref!s}', headers=self.headers)

    @property
    def url(self):
        return urljoin(self.api.url, self.path)

    def head(self, headers: dict = None, **kwargs) -> requests.Response:
        """
        Sends an HTTP HEAD request to API endpoint.
        """
        if self.methods and 'HEAD' not in self.methods:
            raise NotImplementedError

        headers = dict(self.headers, **headers) if headers else self.headers
        response = self.api.head(self.url, headers=self.headers, **kwargs)
        return response

    def get(self, ref: int or str = None, headers: dict = None, **kwargs) -> requests.Response:
        """
        Sends an HTTP GET request to API endpoint.
        """
        if self.methods and 'GET' not in self.methods:
            raise NotImplementedError

        call = f"{self.path!s}/{ref!s}" if ref else self.path
        headers = dict(self.headers, **headers) if headers else self.headers
        response = self.api.get(call, headers=self.headers, **kwargs)
        return response

    def post(self, data: dict, headers: dict = None, **kwargs) -> requests.Response:
        """
        Sends an HTTP POST request to API endpoint.
        """
        if self.methods and 'POST' not in self.methods:
            raise NotImplementedError

        headers = dict(self.headers, **headers) if headers else self.headers
        response = self.api.post(self.path, headers=self.headers, data=data, **kwargs)
        return response

    def put(self, ref: int or str, data: dict, headers: dict = None, **kwargs) -> requests.Response:
        """
        Sends an HTTP PUT request to API endpoint.
        """
        if self.methods and 'PUT' not in self.methods:
            raise NotImplementedError

        call = f"{self.path!s}/{ref!s}"
        headers = dict(self.headers, **headers) if headers else self.headers
        response = self.api.put(call, headers=self.headers, data=data, **kwargs)
        return response

    def delete(self, ref: int or str, headers: dict = None, **kwargs) -> requests.Response:
        """
        Sends an HTTP DELETE request to API endpoint.
        """
        if self.methods and 'DELETE' not in self.methods:
            raise NotImplementedError

        call = f"{self.path!s}/{ref!s}"
        headers = dict(self.headers, **headers) if headers else self.headers
        response = self.api.delete(call, headers=self.headers, **kwargs)
        return response

    def options(self, headers: dict = None, **kwargs) -> requests.Response:
        """
        Sends an HTTP OPTIONS request to API endpoint.
        """
        if self.methods and 'OPTIONS' not in self.methods:
            raise NotImplementedError

        headers = dict(self.headers, **headers) if headers else self.headers
        response = self.api.options(self.url, headers=self.headers, **kwargs)
        return response

    def trace(self, headers: dict = None, **kwargs) -> requests.Response:
        """
        Sends an HTTP TRACE request to API endpoint.
        """
        if self.methods and 'TRACE' not in self.methods:
            raise NotImplementedError

        headers = dict(self.headers, **headers) if headers else self.headers
        response = self.api.trace(self.url, headers=self.headers, **kwargs)
        return response
