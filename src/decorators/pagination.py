# -*- coding: utf-8 -*-

# Standard Library Imports
import functools
import logging
from typing import Callable, Generator
from urllib.parse import urlparse

# Third-Party Imports
import requests


log = logging.getLogger(__name__)


def pagination(func):
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


class Pagination:
    """
     Args:
        func: Decorated function.
        reducer (optional): Function to update state with pagination metadata.
        callback (optional): Function which returns True once request is completed.
            Stop condition must depend on state or pagination metadata.

    """

    def __init__(
        self,
        func: Callable,
        reducer: Callable = None,
        callback: Callable = None
    ):
        self.func = func
        self.reducer = reducer
        self.callback = callback

    def __call__(
        self,
        *args,
        reducer: Callable = None,
        callback: Callable = None,
        **kwargs
    ) -> Generator:
        """
        Args:
            reducer (optional): Function to update state with pagination metadata.
            callback (optional): Function which returns True once request is completed.
                Stop condition must depend on state or pagination metadata.

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

            response = self.func(*args, **kwargs)
            yield response

            state = reducer(state, response) if reducer else self.reducer(state, response)
            completed = callback(state, response) if callback else self.callback(state, response)
