# -*- coding: utf-8 -*-
# src/apytizer/decorators/chunking.py

# Standard Library Imports
import functools
import logging
from typing import Any, Callable, Dict, Iterable, List, Union

# Third-Party Imports
from requests import Response

# Local Imports
from .. import utils

__all__ = ["chunked_request"]


# Initiate logger.
log = logging.getLogger(__name__)


def chunked_request(max_size: int) -> Callable:
    """Split request payload based on maximum request size.

    Args:
        max_size: Maximum size of request.

    Returns:
        Wrapped function.

    """

    def decorator(func: Callable[[list], Union[dict, Response]]) -> Callable:
        """Decorator function for handling chunking.

        Args:
            func: Decorated function.

        Returns:
            Wrapped function.

        """

        @functools.wraps(func)
        def wrapper(
            self, data: list, *args, **kwargs
        ) -> Union[dict, Response]:
            """Wrapper applied to decorated function.

            Args:
                data: Data to chunk into multiple requests.
                *args: Positional arguments to pass to wrapped function.
                **kwargs: Keyword arguments to pass to wrapped function.

            Returns:
                Results.

            """
            if not isinstance(data, Iterable):
                message = f"expected iterable object, got {type(data)} instead"
                raise TypeError(message)

            results = {}
            for group in utils.split_list(data, max_size):
                response = func(self, group, *args, **kwargs)
                results = update_results(results, response)

            return results

        functools.update_wrapper(wrapper, func)
        return wrapper

    return decorator


def update_results(
    results: Dict[str, List[Any]],
    response: Dict[str, List[Any]],
) -> Dict[str, Any]:
    """Update results with response data.

    Args:
        results: Results to update.
        response: Response with which to update results.

    Returns:
        Updated results.

    """
    if not isinstance(response, dict):
        message = f"expected type `dict`, got {type(response)} instead"
        raise TypeError(message)

    for key, value in response.items():
        results.setdefault(key, [])
        results[key].extend(value)

    return results
