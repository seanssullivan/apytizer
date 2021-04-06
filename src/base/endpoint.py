# -*- coding: utf-8 -*-

# Standard Library Imports
import logging
from urllib.parse import urljoin

# Local Imports
from ..abstracts.api import AbstractAPI
from ..abstracts.endpoint import AbstractEndpoint


class BasicEndpoint(AbstractEndpoint):
    """
    Class for interacting with an API endpoint.
    """

    def __init__(self, api: AbstractAPI, path: str, headers: dict = None):
        self.api = api
        self.url = urljoin(self.api.url, path)
        self.headers = headers

    def add(self, data: dict, headers: dict = None):
        """
        Creates a new object at the API endpoint.
        """
        logging.debug(f"Creating object at {self.url}")

        headers = dict(self.headers, **headers) if headers else self.headers
        response = self.api.post(self.url, headers=self.headers, data=data)
        return response

    def all(self, headers: dict = None):
        """
        Get all available objects from the API endpoint.
        """
        logging.debug(f"Listing objects at {self.url}")

        headers = dict(self.headers, **headers) if headers else self.headers
        response = self.api.get(self.url, headers=self.headers)
        return response

    def get(self, ref: int or str, headers: dict = None):
        """
        Get object details from the API endpoint.
        """
        logging.debug(f"Getting object at {self.url}")

        call = f"{self.url}/{str(ref)}"
        headers = dict(self.headers, **headers) if headers else self.headers
        response = self.api.get(call, headers=self.headers)
        return response

    def update(self, ref: int or str, data: dict, headers: dict = None):
        """
        Update an object on the API endpoint.
        """
        logging.debug(f"Updating object at {self.url}")

        call = f"{self.url}/{str(ref)}"
        headers = dict(self.headers, **headers) if headers else self.headers
        response = self.api.put(call, headers=self.headers, data=data)
        return response

    def delete(self, ref: int or str, headers: dict = None):
        """
        Delete an object from the API endpoint.
        """
        logging.debug(f"Removing object at {self.url}")

        call = f"{self.url}/{str(ref)}"
        headers = dict(self.headers, **headers) if headers else self.headers
        response = self.api.delete(call, headers=self.headers)
        return response
