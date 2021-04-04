# -*- coding: utf-8 -*-

# Standard Library Imports
from urllib.parse import urljoin

# Third-Party Imports
import logging

# Local Imports
from ..abstracts.endpoint import AbstractEndpoint


class BasicEndpoint(AbstractEndpoint):
    """
    Class for interacting with an API endpoint.
    """

    def __init__(self, api, route: str = ''):
        self.api = api
        self.url = urljoin(self.api.url, route)

    def add(self, data: dict):
        """
        Create a new object on the API.
        """
        response = self.api.post(self.url, data=data)
        return response

    def all(self):
        """
        Get all available objects.
        """
        response = self.api.get(self.url)
        return response

    def get(self, ref: int or str):
        """
        Get object details from API.
        """
        call = urljoin(self.url, str(ref))
        response = self.api.get(call)
        return response

    def update(self, ref: int or str, data: dict):
        """
        Update object(s) on the API.
        """
        call = urljoin(self.url, str(ref))
        response = self.api.put(call, data=data)
        return response

    def delete(self, ref: int or str):
        """
        Delete object(s).
        """
        call = urljoin(self.url, str(ref))
        response = self.api.delete(call)
        return response
