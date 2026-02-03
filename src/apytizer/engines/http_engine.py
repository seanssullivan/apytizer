# -*- coding: utf-8 -*-
# src/apytizer/engines/http_engine.py
"""HTTP Engine Class.

This module defines the HTTP engine class implementation.

"""

# Standard Library Imports
from collections import ChainMap
from typing import Any
from typing import MutableMapping
from typing import Optional
from typing import Tuple
from typing import Type
from typing import TypeVar
from typing import Union

# Third-Party Imports
from requests.auth import AuthBase
from requests.adapters import HTTPAdapter

# Local Imports
from .abstract_engine import AbstractEngine
from ..connections import HttpConnection
from ..protocols import Protocol
from ..protocols import get_protocol

__all__ = ["HTTPEngine"]


# Custom types:
T = TypeVar("T")


class HTTPEngine(AbstractEngine):
    """Implements an HTTP engine.

    Args:
        url: Base URL.
        adapters (optional): Connection adapters. Default ``None``.
        auth (optional): Authentication header. default ``None``.
        cert (optional): Client certificate. Default ``None``.
        headers (optional): Headers to set globally. Default ``None``.
        params (optional): Parameters to set globally. Default ``None``.
        proxies (optional): Protocols mapped to proxy URLs. Default ``None``.
        stream (optional): Whether to stream response content. Default ``False``.
        timeout (optional): How long to wait before timing out. Default ``None``.
        verify (optional): Whether to verify certificate. Default ``True``.

    Raises:
        TypeError: when URL of type other than `str`.

    """

    _connection_cls: Type[HttpConnection] = HttpConnection

    def __init__(
        self,
        url: str,
        *,
        adapters: Optional[MutableMapping[Protocol, HTTPAdapter]] = None,
        auth: Optional[Union[AuthBase, Tuple[str, str]]] = None,
        cert: Optional[Union[str, Tuple[str, str]]] = None,
        headers: Optional[MutableMapping[str, str]] = None,
        params: Optional[MutableMapping[str, Any]] = None,
        proxies: Optional[MutableMapping[str, str]] = None,
        stream: Optional[bool] = False,
        timeout: Optional[Union[float, Tuple[float, float]]] = None,
        verify: Optional[bool] = True,
    ) -> None:
        self._url = standardize_url(url)
        self._adapters = ChainMap(adapters or {})
        self._auth = auth
        self._cert = cert
        self._headers = ChainMap(headers or {})
        self._params = ChainMap(params or {})
        self._proxies = ChainMap(proxies or {})
        self._stream = stream or False
        self._timeout = timeout
        self._verify = verify

    @property
    def protocol(self) -> Optional[Protocol]:
        """Protocol."""
        result = get_protocol(self.url)
        return result

    @property
    def url(self) -> str:
        """Base URL."""
        return self._url

    @property
    def adapters(self) -> ChainMap[Protocol, HTTPAdapter]:
        """Connection adapters."""
        return self._adapters

    @property
    def auth(self) -> Optional[Union[AuthBase, Tuple[str, str]]]:
        """Authentication header."""
        return self._auth

    @property
    def cert(self) -> Optional[Union[str, Tuple[str, str]]]:
        """Certificate."""
        return self._cert

    @property
    def headers(self) -> ChainMap[str, str]:
        """Headers."""
        return self._headers

    @property
    def params(self) -> ChainMap[str, Any]:
        """Parameters."""
        return self._params

    @property
    def proxies(self) -> ChainMap[str, str]:
        """Proxies."""
        return self._proxies

    @property
    def stream(self) -> bool:
        """Whether response content will be streamed."""
        return self._stream

    @property
    def timeout(self) -> Optional[Union[float, Tuple[float, float]]]:
        """How long before request times out."""
        return self._timeout

    @property
    def verify(self) -> Optional[Union[float, Tuple[float, float]]]:
        """Whether certificate is verified."""
        return self._verify

    def __repr__(self) -> str:
        return f"Engine({self.url!r})"

    def connect(self) -> HttpConnection:
        """Establish connection.

        Returns:
            Connection instance.

        """
        result = self._connection_cls(self)
        return result


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
def standardize_url(__url: Any, /) -> str:
    """Standardize URL.

    Args:
        __url: URL.

    Returns:
        URL.

    """
    if not isinstance(__url, str):
        message = f"expected type 'str', got {type(__url)} instead"
        raise TypeError(message)

    result = __url if __url.endswith("/") else __url + "/"
    return result
