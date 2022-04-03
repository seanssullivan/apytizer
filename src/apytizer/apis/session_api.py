# -*- coding: utf-8 -*-
# src/apytizer/apis/session_api.py
"""Session API class.

This module defines the session API class implementation.

Todo:
    * Allow different adapters on separate protocols.

"""

# Standard Library Imports
import logging
from typing import Any, Dict, Iterable, MutableMapping, Optional, Tuple, Union
from typing import final
from urllib.parse import urljoin

# Third-Party Imports
import requests
from requests.adapters import HTTPAdapter
from requests.auth import AuthBase

# Local Imports
from .. import abstracts
from .base_api import BaseAPI
from ..decorators import confirm_connection
from ..http_methods import HTTPMethod
from ..protocols import Protocol
from ..utils import merge

__all__ = ["SessionAPI"]


# Initialize logger.
log = logging.getLogger(__name__)

# Define custom types.
Authentication = Union[AuthBase, Tuple[str, str]]
Cache = MutableMapping
Headers = Dict[str, str]
Parameters = Dict[str, Any]

# Define constants.
DEFAULT_PROTOCOLS = (Protocol.HTTP, Protocol.HTTPS)


class SessionAPI(abstracts.AbstractSession, BaseAPI):
    """Implements a session-based API.

    The SessionAPI class implements the same interface as the BasicAPI; however, it
    overrides the `request` method to use requests.Session. In addition, the class
    provides `start` and `stop` methods to allow manual control of the session.

    An instance of SessionAPI can also be used as a context manager.

    Args:
        url: Base URL for API.
        auth (optional): Authentication or credentials.
        headers (optional): Headers to set globally for API.
        params (optional): Parameters to set globally for API.
        adapter (optional): Instance of an HTTPAdapter.
        cache (optional): Mutable mapping for caching responses.

    .. Requests Documentation:
        https://docs.python-requests.org/en/latest/api/#request-sessions

    """

    def __init__(
        self,
        url: str,
        auth: Optional[Authentication] = None,
        *,
        headers: Optional[Headers] = None,
        params: Optional[Parameters] = None,
        adapter: Optional[HTTPAdapter] = None,
        cache: Optional[MutableMapping] = None,
    ):
        super().__init__(
            url,
            auth,
            headers=headers,
            params=params,
            cache=cache,
        )
        self.adapter = adapter
        self.session = None  # type: Optional[requests.Session]

    @final
    def __enter__(self):
        self.start()
        return self

    @final
    def __exit__(self, *args):
        self.close()

    @property
    def adapter(self) -> Optional[HTTPAdapter]:
        """Adapter for API requests.

        Raises:
            TypeError: if set to value of type other than HTTPAdapter.

        """
        return self._adapter

    @adapter.setter
    def adapter(self, value: Optional[HTTPAdapter]) -> None:
        if value and not isinstance(value, HTTPAdapter):
            message = f"expected HTTPAdapter, not {type(value)}"
            raise TypeError(message)

        self._adapter = value

    def start(self) -> None:
        """Starts the session."""
        log.debug("Starting API session...")

        factory = _RequestsSessionFactory()
        self.session = factory.make_session(
            self.adapter,
            self.auth,
            self.headers,
        )

    def close(self, *args) -> None:
        """Destroys the session."""
        log.debug("Closing API session...")

        if self.session is not None:
            self.session.close()
            self.session = None

    @confirm_connection
    def request(
        self,
        method: HTTPMethod,
        route: str,
        headers: Optional[Headers] = None,
        params: Optional[Parameters] = None,
        **kwargs,
    ) -> requests.Response:
        """Sends an HTTP request.

        Args:
            method: HTTP request method to use.
            route: API path to which the request will be sent.
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Additional arguments to pass to request.

        Returns:
            Response object.

        .. Requests Documentation:
            https://docs.python-requests.org/en/latest/api/

        """
        uri = urljoin(self.url, route)
        if self.session:
            log.debug(
                "Sending HTTP %(method)s request to %(uri)s",
                {"method": method.name, "uri": uri},
            )

            response = self.session.request(
                method.name,
                uri,
                headers=merge(self.headers, headers),
                params=merge(self.params, params),
                **kwargs,
            )

            log.debug(
                "Received response with status code %(status)s",
                {"status": response.status_code},
            )

        else:
            log.warning(
                "%(event)s: %(reason)s",
                {
                    "event": "Session not started",
                    "reason": "start() was not called before sending request",
                },
            )
            response = super().request(
                method,
                uri,
                headers=headers,
                params=params,
                **kwargs,
            )

        return response


class _RequestsSessionBuilder:
    """Implements a builder for requests sessions."""

    _session: requests.Session

    def __init__(self) -> None:
        self.reset()

    @property
    def session(self) -> requests.Session:
        """Constructed session."""
        result = self._session
        self.reset()
        return result

    def reset(self) -> None:
        """Reset build cycle."""
        self._session = requests.Session()

    def include_adapter(
        self,
        adapter: HTTPAdapter,
        *,
        protocols: Iterable[Protocol] = DEFAULT_PROTOCOLS,
    ) -> None:
        """Add adapter to session.

        Args:
            adapter: Adapter to mount to session.
            protocols (optional): Protocols on which to mount adapter.

        """
        for protocol in protocols:
            log.debug(
                "Mounting %(adapter)s adapter to %(protocol)s protocol",
                {"adapter": adapter, "protoc0l": protocol.name},
            )
            prefix = f"{protocol.value!s}://"
            self._session.mount(prefix, adapter)

    def include_auth(self, auth: Authentication) -> None:
        """Add authentication to session."""
        self._session.auth = auth

    def include_default_headers(self, headers: Headers) -> None:
        """Add default headers to session."""
        self._session.headers.update(headers)


class _RequestsSessionFactory:
    """Implements a factory for requests sessions."""

    def __init__(self) -> None:
        self.builder = _RequestsSessionBuilder()

    def make_session(
        self,
        adapter: Optional[HTTPAdapter] = None,
        auth: Optional[Authentication] = None,
        headers: Optional[Headers] = None,
    ) -> requests.Session:
        """Make requests session.

        Args:
            adapter (optional): Instance of an HTTPAdapter.
            auth (optional): Authentication or credentials.
            headers (optional): Headers to set for all requests.

        Returns:
            Requests Session.

        """
        if adapter is not None:
            self.builder.include_adapter(adapter)

        if auth is not None:
            self.builder.include_auth(auth)

        if headers is not None:
            self.builder.include_default_headers(headers)

        result = self.builder.session
        return result
