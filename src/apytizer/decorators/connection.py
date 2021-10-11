# -*- coding: utf-8 -*-

# Standard Library Imports
import functools
import logging
from typing import Callable

# Third-Party Imports
import requests


log = logging.getLogger(__name__)


def confirm_connection(func) -> Callable:
    """
    Confirms successful connection to API.

    Args:
        func: Function to decorate.

    Returns:
        Wrapped function.

    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            response = func(self, *args, **kwargs)

        except requests.exceptions.ConnectionError as error:
            log.critical("Failed to establish a connection")
            log.debug(f"Error message: {error}")
            return error

        except requests.exceptions.Timeout as error:
            log.critical("request timed out")
            log.debug(f"Error message: {error}")
            return error

        else:
            log.debug(
                "Response received with status code %(status)",
                {'status': response.status_code}
            )
            return response

    return wrapper
