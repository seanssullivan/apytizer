# -*- coding: utf-8 -*-
"""Abstract API class interface.

This module defines an abstract API class which provides an interface
for subclasses to implement. Each of the abstract methods represents
a standard HTTP request method.

"""

# Third-Party Imports
from __future__ import annotations
import abc
from typing import Dict, Tuple, Union

# Third-Party Imports
from requests import Response
from requests.auth import AuthBase


class AbstractAPI(abc.ABC):
    """
    Represents an abstract API.
    """
    url: str
    auth: Union[AuthBase, Tuple]

    def __eq__(self, other: AbstractAPI) -> bool:
        return other.url == self.url \
            and other.auth == self.auth

    def __hash__(self) -> int:
        return hash(self.url)

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__!s} url={self.url!s}>'

    @abc.abstractmethod
    def head(self, route: str, *args, headers: Dict = None, **kwargs) -> Response:
        """
        Abstract method for sending an HTTP HEAD request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/HEAD

        """
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, route: str, *args, headers: Dict = None, **kwargs) -> Response:
        """
        Abstract method for sending an HTTP GET request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/GET

        """
        raise NotImplementedError

    @abc.abstractmethod
    def post(self, route: str, *args, headers: Dict = None, **kwargs) -> Response:
        """
        Abstract method for sending an HTTP POST request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST

        """
        raise NotImplementedError

    @abc.abstractmethod
    def put(self, route: str, *args, headers: Dict = None, **kwargs) -> Response:
        """
        Abstract method for sending an HTTP PUT request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PUT

        """
        raise NotImplementedError

    @abc.abstractmethod
    def patch(self, route: str, *args, headers: Dict = None, **kwargs) -> Response:
        """
        Abstract method for sending an HTTP PATCH request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PATCH

        """
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, route: str, *args, headers: Dict = None, **kwargs) -> Response:
        """
        Abstract method for sending an HTTP DELETE request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/DELETE

        """
        raise NotImplementedError

    @abc.abstractmethod
    def options(self, route: str, *args, headers: Dict = None, **kwargs) -> Response:
        """
        Abstract method for sending an HTTP OPTIONS request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/OPTIONS

        """
        raise NotImplementedError

    @abc.abstractmethod
    def trace(self, route: str, *args, headers: Dict = None, **kwargs) -> Response:
        """
        Abstract method for sending an HTTP TRACE request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/TRACE

        """
        raise NotImplementedError
