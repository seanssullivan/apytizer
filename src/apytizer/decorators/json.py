# -*- coding: utf-8 -*-
# src/apytizer/decorators/json.py

# Standard Library Imports
import functools
import json
import logging
from typing import Callable, Dict, List, Union

# Third-Party Importd
from requests import Response


# Initialize logger.
log = logging.getLogger(__name__)

# Define constants.
APPLICATION_JSON = "application/json"


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
        if response.status_code == 204:  # No content
            return response

        if not APPLICATION_JSON in response.headers.get("Content-Type"):
            return response

        try:
            log.debug("Parsing JSON response...")
            return response.json()

        except json.JSONDecodeError as error:
            log.error(error)
            return response

    functools.update_wrapper(wrapper, func)
    return wrapper
