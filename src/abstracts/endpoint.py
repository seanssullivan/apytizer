# -*- coding: utf-8 -*-

# Third-Party Imports
import abc


class AbstractEndpoint(abc.ABC):
    """
    Represents an abstract endpoint.
    """

    @abc.abstractmethod
    def add(self, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def list(self, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, *args, **kwargs):
        raise NotImplementedError
