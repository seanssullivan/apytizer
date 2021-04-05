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

    def add(self, data: dict):
        """
        Creates a new object at the API endpoint.
        """
        logging.debug(f"Creating object at {self.url}")

        response = self.api.post(self.url, headers=self.headers, data=data)
        return response

    def all(self):
        """
        Get all available objects from the API endpoint.
        """
        logging.debug(f"Listing objects at {self.url}")

        response = self.api.get(self.url, headers=self.headers)
        return response

    def get(self, ref: int or str):
        """
        Get object details from the API endpoint.
        """
        logging.debug(f"Getting object at {self.url}")

        call = urljoin(self.url, str(ref))
        response = self.api.get(call, headers=self.headers)
        return response

    def update(self, ref: int or str, data: dict):
        """
        Update an object on the API endpoint.
        """
        logging.debug(f"Updating object at {self.url}")

        call = urljoin(self.url, str(ref))
        response = self.api.put(call, headers=self.headers, data=data)
        return response

    def delete(self, ref: int or str):
        """
        Delete an object from the API endpoint.
        """
        logging.debug(f"Removing object at {self.url}")

        call = urljoin(self.url, str(ref))
        response = self.api.delete(call, headers=self.headers)
        return response
