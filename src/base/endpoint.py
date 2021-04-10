# -*- coding: utf-8 -*-

# Standard Library Imports
# import logging
from urllib.parse import urljoin

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

    @property
    def url(self):
        return urljoin(self.api.url, self.path)

    def head(self, headers: dict = None):
        """
        Sends an HTTP HEAD request to API endpoint.
        """
        if self.methods and 'HEAD' not in self.methods:
            raise NotImplementedError

        headers = dict(self.headers, **headers) if headers else self.headers
        response = self.api.head(self.url, headers=self.headers)
        return response

    def get(self, ref: int or str = None, headers: dict = None):
        """
        Sends an HTTP GET request to API endpoint.
        """
        if self.methods and 'GET' not in self.methods:
            raise NotImplementedError

        call = f"{self.path}/{str(ref)}" if ref else self.path
        headers = dict(self.headers, **headers) if headers else self.headers
        response = self.api.get(call, headers=self.headers)
        return response

    def post(self, data: dict, headers: dict = None):
        """
        Sends an HTTP POST request to API endpoint.
        """
        if self.methods and 'POST' not in self.methods:
            raise NotImplementedError

        headers = dict(self.headers, **headers) if headers else self.headers
        response = self.api.post(self.path, headers=self.headers, data=data)
        return response

    def put(self, ref: int or str, data: dict, headers: dict = None):
        """
        Sends an HTTP PUT request to API endpoint.
        """
        if self.methods and 'PUT' not in self.methods:
            raise NotImplementedError

        call = f"{self.path}/{str(ref)}"
        headers = dict(self.headers, **headers) if headers else self.headers
        response = self.api.put(call, headers=self.headers, data=data)
        return response

    def delete(self, ref: int or str, headers: dict = None):
        """
        Sends an HTTP DELETE request to API endpoint.
        """
        if self.methods and 'DELETE' not in self.methods:
            raise NotImplementedError

        call = f"{self.path}/{str(ref)}"
        headers = dict(self.headers, **headers) if headers else self.headers
        response = self.api.delete(call, headers=self.headers)
        return response

    def options(self, headers: dict = None):
        """
        Sends an HTTP OPTIONS request to API endpoint.
        """
        if self.methods and 'OPTIONS' not in self.methods:
            raise NotImplementedError

        headers = dict(self.headers, **headers) if headers else self.headers
        response = self.api.options(self.url, headers=self.headers)
        return response

    def trace(self, headers: dict = None):
        """
        Sends an HTTP TRACE request to API endpoint.
        """
        if self.methods and 'TRACE' not in self.methods:
            raise NotImplementedError

        headers = dict(self.headers, **headers) if headers else self.headers
        response = self.api.trace(self.url, headers=self.headers)
        return response


class EndpointFactory:
    """
    """

    def __init__(self, api: AbstractAPI):
        self.api = api

    def __call__(self, **kwargs):
        path = kwargs.get('path', '')
        headers = kwargs.get('headers')
        methods = kwargs.get('methods')
        endpoint = BasicEndpoint(self.api, path, headers, methods)
        return endpoint
