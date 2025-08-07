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
        return cached_func(*args, **kwargs)

    functools.update_wrapper(wrapper, func)
    return wrapper
