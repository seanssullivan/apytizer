# -*- coding: utf-8 -*-
# src/apytizer/endpoints.py
"""Composite endpoint class.

This module defines the composite endpoint class implementation.

"""

# Standard Library Imports
from __future__ import annotations
import functools
import logging
from typing import Any, Dict, Iterable, Iterator, MutableMapping, Optional, Set

# Local Imports
from .. import abstracts
from .base_endpoint import BaseEndpoint, DEFAULT_METHODS
from ..http_methods import HTTPMethod
from ..utils import iter_setattr

__all__ = ["CompositeEndpoint"]


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

    _parent: CompositeEndpoint = None

    def __init__(
        self,
        api: abstracts.AbstractAPI,
        name: str,
        *,
        methods: Optional[Iterable[HTTPMethod]] = DEFAULT_METHODS,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        cache: Optional[MutableMapping] = None,
    ):
        super().__init__(
            api,
            name,
            methods=methods,
            headers=headers,
            params=params,
            cache=cache,
        )
        self.children = _Children(self)

    @property
    def name(self) -> str:
        """Name of endpoint."""
        return self._path

    @property
    def parent(self) -> CompositeEndpoint:
        """Parent endpoint."""
        return self._parent

    @parent.setter
    def parent(self, parent: BaseEndpoint) -> None:
        if not isinstance(parent, CompositeEndpoint):
            message = f"expected an endpoint, got {type(parent)} instead"
            raise TypeError(message)

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
        if not isinstance(path, str):
            message = f"expected type str, got {type(path)} instead"
            raise TypeError(message)

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
    def __add__(self, __endpoint: Any) -> CompositeEndpoint:
        """Adds a child endpoint."""
        raise NotImplementedError

    @functools.singledispatchmethod
    def __getattr__(self, __endpoint: str) -> CompositeEndpoint:
        """Gets a child endpoint."""
        raise NotImplementedError

    @functools.singledispatchmethod
    def __getitem__(self, __endpoint: Any) -> CompositeEndpoint:
        """Gets a child endpoint."""
        raise NotImplementedError

    @functools.singledispatchmethod
    def __truediv__(self, __endpoint: Any) -> CompositeEndpoint:
        """Adds a child endpoint."""
        raise NotImplementedError

    @__add__.register
    @__truediv__.register
    def _(self, __endpoint: BaseEndpoint) -> BaseEndpoint:
        self._add_child(__endpoint)
        return __endpoint

    @__add__.register
    @__getitem__.register
    @__truediv__.register
    def _(self, __endpoint: int) -> BaseEndpoint:
        result = self._get_child(str(__endpoint))
        return result

    @__add__.register
    @__getattr__.register
    @__getitem__.register
    @__truediv__.register
    def _(self, __endpoint: str) -> BaseEndpoint:
        result = self._get_child(__endpoint)
        return result

    def _get_child(self, name: str, /) -> CompositeEndpoint:
        """Get child endpoint.

        Args:
            name: Name of endpoint.

        Returns:
            Child endpoint.

        """
        endpoint = self.children.get(name) or self._make_child(name)
        return endpoint

    def _make_child(self, name: str, /) -> CompositeEndpoint:
        """Make a child endpoint.

        Args:
            name: Name of endpoint.

        Returns:
            Child endpoint.

        """
        endpoint = CompositeEndpoint(self.api, name)
        self._add_child(endpoint)
        return endpoint

    def _add_child(self, endpoint: CompositeEndpoint, /) -> None:
        """Add endpoint as child.

        Args:
            endpoint: Endpoint to add as a child.

        """
        self.children.add(endpoint)


class _Children(abstracts.AbstractEndpointCollection):
    """Collection class for child endpoints.

    Args:
        __parent: Parent endpoint.
        endpoints (optional): Iterable object containing child endpoints.
            Default `None`.

    Raises:
        TypeError: if parent argument is not an endpoint.

    """

    _endpoints: Set[CompositeEndpoint]

    def __init__(
        self,
        __parent: CompositeEndpoint,
        endpoints: Optional[Iterable[CompositeEndpoint]] = None,
    ) -> None:
        __endpoints = (
            iter_setattr(endpoints, "parent", __parent)
            if endpoints is not None
            else None
        )

        self._endpoints = set(__endpoints or [])
        self.context = __parent

    @property
    def context(self) -> CompositeEndpoint:
        return self._context

    @context.setter
    def context(self, context: BaseEndpoint) -> None:
        if not isinstance(context, CompositeEndpoint):
            message = f"expected an endpoint, got {type(context)} instead"
            raise TypeError(message)

        self._context = context

    def __contains__(self, item: object) -> bool:
        return (
            item in self._endpoints
            if isinstance(item, abstracts.AbstractEndpoint)
            else False
        )

    def __getitem__(self, key: str) -> abstracts.AbstractEndpoint:
        return self.get(key)

    def __len__(self) -> int:
        return len(self._endpoints)

    def __iter__(self) -> Iterator:
        return iter(self._endpoints)

    def add(self, __child: CompositeEndpoint, /) -> None:
        """Add child endpoint."""
        __child.parent = self.context
        self._endpoints.add(__child)

    def clear(self) -> None:
        """Clear child endpoints."""
        self._endpoints.clear()

    def discard(self, __child: CompositeEndpoint, /) -> None:
        """Discard child endpoint."""
        self._endpoints.discard(__child)
        if __child.parent is self.context:
            del __child.parent

    def get(self, ref: str) -> Optional[CompositeEndpoint]:
        """Get child endpoint."""
        try:
            result = next(
                child for child in self._endpoints if child.name == ref
            )
        except StopIteration:
            return None
        else:
            return result

    def pop(self, ref: str, /) -> abstracts.AbstractEndpoint:
        """Pop endpoint from children."""
        endpoint = self.get(ref)
        if endpoint is not None:
            self.remove(endpoint)

        return endpoint

    def remove(self, __child: CompositeEndpoint, /) -> None:
        """Remove child endpoint."""
        self._endpoints.remove(__child)
        del __child.parent

    def update(self, *children: CompositeEndpoint) -> None:
        """Update children."""
        children = [
            iter_setattr(endpoints, "parent", self.context)
            for endpoints in children
        ]
        self._endpoints.update(*children)
