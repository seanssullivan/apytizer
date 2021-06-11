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


def merge(initial: Dict, new: Dict) -> Dict:
    """
    Combines two sets of headers.
    """
    headers = dict(initial, **new) if initial and new \
        else new if new and not initial \
        else initial

    return headers
