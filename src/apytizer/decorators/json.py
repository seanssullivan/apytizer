# -*- coding: utf-8 -*-
# src/apytizer/decorators/json.py

# Standard Library Imports
import functools
from http import HTTPStatus
import json
import logging
from typing import Callable, Dict, List, Union

# Third-Party Importd
from requests import Response

__all__ = ["json_response"]


# Initialize logger.
log = logging.getLogger(__name__)

# Define constants.
APPLICATION_JSON = "application/json"
CONTENT_TYPE = "Content-Type"


def json_response(func: Callable) -> Callable:
    """Automatically parses a JSON response.

    Args:
        func: Function to decorate.

    Returns:
        Wrapped function.

    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Union[Dict, List, Response]:
        """Wrapper applied to decorated function.

        Args:
            *args: Positional arguments to pass to wrapped function.
            **kwargs: Keyword arguments to pass to wrapped function.

        Returns:
            Parsed JSON or Response.

        """
        response = func(*args, **kwargs)  # type: Response
        if response.status_code == HTTPStatus.NO_CONTENT:
            return response

        content_type = response.headers.get(CONTENT_TYPE)
        if not content_type or APPLICATION_JSON not in content_type:
            return response

        result = parse_json_response(response)
        return result

    functools.update_wrapper(wrapper, func)
    return wrapper


def parse_json_response(response: Response) -> Union[Dict, List, Response]:
    """Parse JSON response.

    Args:
        response: JSON response.

    Returns:
        Parsed data.

    """
    try:
        log.debug("Parsing JSON response...")
        result = response.json()

    except json.JSONDecodeError as error:
        handle_decode_error(error)
        return response

    else:
        return result


def handle_decode_error(error: json.JSONDecodeError) -> None:
    """Handle decode errors.

    Args:
        error: JSONDecodeError error.

    """
    log.error(error)
