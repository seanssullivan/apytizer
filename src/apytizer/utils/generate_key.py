# -*- coding: utf-8 -*-

# Third-Party Imports
from cachetools.keys import hashkey


def generate_key(*tags):
    """Generates a hashable key for caching values."""

    def hash_parameters(*args, **kwargs):
        """Hashes function parameters."""
        key = hashkey(
            *tags, *args,
            *[f"{k!s}={v!s}" for k, v in sorted(kwargs.items())]
        )
        return key

    return hash_parameters
