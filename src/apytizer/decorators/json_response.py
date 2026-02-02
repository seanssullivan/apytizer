# -*- coding: utf-8 -*-
# src/apytizer/decorators/json.py

# Standard Library Imports
import functools
from http import HTTPStatus
import json
import logging
from typing import Any
from typing import Callable

# Third-Party Imports
from requests import Response

# Local Imports
from ..media_types import MediaType

__all__ = ["json_response"]


log = logging.getLogger("apytizer")

# Constants
CONTENT_TYPE = "Content-Type"


def json_response(func: Callable[..., Response]) -> Callable[..., Any]:
    """Automatically parses a JSON response.

    Args:
        func: Function to decorate.

    Returns:
        Wrapped function.

    """

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        """Wrapper applied to decorated function.

        Args:
            *args: Positional arguments to pass to wrapped function.
            **kwargs: Keyword arguments to pass to wrapped function.

        Returns:
            Parsed JSON or Response.

        """
        response: Response = func(*args, **kwargs)
        if response.status_code == HTTPStatus.NO_CONTENT:
            return response

        content_type = response.headers.get(CONTENT_TYPE)
        if not content_type or MediaType.APPLICATION_JSON not in content_type:
            return response

        result = parse_json_response(response)
        return result

    functools.update_wrapper(wrapper, func)
    return wrapper


def parse_json_response(response: Response) -> Any:
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

    return result


def handle_decode_error(error: json.JSONDecodeError) -> None:
    """Handle decode errors.

    Args:
        error: JSONDecodeError error.

    """
    log.error(error)
