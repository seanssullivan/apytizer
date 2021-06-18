# -*- coding: utf-8 -*-
"""Transport Adapter.

This module defines a transport adapter class: an implementation of an
HTTPAdapter which handles exponential backoff for retrying requests and
provides default values for rate limiting and request timeout.

"""

# Standard Library Imports
from urllib3.util import Retry

# Third-Party Imports
from requests import PreparedRequest
from requests import Response
from requests.adapters import HTTPAdapter


class TransportAdapter(HTTPAdapter):
    """
    Implementation of a transport adaptor.

    Transport adapters define methods for interacting with HTTP services,
    enabling the use of per-service configurations.

    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_retries', Retry(
            total=10,
            status_forcelist=[413, 429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "TRACE"],
            backoff_factor=kwargs.pop('rate_limit', 1)
        ))
        self.timeout = kwargs.pop('timeout', 5)
        super().__init__(*args, **kwargs)

    def send(self, request: PreparedRequest, **kwargs) -> Response:
        kwargs.setdefault('timeout', self.timeout)
        return super().send(request, **kwargs)
