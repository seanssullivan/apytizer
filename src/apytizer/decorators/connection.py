# -*- coding: utf-8 -*-
# src/apytizer/decorators/connection.py

# Standard Library Imports
import functools
import logging
from typing import Callable

# Third-Party Imports
import requests
from requests.exceptions import ConnectionError
from requests.exceptions import Timeout

__all__ = ["confirm_connection"]


# Initialize logger.
log = logging.getLogger(__name__)


def confirm_connection(func) -> Callable:
    """Confirms successful connection to API.

    Args:
        func: Function to decorate.

    Returns:
        Wrapped function.

    """

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs) -> requests.Response:
        """Wrapper applied to decorated function.

        Args:
            *args: Positional arguments to pass to wrapped function.
            **kwargs: Keyword arguments to pass to wrapped function.

        Returns:
            Response.

        """
        try:
            response = func(self, *args, **kwargs)  # type: requests.Response

        except ConnectionError as error:
            _handle_connection_error(error)
            return error

        except Timeout as error:
            _handle_timeout_error(error)
            return error

        else:
            log.debug(
                "Response received with status code %s",
                response.status_code,
            )
            return response

    functools.update_wrapper(wrapper, func)
    return wrapper


def _handle_connection_error(error: ConnectionError) -> None:
    """Handle connection errors.

    Args:
        error: Connection error.

    """
    log.critical("Failed to establish a connection")
    log.error(error)


def _handle_timeout_error(error: Timeout) -> None:
    """Handle timeout errors.

    Args:
        error: Timeout error.

    """
    log.critical("request timed out")
    log.error(error)
