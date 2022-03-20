# -*- coding: utf-8 -*-
# src/apytizer/decorators/caching.py

# Standard Library Imports
import functools
import logging
import operator
from typing import Callable

# Third-Party Imports
from cachetools import cachedmethod

# Local Imports
from ..utils import generate_key

__all__ = ["cache_response"]


# Initialize logger.
log = logging.getLogger(__name__)


def cache_response(func: Callable) -> Callable:
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
    def wrapper(*args, **kwargs):
        """Wrapper applied to decorated function."""
        return cached_func(*args, **kwargs)

    functools.update_wrapper(wrapper, func)
    return wrapper
