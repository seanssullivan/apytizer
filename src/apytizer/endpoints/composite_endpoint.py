# -*- coding: utf-8 -*-
# src/apytizer/endpoints.py
"""Composite endpoint class.

This module defines the composite endpoint class implementation.

"""

# Standard Library Imports
from __future__ import annotations
import collections
import functools
import logging
from typing import Any, Collection, Dict, MutableMapping, Optional

# Local Imports
from .. import abstracts
from .base_endpoint import BaseEndpoint, DEFAULT_METHODS
from ..http_methods import HTTPMethod
from ..utils import errors

__all__ = ["CompositeEndpoint"]


# Define custom types.
AllowedMethods = Collection[HTTPMethod]
Cache = MutableMapping
Headers = Dict[str, str]
Parameters = Dict[str, Any]

# Initialize logger.
log = logging.getLogger(__name__)


class CompositeEndpoint(BaseEndpoint):
    """Implements a composite endpoint.

    Args:
        api: API instance.
        name: Name of endpoint.
        methods (optional): List of HTTP methods accepted by endpoint.
        headers (optional): Headers to set globally for endpoint.
        params (optional): Parameters to set globally for endpoint.
        cache (optional): Mutable mapping for caching responses.

    Attributes:
        uri: Endpoint URL.

    """

    _parent: Optional[abstracts.AbstractEndpoint] = None

    def __init__(
        self,
        api: abstracts.AbstractAPI,
        name: str,
        *,
        methods: AllowedMethods = DEFAULT_METHODS,
        headers: Optional[Headers] = None,
        params: Optional[Parameters] = None,
        cache: Optional[Cache] = None,
    ):
        super().__init__(
            api,
            name,
            methods=methods,
            headers=headers,
            params=params,
            cache=cache,
        )
        self.children = _Children()
        self.children.context = self

    @property
    def name(self) -> str:
        """Name of endpoint."""
        return self._path

    @property
    def parent(self) -> Optional[abstracts.AbstractEndpoint]:
        """Parent endpoint."""
        return self._parent

    @parent.setter
    def parent(self, parent: abstracts.AbstractEndpoint) -> None:
        errors.raise_for_instance(parent, CompositeEndpoint)
        self._parent = parent

    @parent.deleter
    def parent(self) -> None:
        self._parent = None

    @property
    def path(self) -> str:
        """Relative URL path."""
        return (
            f"{self.parent!s}/{self._path!s}"
            if self.parent is not None
            else self._path
        )

    @path.setter
    def path(self, path: str) -> None:
        errors.raise_for_instance(path, str)
        self._path = path.strip("/")

    def __eq__(self, other: object) -> bool:
        return (
            other.path == self.path
            if isinstance(other, CompositeEndpoint)
            else False
        )

    def __hash__(self) -> int:
        return hash(self.path)

    @functools.singledispatchmethod
    def __add__(self, __endpoint: Any) -> abstracts.AbstractEndpoint:
        """Adds a child endpoint."""
        raise NotImplementedError

    @functools.singledispatchmethod
    def __getattr__(self, __endpoint: str) -> abstracts.AbstractEndpoint:
        """Gets a child endpoint."""
        raise NotImplementedError

    @functools.singledispatchmethod
    def __getitem__(self, __endpoint: Any) -> abstracts.AbstractEndpoint:
        """Gets a child endpoint."""
        raise NotImplementedError

    @functools.singledispatchmethod
    def __truediv__(self, __endpoint: Any) -> abstracts.AbstractEndpoint:
        """Adds a child endpoint."""
        raise NotImplementedError

    @__add__.register
    @__truediv__.register
    def _add_child_endpoint(
        self, __endpoint: abstracts.AbstractEndpoint
    ) -> abstracts.AbstractEndpoint:
        key = __endpoint.path
        self.children[key] = __endpoint
        return __endpoint

    @__add__.register
    @__getattr__.register
    @__getitem__.register
    @__truediv__.register
    def _get_child_endpoint(
        self, __endpoint: str
    ) -> abstracts.AbstractEndpoint:
        result = self.children[__endpoint]
        return result


class _Children(collections.UserDict):
    """Collection class for child endpoints."""

    @property
    def context(self) -> abstracts.AbstractEndpoint:
        """Endpoint on which childen exist.

        Raises:
            TypeError: If provided context is not an endpoint.

        """
        return self._context

    @context.setter
    def context(self, context: abstracts.AbstractEndpoint) -> None:
        errors.raise_for_instance(context, BaseEndpoint)
        self._context = context

    def __missing__(self, key: str) -> abstracts.AbstractEndpoint:
        endpoint = CompositeEndpoint(self.context.api, key)
        self.data[key] = endpoint
        return endpoint

    def __setitem__(self, key: str, item: abstracts.AbstractEndpoint) -> None:
        setattr(item, "parent", self.context)
        self.data[key] = item

    def __delitem__(self, key: str) -> None:
        if key in self.data:
            delattr(self.data[key], "parent")
            del self.data[key]
