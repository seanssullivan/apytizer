# -*- coding: utf-8 -*-
"""Abstract API class interface.

This module defines an abstract API class which provides an interface
for subclasses to implement. Each of the abstract methods represents
a standard HTTP request method.

"""

# Third-Party Imports
import abc
from typing import Dict, Tuple, Union

# Third-Party Imports
from requests import Response
from requests.auth import HTTPBasicAuth


class AbstractAPI(abc.ABC):
    """
    Represents an abstract API.
    """
    url: str
    auth: Union[HTTPBasicAuth, Tuple]

    @abc.abstractmethod
    def head(self, endpoint: str, headers: Dict = None, **kwargs) -> Response:
        """
        Abstract method for sending an HTTP HEAD request.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/HEAD

        """
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, endpoint: str, headers: Dict = None, **kwargs) -> Response:
        """
        Abstract method for sending an HTTP GET request.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/GET

        """
        raise NotImplementedError

    @abc.abstractmethod
    def post(self, endpoint: str, headers: Dict = None, **kwargs) -> Response:
        """
        Abstract method for sending an HTTP POST request.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST

        """
        raise NotImplementedError

    @abc.abstractmethod
    def put(self, endpoint: str, headers: Dict = None, **kwargs) -> Response:
        """
        Abstract method for sending an HTTP PUT request.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PUT

        """
        raise NotImplementedError

    @abc.abstractmethod
    def patch(self, endpoint: str, headers: Dict = None, **kwargs) -> Response:
        """
        Abstract method for sending an HTTP PATCH request.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PATCH

        """
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, endpoint: str, headers: Dict = None, **kwargs) -> Response:
        """
        Abstract method for sending an HTTP DELETE request.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/DELETE

        """
        raise NotImplementedError

    @abc.abstractmethod
    def options(self, endpoint: str, headers: Dict = None, **kwargs) -> Response:
        """
        Abstract method for sending an HTTP OPTIONS request.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/OPTIONS

        """
        raise NotImplementedError

    @abc.abstractmethod
    def trace(self, endpoint: str, headers: Dict = None, **kwargs) -> Response:
        """
        Abstract method for sending an HTTP TRACE request.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/TRACE

        """
        raise NotImplementedError
