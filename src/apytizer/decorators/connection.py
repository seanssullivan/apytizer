# -*- coding: utf-8 -*-
# src/apytizer/decorators/connection.py

# Standard Library Imports
import functools
import logging
from typing import Callable

# Third-Party Imports
import requests


# Initialize logger.
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
    def wrapper(self, *args, **kwargs) -> requests.Response:
        """
        Wrapper applied to decorated function.

        Args:
            *args: Positional arguments to pass to wrapped function.
            **kwargs: Keyword arguments to pass to wrapped function.

        """

        try:
            response = func(self, *args, **kwargs)  # type: requests.Response

        except requests.exceptions.ConnectionError as error:
            log.critical("Failed to establish a connection")
            log.error(error)
            return error

        except requests.exceptions.Timeout as error:
            log.critical("request timed out")
            log.error(error)
            return error

        else:
            log.debug(
                "Response received with status code %s",
                response.status_code,
            )
            return response

    functools.update_wrapper(wrapper, func)
    return wrapper
