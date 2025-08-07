# -*- coding: utf-8 -*-
# src/apytizer/connection/base_connection.py
"""HTTP Connection Class.

This module defines the base HTTP connection class implementation.

"""

# Standard Library Imports
import logging
from typing import Any
from typing import Dict
from typing import Optional
from typing import Tuple
from typing import Union
from typing import final
from typing import TYPE_CHECKING
from urllib.parse import urljoin

# Third-Party Imports
from requests import Request
from requests import Response

# Local Imports
from .abstract_connection import AbstractConnection
from ..decorators import confirm_connection
from ..http_methods import HTTPMethod
from ..sessions import AbstractSession
from ..sessions import sessionmaker
from .. import errors
from .. import utils

if TYPE_CHECKING:
    from ..engines import HTTPEngine

__all__ = ["HttpConnection"]


log = logging.getLogger("apytizer")

# Constants
DEFAULT_SESSION_FACTORY = sessionmaker()


class HttpConnection(AbstractConnection):
    """Implements an HTTP connection.

    The connection class provides an interface for interacting with an API.
    It implements the standard HTTP methods (HEAD, GET, POST, PUT, PATCH,
    DELETE, OPTIONS and TRACE) as well as a `request` method for sending
    custom HTTP requests.

    Args:
        engine: Engine.
        session_factory (optional): Function for creating sessions.

    """

    def __init__(
        self,
        engine: "HTTPEngine",
        *,
        session_factory: sessionmaker = DEFAULT_SESSION_FACTORY,
    ) -> None:
        self._engine = engine
        self._session_factory = session_factory

    @property
    def headers(self) -> Optional[Dict[str, str]]:
        """Connection headers."""
        return getattr(self._engine, "headers", None)

    @property
    def params(self) -> Optional[Dict[str, Any]]:
        """Connection parameters."""
        return getattr(self._engine, "params", None)

    @property
    def session(self) -> Optional[AbstractSession]:
        """Session."""
        return getattr(self, "_session", None)

    @property
    def timeout(self) -> Optional[Union[float, Tuple[float, float]]]:
        """Connection timeout."""
        return getattr(self._engine, "timeout", None)

    @property
    def url(self) -> str:
        """Connection URL."""
        return getattr(self._engine, "url")

    @final
    def __enter__(self) -> AbstractConnection:
        """Starts connection as context manager."""
        self.start()
        return self

    @final
    def __exit__(self, *_) -> None:
        """Ends connection as context manager."""
        self.close()

    def start(self) -> None:
        """Start connection."""
        session = self._session_factory(self._engine)
        setattr(self, "_session", session)
        session.start()

    def close(self) -> None:
        """Close connection."""
        if self.session is not None:
            self.session.close()

    def head(
        self,
        route: Optional[str] = None,
        *,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Optional[Response]:
        """Sends an HTTP HEAD request.

        Args:
            route (optional): Route to which to send request. Default ``None``.
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Additional arguments to pass to request.

        Returns:
            Response object.

        .. _HTTP HEAD Method:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/HEAD

        """
        response = self.request(
            HTTPMethod.HEAD,
            route,
            headers=headers,
            params=params,
            **kwargs,
        )
        return response

    def get(
        self,
        route: Optional[str] = None,
        *,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Optional[Response]:
        """Sends an HTTP GET request.

        Args:
            route (optional): Route to which to send request. Default ``None``.
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Additional arguments to pass to request.

        Returns:
            Response object.

        .. _HTTP GET Method:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/GET

        """
        response = self.request(
            HTTPMethod.GET,
            route,
            headers=headers,
            params=params,
            **kwargs,
        )
        return response

    def post(
        self,
        route: Optional[str] = None,
        *,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Optional[Response]:
        """Sends an HTTP POST request.

        Args:
            route (optional): Route to which to send request. Default ``None``.
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Additional arguments to pass to request.

        Returns:
            Response object.

        .. _HTTP POST Method:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST

        """
        response = self.request(
            HTTPMethod.POST,
            route,
            headers=headers,
            params=params,
            **kwargs,
        )
        return response

    def put(
        self,
        route: Optional[str] = None,
        *,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Optional[Response]:
        """Sends an HTTP PUT request.

        Args:
            route (optional): Route to which to send request. Default ``None``.
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Additional arguments to pass to request.

        Returns:
            Response object.

        .. _HTTP PUT Method:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PUT

        """
        response = self.request(
            HTTPMethod.PUT,
            route,
            headers=headers,
            params=params,
            **kwargs,
        )
        return response

    def patch(
        self,
        route: Optional[str] = None,
        *,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Optional[Response]:
        """Sends an HTTP PATCH request.

        Args:
            route (optional): Route to which to send request. Default ``None``.
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Additional arguments to pass to request.

        Returns:
            Response object.

        .. _HTTP PATCH Method:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PATCH

        """
        response = self.request(
            HTTPMethod.PATCH,
            route,
            headers=headers,
            params=params,
            **kwargs,
        )
        return response

    def delete(
        self,
        route: Optional[str] = None,
        *,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Optional[Response]:
        """Sends an HTTP DELETE request.

        Args:
            route (optional): Route to which to send request. Default ``None``.
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Additional arguments to pass to request.

        Returns:
            Response object.

        .. _HTTP DELETE Method:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/DELETE

        """
        response = self.request(
            HTTPMethod.DELETE,
            route,
            headers=headers,
            params=params,
            **kwargs,
        )
        return response

    def options(
        self,
        route: Optional[str] = None,
        *,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Optional[Response]:
        """Sends an HTTP OPTIONS request.

        Args:
            route (optional): Route to which to send request. Default ``None``.
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Additional arguments to pass to request.

        Returns:
            Response object.

        .. _HTTP OPTIONS Method:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/OPTIONS

        """
        response = self.request(
            HTTPMethod.OPTIONS,
            route,
            headers=headers,
            params=params,
            **kwargs,
        )
        return response

    def trace(
        self,
        route: Optional[str] = None,
        *,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Optional[Response]:
        """Sends an HTTP TRACE request.

        Args:
            route (optional): Route to which to send request. Default ``None``.
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Additional arguments to pass to request.

        Returns:
            Response object.

        .. _HTTP TRACE Method:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/TRACE

        """
        response = self.request(
            HTTPMethod.TRACE,
            route,
            headers=headers,
            params=params,
            **kwargs,
        )
        return response

    def request(
        self,
        method: HTTPMethod,
        /,
        route: Optional[str] = None,
        *,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Optional[Response]:
        """Sends an HTTP request.

        Args:
            method: HTTP request method to use.
            route (optional): Route to which to send request. Default ``None``.
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Additional arguments to pass to request.

        Returns:
            Response object.

        .. _Requests Documentation:
            https://docs.python-requests.org/en/latest/api/

        """
        request = Request(
            method.name,
            urljoin(self.url, route),
            headers=utils.merge(self.headers, headers),
            params=utils.merge(self.params, params),
            **kwargs,
        )
        response = self.send(request)
        return response

    @confirm_connection
    def send(self, request: Request) -> Optional[Response]:
        """Sends an HTTP request.

        Args:
            request: Request to send.

        Returns:
            Response object.

        """
        if self.session is None:
            message = "session not started before sending request"
            raise errors.SessionNotStarted(message)

        log.debug(
            "Sending HTTP %(method)s request to %(url)s",
            {"method": request.method, "url": request.url},
        )
        response = self.session.send(request, timeout=self.timeout)
        log.debug(
            "Received response with status code %(status)s",
            {"status": response.status_code},
        )
        return response
