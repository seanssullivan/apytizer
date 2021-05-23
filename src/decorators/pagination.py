# -*- coding: utf-8 -*-

# Standard Library Imports
import functools
import logging
from typing import Callable


log = logging.getLogger(__name__)


def pagination(func) -> Callable:
    """
    Args:
        func: Decorated function.

    Returns:
        Function wrapper.

    """
    @functools.wraps(func)
    def wrapper(*args, reducer: Callable, callback: Callable, **kwargs):
        """
        Wrapper applied to decorated function.

        Args:
            reducer (Callable): Function to update state with pagination metadata.
            callback (Callable): Function which returns True once request is completed.
                Stop condition must depend on state or pagination metadata.
            *args
            **kwargs

        """
        completed = False
        state = {
            'params': kwargs.pop('params', None),
            'data': kwargs.pop('data', None)
        }

        while not completed:
            if state.get('params'):
                kwargs.update({'params': state.get('params')})

            if state.get('data'):
                kwargs.update({'data': state.get('data')})

            response = func(*args, **kwargs)
            yield response

            state = reducer(state, response)
            completed = callback(state, response)

    return wrapper
