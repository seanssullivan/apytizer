# -*- coding: utf-8 -*-
# src/apytizer/engines/base_engine.py
"""Base engine class.

This module defines the base engine class implementation.

"""

# Standard Library Imports
from typing import Any
from typing import Dict
from typing import Mapping
from typing import Optional
from typing import Tuple
from typing import TypeVar
from typing import Union

# Third-Party Imports
from requests.adapters import HTTPAdapter

# Local Imports
from .abstract_engine import AbstractEngine
from ..connections import HttpConnection
from ..protocols import Protocol
from ..protocols import get_protocol
from ..utils import errors

__all__ = ["BaseEngine"]


# Custom types:
T = TypeVar("T")


class BaseEngine(AbstractEngine):
    """Implements an engine.

    Args:
        url: Base URL.
        adapters (optional): Connection adapters. Default ``None``.
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

    def __init__(
        self,
        url: str,
        *,
        adapters: Optional[Dict[Protocol, HTTPAdapter]] = None,
        cert: Optional[Union[str, Tuple[str, str]]] = None,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        proxies: Optional[Mapping] = None,
        stream: Optional[bool] = False,
        timeout: Optional[Union[float, Tuple[float, float]]] = None,
        verify: Optional[bool] = True,
    ) -> None:
        self.url = url
        self.adapters = adapters or {}
        self.cert = cert
        self.headers = headers
        self.params = params
        self.proxies = proxies
        self.stream = stream
        self.timeout = timeout
        self.verify = verify

    @property
    def protocol(self) -> Optional[Protocol]:
        """Protocol."""
        result = get_protocol(self.url)
        return result

    @property
    def url(self) -> str:
        """Base URL."""
        return self._url

    @url.setter
    def url(self, url: str) -> None:
        errors.raise_for_instance(url, str)
        self._url = url if url.endswith("/") else url + "/"

    def connect(self) -> HttpConnection:
        """Establish connection.

        Returns:
            Connection instance.

        """
        result = HttpConnection(self)
        return result
