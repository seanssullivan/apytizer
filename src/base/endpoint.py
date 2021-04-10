# -*- coding: utf-8 -*-

# Standard Library Imports
import logging
from urllib.parse import urljoin

# Local Imports
from ..abstracts.api import AbstractAPI
from ..abstracts.endpoint import AbstractEndpoint


log = logging.getLogger(__name__)


class BasicEndpoint(AbstractEndpoint):
    """
    Class for interacting with an API endpoint.
    """

    def __init__(self, api: AbstractAPI, path: str, headers: dict = None, methods: list = None):
        self.api = api
        self.path = path
        self.url = urljoin(api.url, path)
        self.headers = headers
        self.methods = methods

    def add(self, data: dict, headers: dict = None):
        """
        Creates a new object at the API endpoint.
        """
        if self.methods and 'POST' not in self.methods:
            raise NotImplementedError

        log.debug(f"Creating object at {self.url}")

        headers = dict(self.headers, **headers) if headers else self.headers
        response = self.api.post(self.path, headers=self.headers, data=data)
        return response

    def all(self, headers: dict = None):
        """
        Get all available objects from the API endpoint.
        """
        if self.methods and 'GET' not in self.methods:
            raise NotImplementedError

        log.debug(f"Listing objects at {self.url}")

        headers = dict(self.headers, **headers) if headers else self.headers
        response = self.api.get(self.path, headers=self.headers)
        return response

    def get(self, ref: int or str, headers: dict = None):
        """
        Get object details from the API endpoint.
        """
        if self.methods and 'GET' not in self.methods:
            raise NotImplementedError

        log.debug(f"Getting object at {self.url}")

        call = f"{self.path}/{str(ref)}"
        headers = dict(self.headers, **headers) if headers else self.headers
        response = self.api.get(call, headers=self.headers)
        return response

    def update(self, ref: int or str, data: dict, headers: dict = None):
        """
        Update an object on the API endpoint.
        """
        if self.methods and 'PUT' not in self.methods:
            raise NotImplementedError

        log.debug(f"Updating object at {self.url}")

        call = f"{self.path}/{str(ref)}"
        headers = dict(self.headers, **headers) if headers else self.headers
        response = self.api.put(call, headers=self.headers, data=data)
        return response

    def remove(self, ref: int or str, headers: dict = None):
        """
        Delete an object from the API endpoint.
        """
        if self.methods and 'DELETE' not in self.methods:
            raise NotImplementedError

        log.debug(f"Removing object at {self.url}")

        call = f"{self.path}/{str(ref)}"
        headers = dict(self.headers, **headers) if headers else self.headers
        response = self.api.delete(call, headers=self.headers)
        return response
