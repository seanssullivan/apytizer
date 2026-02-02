# -*- coding: utf-8 -*-
# src/apytizer/decorators/connection.py

# Standard Library Imports
import functools
import logging
from typing import Any
from typing import Callable
from typing import Optional

# Third-Party Imports
from requests import Response
from requests.exceptions import ConnectionError
from requests.exceptions import Timeout

__all__ = ["confirm_connection"]


log = logging.getLogger("apytizer")


def confirm_connection(
    func: Callable[..., Optional[Response]],
) -> Callable[..., Optional[Response]]:
    """Confirms successful connection to API.

    Args:
        func: Function to decorate.

    Returns:
        Wrapped function.

    """

    @functools.wraps(func)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Optional[Response]:
        """Wrapper applied to decorated function.

        Args:
            *args: Positional arguments to pass to wrapped function.
            **kwargs: Keyword arguments to pass to wrapped function.

        Returns:
            Response.

        """
        try:
            response = func(self, *args, **kwargs)

        except ConnectionError as error:
            handle_connection_error(error)
            return error.response

        except Timeout as error:
            handle_timeout_error(error)
            return error.response

        return response

    functools.update_wrapper(wrapper, func)
    return wrapper


def handle_connection_error(error: ConnectionError) -> None:
    """Handle connection errors.

    Args:
        error: Connection error.

    """
    log.critical("failed to establish a connection")
    log.error(error)


def handle_timeout_error(error: Timeout) -> None:
    """Handle timeout errors.

    Args:
        error: Timeout error.

    """
    log.critical("request timed out")
    log.error(error)
