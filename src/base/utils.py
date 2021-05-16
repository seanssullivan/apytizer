# -*- coding: utf-8 -*-

# Standard Library Imports
from typing import Dict

# Third-Party Imports
from cachetools.keys import hashkey


def generate_key(*tags):
    """Generates a hashable key for caching values."""

    def hash_parameters(*args, **kwargs):
        """Hashes function parameters."""
        key = hashkey(*tags, *args, *[f"{k!s}={v!s}" for k, v in kwargs.items()])
        return key

    return hash_parameters


def merge_headers(initial_headers: Dict, new_headers: Dict) -> Dict:
    """
    Combines two sets of headers.
    """
    headers = dict(initial_headers, **new_headers) if initial_headers and new_headers \
        else new_headers if new_headers and not initial_headers \
        else initial_headers
    return headers
