# -*- coding: utf-8 -*-
# src/apytizer/adapters/transport_adapter.py
"""Transport Adapter.

This module defines a transport adapter class: an implementation of an
HTTPAdapter which handles exponential backoff for retrying requests and
provides default values for rate limiting and request timeout.

"""

# Standard Library Imports
from http import HTTPStatus
from urllib3.util import Retry

# Third-Party Imports
from requests import PreparedRequest
from requests import Response
from requests.adapters import HTTPAdapter

__all__ = ["TransportAdapter"]


# Define constants.
DEFAULT_RATE_LIMIT = 1
NUMBER_OF_RETRIES = 10


class TransportAdapter(HTTPAdapter):
    """Implementation of a transport adaptor.

    Transport adapters define methods for interacting with HTTP services,
    enabling the use of per-service configurations.

    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault(
            "max_retries",
            Retry(
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
                backoff_factor=kwargs.pop("rate_limit", DEFAULT_RATE_LIMIT),
            ),
        )
        self.timeout = kwargs.pop("timeout", 5)
        super().__init__(*args, **kwargs)

    def send(self, request: PreparedRequest, **kwargs) -> Response:
        kwargs.setdefault("timeout", self.timeout)
        return super().send(request, **kwargs)
