# -*- coding: utf-8 -*-

# Standard Library Imports
import functools
import logging
from typing import Callable, Dict, List, Union

# Third-Party Importd
from requests import Response


log = logging.getLogger(__name__)


def json_response(func: Callable) -> Callable:
    """
    Automatically parses a JSON response.

    Args:
        func: Function to decorate.

    Returns:
        Wrapped function.

    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Union[Dict, List, Response]:
        log.debug('Parsing JSON response...')
        response = func(*args, **kwargs)
        return response.json() \
            if response.headers.get('Content-Type') == "application/json" \
            else response

    return wrapper
