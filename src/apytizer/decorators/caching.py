# -*- coding: utf-8 -*-

# Standard Library Imports
import functools
import logging
import operator
from typing import Callable

# Third-Party Imports
from cachetools import cachedmethod

# Local Imports
from ..utils import generate_key


log = logging.getLogger(__name__)


def cache_response(func: Callable) -> Callable:
    """
    Decorator function for handling caching.

    Args:
        func: Decorated function.

    Return:
        Wrapped function.

    """
    @functools.wraps(func)
    @cachedmethod(operator.attrgetter('cache'), key=generate_key(func.__name__.upper()))
    def wrapper(*args, **kwargs):
        """Wrapper applied to decorated function."""
        return func(*args, **kwargs)

    return wrapper
