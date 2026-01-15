# -*- coding: utf-8 -*-
# src/apytizer/sessions/requests_session.py
"""Requests Session Class.

This module defines the requests session class implementation.

"""

# Standard Library Imports
import logging
from typing import Any
from typing import Dict
from typing import MutableMapping
from typing import Optional
from typing import Tuple
from typing import Union
from typing import final

# Third-Party Imports
import requests
from requests.auth import AuthBase
from requests.adapters import HTTPAdapter

# Local Imports
from .abstract_session import AbstractSession
from ..protocols import Protocol

__all__ = ["RequestsSession"]


log = logging.getLogger("apytizer")


class RequestsSession(AbstractSession):
    """Implements a requests session.

    The `RequestsSession` class provides `start` and `close` methods for manual
    control of the session.

    A session instance can also be used as a context manager.

    Args:
        adapters (optional): Connection adapters. Default ``None``.
        auth (optional): Authentication header. default ``None``.
        cert (optional): Client certificate. Default ``None``.
        proxies (optional): Protocols mapped to proxy URLs. Default ``None``.
        stream (optional): Whether to stream response content. Default ``False``.
        verify (optional): Whether to verify certificate. Default ``True``.

    .. Requests Documentation:
        https://docs.python-requests.org/en/latest/api/#request-sessions

    """

    def __init__(
        self,
        *,
        adapters: Optional[Dict[Protocol, HTTPAdapter]] = None,
        auth: Optional[Union[AuthBase, Tuple[str, str]]] = None,
        cert: Optional[Union[str, Tuple[str, str]]] = None,
        proxies: Optional[MutableMapping[str, str]] = None,
        stream: Optional[bool] = False,
        verify: Optional[bool] = True,
    ) -> None:
        self._session = requests.Session()
        self._session.auth = auth
        self._session.cert = cert
        self._session.proxies = proxies  # type: ignore
        self._session.stream = stream  # type: ignore
        self._session.verify = verify  # type: ignore

        if adapters is not None:
            for protocol, adapter in adapters.items():
                self._session.mount(protocol, adapter)

    @final
    def __enter__(self) -> AbstractSession:
        """Starts session as context manager."""
        self.start()
        return self

    @final
    def __exit__(self, *_) -> None:
        """Stops session as context manager."""
        self.close()

    def start(self) -> None:
        """Starts session."""
        log.debug("Starting session...")

    def close(self, *_: Any) -> None:
        """Destroys session."""
        self._session.close()
        log.debug("Session closed")

    def mount(self, protocol: Protocol, adapter: HTTPAdapter) -> None:
        """Registers connection adapter to protocol prefix.

        Args:
            protocol: Protocol on which to mount adapter.
            adapter: HTTP adapter to apply to connection.

        """
        self._session.mount(f"{protocol.value!s}://", adapter)
        log.debug(
            "Mounted %(adapter)s adapter to %(protocol)s protocol",
            {"adapter": adapter, "protocol": protocol.value},
        )

    def send(
        self, __request: requests.Request, /, **kwargs: Any
    ) -> requests.Response:
        """Send an HTTP request.

        Args:
            __request: Request to send.
            **kwargs (optional): Keyword arguments.

        Returns:
            Response object.

        """
        request = self._session.prepare_request(__request)
        response = self._session.send(request, **kwargs)
        return response
