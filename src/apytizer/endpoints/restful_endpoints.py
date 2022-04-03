# -*- coding: utf-8 -*-
# src/apytizer/endpoints/restful_endpoints.py
"""RESTful Endpoints.

This module defines endpoint classes for REST APIs.

"""

# Standard Library Imports
from __future__ import annotations
import logging
from typing import Any, Dict, Iterable, MutableMapping, Optional, Union

# Local Imports
from .composite_endpoint import CompositeEndpoint
from ..http_methods import HTTPMethod

__all__ = []


# Initialize logger.
log = logging.getLogger(__name__)


class CollectionEndpoint(CompositeEndpoint):
    """Implements a collection endpoint.

    Args:
        path: Relative URL path for endpoint.
        headers (optional): Headers to set globally for endpoint.
        params (optional): Parameters to set globally for endpoint.
        methods (optional): List of HTTP methods accepted by endpoint.
        cache (optional): Mutable mapping for caching responses.

    Attributes:
        api: Instance of an API subclass.
        path: Relative path to API endpoint.
        uri: Endpoint URL.

    """

    def __call__(
        self,
        ref: Union[int, str],
        *,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Any:
        """Gets a resource from the collection.

        Args:
            ref: Reference to resource.
            headers (optional): Request headers (overrides global headers).
            params (optional): Request parameters (overrides global parameters).
            **kwargs: Data or parameters to include in request.

        Returns:
            Response object.

        """
        if isinstance(ref, (int, str)):
            endpoint = ResourceEndpoint(self.api, f"{self.path!s}/{ref!s}")
            result = endpoint.get(headers=headers, params=params, **kwargs)
        else:
            raise TypeError

        return result


#     def __getitem__(self, ref: Union[int, str]) -> ResourceEndpoint:
#         """Returns a new endpoint with the appended reference.

#         This method is a shortcut for accessing HTTP methods on a
#         child endpoint or a nested resource.

#         Args:
#             ref: Reference to a nested resource.

#         Returns:
#             ResourceEndpoint instance.

#         Example:
#             Getting an item from an instance of a composite endpoint returns
#             a new endpoint with the appended reference string.

#             >>> endpoint = CollectionEndpoint(api, 'base')
#             >>> endpoint['ref'].uri
#             'api/base/ref'

#         """
#         if isinstance(ref, (int, str)):
#             endpoint = ResourceEndpoint(self.api, f"{self.path!s}/{ref!s}")
#         else:
#             raise TypeError

#         return endpoint


class ResourceEndpoint(CompositeEndpoint):
    """Implements a resource endpoint.

    Args:
        path: Relative URL path for endpoint.
        headers (optional): Headers to set globally for endpoint.
        params (optional): Parameters to set globally for endpoint.
        methods (optional): List of HTTP methods accepted by endpoint.
        cache (optional): Mutable mapping for caching responses.

    Attributes:
        api: Instance of an API subclass.
        path: Relative path to API endpoint.
        uri: Endpoint URL.

    """

    def __call__(
        self,
        ref: Union[int, str],
        *,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        methods: Optional[Iterable[HTTPMethod]] = None,
        cache: Optional[MutableMapping] = None,
    ) -> CompositeEndpoint:
        """Returns a new endpoint with the appended reference.

        This method is a shortcut for accessing HTTP methods on a
        child endpoint or a nested resource.

        Args:
            ref: Reference for a collection or nested resource.
            headers (optional) : Headers to set globally for endpoint.
            params (optional) : Parameters to set globally for endpoint.
            methods (optional): List of HTTP methods accepted by endpoint.
            cache (optional): Mutable mapping for caching responses.

        Returns:
            BaseEndpoint instance.

        Examples:
            Calling an instance of a basic endpoint returns a new endpoint
            with the appended reference string.

            >>> endpoint = BaseEndpoint(api, 'base')
            >>> endpoint('ref').uri
            'api/base/ref'

        """
        if isinstance(ref, (int, str)):
            endpoint = CollectionEndpoint(
                self.api,
                ref,
                headers=headers,
                params=params,
                methods=methods,
                cache=cache,
            )
        else:
            raise TypeError

        return endpoint


#     def __getattr__(self, name: str) -> CollectionEndpoint:
#         """Returns a new endpoint with the appended reference.

#         This method is a shortcut for accessing HTTP methods on a
#         child endpoint or a nested collection.

#         Args:
#             name: Name of nested collection.

#         Returns:
#             CollectionEndpoint instance.

#         Example:
#             Getting an attribute from an instance of a composite endpoint returns
#             a new endpoint with the appended reference string.

#            >>> endpoint = CollectionEndpoint(api, 'base')
#            >>> endpoint.name.uri
#            'api/base/name'

#         """
#         if isinstance(name, str):
#             endpoint = CollectionEndpoint(self.api, f"{self.path!s}/{name!s}")
#         else:
#             raise TypeError

#         return endpoint
