# -*- coding: utf-8 -*-
# src/apytizer/decorators/chunking.py

# Standard Library Imports
import functools
from typing import Any
from typing import Callable
from typing import Dict
from typing import Iterable
from typing import List
from typing import Union

# Third-Party Imports
from requests import Response

# Local Imports
from .. import utils

__all__ = ["chunked_request"]


def chunked_request(
    max_size: int,
) -> Callable[..., Callable[..., Union[Dict[str, Any], Response]]]:
    """Split request payload based on maximum request size.

    Args:
        max_size: Maximum size of request.

    Returns:
        Wrapped function.

    """

    def decorator(
        func: Callable[[Any, List[Any]], Union[Dict[str, Any], Response]],
    ) -> Callable[..., Union[Dict[str, Any], Response]]:
        """Decorator function for handling chunking.

        Args:
            func: Decorated function.

        Returns:
            Wrapped function.

        """

        @functools.wraps(func)
        def wrapper(
            self: Any, data: List[Any], *args: Any, **kwargs: Any
        ) -> Union[Dict[str, Any], Response]:
            """Wrapper applied to decorated function.

            Args:
                data: Data to chunk into multiple requests.
                *args: Positional arguments to pass to wrapped function.
                **kwargs: Keyword arguments to pass to wrapped function.

            Returns:
                Results.

            """
            if not isinstance(data, Iterable):  # type: ignore
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
    response: Union[Dict[str, List[Any]], Response],
) -> Dict[str, Any]:
    """Update results with response data.

    Args:
        results: Results to update.
        response: Response with which to update results.

    Returns:
        Updated results.

    """
    if isinstance(response, Response) and response.ok:
        return results

    if not isinstance(response, dict):  # type: ignore
        message = f"expected type `dict`, got {type(response)} instead"
        raise TypeError(message)

    for key, value in response.items():
        results.setdefault(key, [])
        results[key].extend(value)

    return results
