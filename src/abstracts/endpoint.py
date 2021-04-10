# -*- coding: utf-8 -*-

# Third-Party Imports
import abc


class AbstractEndpoint(abc.ABC):
    """
    Represents an abstract endpoint.
    """

    @abc.abstractmethod
    def head(self, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def post(self, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def put(self, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def options(self, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def trace(self, *args, **kwargs):
        raise NotImplementedError
