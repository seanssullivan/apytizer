# -*- coding: utf-8 -*-
# src/apytizer/apis/abstract_api.py
"""Abstract Web API class.

This module defines an abstract API class which provides an interface
for subclasses to implement.

"""

# Standard Library Imports
from __future__ import annotations
import abc
from typing import Any
from typing import Dict
from typing import Optional

# Third-Party Imports
from requests import Response

# Local Imports
from ..connections import AbstractHttpConnection

__all__ = ["AbstractWebAPI"]


class AbstractWebAPI(abc.ABC):
    """Represents an abstract web API."""

    @property
    @abc.abstractmethod
    def connection(self) -> Optional[AbstractHttpConnection]:
        """Connection with which to make requests."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def url(self) -> str:
        """Base URL."""
        raise NotImplementedError

    @abc.abstractmethod
    def __eq__(self, other: object) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def __hash__(self) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def head(
        self,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Response:
        """Abstract method for sending an HTTP HEAD request.

        This method must call the `head` method on a `Connection` instance.

        Args:
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Keyword arguments to include in request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/HEAD

        """
        raise NotImplementedError

    @abc.abstractmethod
    def get(
        self,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Response:
        """Abstract method for sending an HTTP GET request.

        This method must call the `get` method on a `Connection` instance.

        Args:
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Keyword arguments to include in request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/GET

        """
        raise NotImplementedError

    @abc.abstractmethod
    def post(
        self,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Response:
        """Abstract method for sending an HTTP POST request.

        This method must call the `post` method on a `Connection` instance.

        Args:
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Keyword arguments to include in request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST

        """
        raise NotImplementedError

    @abc.abstractmethod
    def put(
        self,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Response:
        """Abstract method for sending an HTTP PUT request.

        This method must call the `put` method on a `Connection` instance.

        Args:
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Keyword arguments to include in request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PUT

        """
        raise NotImplementedError

    @abc.abstractmethod
    def patch(
        self,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Response:
        """Abstract method for sending an HTTP PATCH request.

        This method must call the `patch` method on a `Connection` instance.

        Args:
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Keyword arguments to include in request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PATCH

        """
        raise NotImplementedError

    @abc.abstractmethod
    def delete(
        self,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Response:
        """Abstract method for sending an HTTP DELETE request.

        This method must call the `delete` method on a `Connection` instance.

        Args:
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Keyword arguments to include in request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/DELETE

        """
        raise NotImplementedError

    @abc.abstractmethod
    def options(
        self,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Response:
        """Abstract method for sending an HTTP OPTIONS request.

        This method must call the `options` method on a `Connection` instance.

        Args:
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Keyword arguments to include in request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/OPTIONS

        """
        raise NotImplementedError

    @abc.abstractmethod
    def trace(
        self,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Response:
        """Abstract method for sending an HTTP TRACE request.

        This method must call the `trace` method on a `Connection` instance.

        Args:
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Keyword arguments to include in request.

        Returns:
            Response object.

        .. _MDN Web Docs:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/TRACE

        """
        raise NotImplementedError
