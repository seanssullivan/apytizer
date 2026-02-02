# -*- coding: utf-8 -*-
# src/apytizer/decorators/caching.py

# Standard Library Imports
import functools
import operator
from typing import Any
from typing import Callable
from typing import TypeVar

# Third-Party Imports
from cachetools import cachedmethod

# Local Imports
from ..utils.caching import generate_key

__all__ = ["cache_response"]


# Custom types
T = TypeVar("T")


def cache_response(func: Callable[..., T]) -> Callable[..., T]:
    """Decorator function for handling caching.

    Args:
        func: Decorated function.

    Return:
        Wrapped function.

    """
    cached_func = cachedmethod(
        operator.attrgetter("cache"),
        key=generate_key(func.__name__.upper()),
    )(func)

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        """Wrapper applied to decorated function."""
        try:
            result = cached_func(*args, **kwargs)

        except TypeError as error:  # raised when cache is 'None'
            if is_missing_cache(error):
                result = func(*args, **kwargs)

            else:
                raise error

        return result

    functools.update_wrapper(wrapper, func)
    return wrapper


# ----------------------------------------------------------------------------
# Validators
# ----------------------------------------------------------------------------
def is_missing_cache(e: Exception) -> bool:
    """Check whether exception was raised because of missing cache.

    Args:
        e: Exception.

    Returns:
        Whether exception was raised because of missing cache.

    """
    expected = "'NoneType' object is not subscriptable"
    result = is_nonetype_error(e) and expected in str(e)
    return result


def is_nonetype_error(e: Exception) -> bool:
    """Check whether exception is 'NoneType' error.

    Args:
        e: Exception.

    Returns:
        Whether exception wis 'NoneType' error.

    """
    result = isinstance(e, TypeError) and "NoneType" in str(e)
    return result
