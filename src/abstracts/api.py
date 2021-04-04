# -*- coding: utf-8 -*-

# Third-Party Imports
import abc


class AbstractAPI(abc.ABC):
    """
    Represents an abstract API.
    """

    @abc.abstractmethod
    def get(self, endpoint: str, headers: dict = None, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def post(self, endpoint: str, headers: dict = None, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def put(self, endpoint: str, headers: dict = None, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, endpoint: str, headers: dict = None, **kwargs):
        raise NotImplementedError
