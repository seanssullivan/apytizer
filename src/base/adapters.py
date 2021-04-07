# -*- coding: utf-8 -*-

# Standard Library Imports
from urllib3.util import Retry

# Third-Party Imports
from requests.adapters import HTTPAdapter


class TransportAdapter(HTTPAdapter):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_retries', Retry(
            total=10,
            status_forcelist=[413, 429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE"],
            backoff_factor=1
        ))
        self.timeout = kwargs.pop('timeout', 5)
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        kwargs.setdefault('timeout', self.timeout)
        return super().send(request, **kwargs)
