# -*- coding: utf-8 -*-

# Standard Library Imports
from __future__ import annotations
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

    @property
    def url(self):
        return urljoin(self.api.url, self.path)

    def __call__(self, ref: int or str = None, headers: dict = None, **kwargs) -> requests.Response:
        """
        Calling an instance of an endpoint performs a simple HTTP GET request.
        """

        return self.get(ref, headers, **kwargs)

    def __getitem__(self, ref: int or str) -> BasicEndpoint:
        """
        Returns a new endpoint with the appended reference.

        This method is a shortcut for accessing HTTP methods on a child endpoint or a nested resource.

        Args:
            ref: Reference for a nested resource or an object available through a resource collection endpoint.

        Returns:
            A new BasicEndpoint instance.

        """

        return BasicEndpoint(self.api, f'{self.path!s}/{ref!s}', headers=self.headers)

    def __add__(self, other: AbstractEndpoint or str) -> BasicEndpoint:
        """
        Returns a new endpoint after combining both paths.

        This is a method for quickly accessing HTTP methods for child endpoints or nested resources.
        It behaves exactly the same as the __truediv__ method.

        Args:
            other: Another endpoint-class object or a string to append to the current path.

        Returns:
            A new BasicEndpoint instance.

        """

        if isinstance(other, AbstractEndpoint):
            endpoint = BasicEndpoint(self.api, f'{self.path!s}/{other.path!s}', headers=self.headers)
        elif isinstance(other, str) or isinstance(other, int):
            endpoint = BasicEndpoint(self.api, f'{self.path!s}/{other!s}', headers=self.headers)
        else:
            raise TypeError

        return endpoint

    def __truediv__(self, other: AbstractEndpoint or str) -> BasicEndpoint:
        """
        Returns a new endpoint after combining both paths.

        This is a method for quickly accessing HTTP methods for child endpoints or nested resources.
        It behaves exactly the same as the __add__ method.

        Args:
            other: Another endpoint-class object or a string to append to the current path.

        Returns:
            A new BasicEndpoint instance.

        """

        if isinstance(other, AbstractEndpoint):
            endpoint = BasicEndpoint(self.api, f'{self.path!s}/{other.path!s}', headers=self.headers)
        elif isinstance(other, str) or isinstance(other, int):
            endpoint = BasicEndpoint(self.api, f'{self.path!s}/{other!s}', headers=self.headers)
        else:
            raise TypeError

        return endpoint

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
