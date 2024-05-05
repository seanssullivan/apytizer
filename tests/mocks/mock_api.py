# -*- coding: utf-8 -*-

# Standard Library Imports
import operator
from typing import Any
from typing import Dict
from typing import Optional
from unittest.mock import Mock

# Local Imports
try:
    from apytizer.apis import AbstractWebAPI
    from apytizer.engines import AbstractEngine
except ImportError:
    from src.apytizer.apis import AbstractWebAPI
    from src.apytizer.engines import AbstractEngine

__all__ = ["MockAPI"]


class MockAPI(AbstractWebAPI):
    def __init__(self, __engine: AbstractEngine, /) -> None:
        self._engine = __engine
        self._connection = self._engine.connect()

    @property
    def connection(self) -> Mock:
        """Connection."""
        return self._connection

    @property
    def url(self) -> str:
        """Base URL."""
        return self._engine.url

    def __eq__(self, other: object) -> bool:
        result = (
            other.url.strip("/").lower() == self.url.strip("/").lower()
            if isinstance(other, AbstractWebAPI)
            else False
        )
        return result

    def __hash__(self) -> int:
        result = hash(self.url)
        return result

    def head(
        self,
        route: str = "/",
        *,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Any:
        """Sends an HTTP HEAD request to the mock API.

        Args:
            route (optional): Route to which to send request. Default ``/``.
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Keyword arguments to include in request.

        Returns:
            Response object.

        """
        make_request = operator.methodcaller(
            "head",
            route,
            headers=headers,
            params=params,
            **kwargs,
        )
        response = make_request(self.connection)
        return response

    def get(
        self,
        route: str = "/",
        *,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Any:
        """Sends an HTTP GET request to the mock API.

        Args:
            route (optional): Route to which to send request. Default ``/``.
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Keyword arguments to include in request.

        Returns:
            Response object.

        """
        make_request = operator.methodcaller(
            "get",
            route,
            headers=headers,
            params=params,
            **kwargs,
        )
        response = make_request(self.connection)
        return response

    def post(
        self,
        route: str = "/",
        *,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Any:
        """Sends an HTTP POST request to the mock API.

        Args:
            route (optional): Route to which to send request. Default ``/``.
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Keyword arguments to include in request.

        Returns:
            Response object.

        """
        make_request = operator.methodcaller(
            "post",
            route,
            headers=headers,
            params=params,
            **kwargs,
        )
        response = make_request(self.connection)
        return response

    def put(
        self,
        route: str = "/",
        *,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Any:
        """Sends an HTTP PUT request to the mock API.

        Args:
            route (optional): Route to which to send request. Default ``/``.
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Keyword arguments to include in request.

        Returns:
            Response object.

        """
        make_request = operator.methodcaller(
            "put",
            route,
            headers=headers,
            params=params,
            **kwargs,
        )
        response = make_request(self.connection)
        return response

    def patch(
        self,
        route: str = "/",
        *,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Any:
        """Sends an HTTP PATCH request to the mock API.

        Args:
            route (optional): Route to which to send request. Default ``/``.
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Keyword arguments to include in request.

        Returns:
            Response object.

        """
        make_request = operator.methodcaller(
            "patch",
            route,
            headers=headers,
            params=params,
            **kwargs,
        )
        response = make_request(self.connection)
        return response

    def delete(
        self,
        route: str = "/",
        *,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Any:
        """Sends an HTTP DELETE request to the mock API.

        Args:
            route (optional): Route to which to send request. Default ``/``.
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Keyword arguments to include in request.

        Returns:
            Response object.

        """
        make_request = operator.methodcaller(
            "delete",
            route,
            headers=headers,
            params=params,
            **kwargs,
        )
        response = make_request(self.connection)
        return response

    def options(
        self,
        route: str = "/",
        *,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Any:
        """Sends an HTTP OPTIONS request to the mock API.

        Args:
            route (optional): Route to which to send request. Default ``/``.
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Keyword arguments to include in request.

        Returns:
            Response object.

        """
        make_request = operator.methodcaller(
            "options",
            route,
            headers=headers,
            params=params,
            **kwargs,
        )
        response = make_request(self.connection)
        return response

    def trace(
        self,
        route: str = "/",
        *,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Any:
        """Sends an HTTP TRACE request to the mock API.

        Args:
            route (optional): Route to which to send request. Default ``/``.
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Keyword arguments to include in request.

        Returns:
            Response object.

        """
        make_request = operator.methodcaller(
            "trace",
            route,
            headers=headers,
            params=params,
            **kwargs,
        )
        response = make_request(self.connection)
        return response
