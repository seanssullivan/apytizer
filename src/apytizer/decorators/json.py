# -*- coding: utf-8 -*-

# Standard Library Imports
import functools
import logging
from typing import Callable, Dict, List, Union

# Third-Party Importd
from requests import Response


# Initialize logger.
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
        """
        Wrapper applied to decorated function.

        Args:
            *args: Positional arguments to pass to wrapped function.
            **kwargs: Keyword arguments to pass to wrapped function.

        """

        response = func(*args, **kwargs)  # type: Response

        log.debug("Parsing JSON response...")
        return (
            response.json()
            if "application/json" in response.headers.get("Content-Type")
            else response
        )

    functools.update_wrapper(wrapper, func)
    return wrapper
