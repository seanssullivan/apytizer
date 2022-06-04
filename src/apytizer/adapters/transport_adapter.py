# -*- coding: utf-8 -*-
# src/apytizer/adapters/transport_adapter.py
"""Transport Adapter.

This module defines a transport adapter class: an implementation of an
HTTPAdapter which handles exponential backoff for retrying requests and
provides default values for rate limiting and timeout.

"""

# Standard Library Imports
from http import HTTPStatus
from urllib3.util import Retry

# Third-Party Imports
from requests import PreparedRequest
from requests import Response
from requests.adapters import HTTPAdapter

__all__ = ["TransportAdapter"]


# Constants
DEFAULT_RATE_LIMIT = 1
DEFAULT_TIMEOUT = 5
NUMBER_OF_RETRIES = 10


class TransportAdapter(HTTPAdapter):
    """Implementation of a transport adaptor.

    Transport adapters define methods for interacting with HTTP services,
    enabling the use of per-service configurations.

    Args:
        *args: Positional arguments.
        rate_limit (optional): Rate limit.
        timeout (optional): Timeout.
        **kwargs: Keyword arguments.

    """

    def __init__(
        self,
        *args,
        rate_limit: int = DEFAULT_RATE_LIMIT,
        timeout: int = DEFAULT_TIMEOUT,
        **kwargs,
    ):
        kwargs.setdefault("max_retries", make_retry(rate_limit))
        super().__init__(*args, **kwargs)
        self.timeout = timeout

    def send(self, request: PreparedRequest, *args, **kwargs) -> Response:
        kwargs.setdefault("timeout", self.timeout)
        return super().send(request, *args, **kwargs)


def make_retry(rate_limit: int) -> Retry:
    """Make retry configuration.

    Args:
        rate_limit: Rate limit for backoff factor.

    Returns:
        Retry configuration.

    """
    result = Retry(
        total=NUMBER_OF_RETRIES,
        status_forcelist=[
            HTTPStatus.REQUEST_ENTITY_TOO_LARGE,
            HTTPStatus.TOO_MANY_REQUESTS,
            HTTPStatus.INTERNAL_SERVER_ERROR,
            HTTPStatus.BAD_GATEWAY,
            HTTPStatus.SERVICE_UNAVAILABLE,
            HTTPStatus.GATEWAY_TIMEOUT,
        ],
        allowed_methods=[
            "HEAD",
            "GET",
            "POST",
            "PUT",
            "PATCH",
            "DELETE",
            "OPTIONS",
            "TRACE",
        ],
        backoff_factor=rate_limit,
    )
    return result
