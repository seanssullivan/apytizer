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


def merge(*args: Dict) -> Dict:
    """
    Combines dictionaries.

    Args:
        *args: Dictionaries to merge.

    Returns:
        Merged dictionary.

    """
    result = {k: v for dictionary in args if dictionary for k, v in dictionary.items()}
    return result if result else None

    # headers = dict(first, **new) if first and new \
    #     else new if new and not first \
    #     else first

    # return headers
