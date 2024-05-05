# -*- coding: utf-8 -*-

# Standard Library Import
from typing import Callable
from typing import Hashable
from typing import Tuple

# Third-Party Imports
from cachetools.keys import hashkey

__all__ = ["generate_key"]


def generate_key(*tags: str) -> Callable[..., Tuple[Hashable, ...]]:
    """Generates a hashable key for caching values.

    Args:
        *tags: Tags.

    """

    def hash_parameters(*args, **kwargs) -> Tuple[Hashable, ...]:
        """Hashes function parameters."""
        key = hashkey(
            *tags, *args, *[f"{k!s}={v!s}" for k, v in sorted(kwargs.items())]
        )
        return key

    return hash_parameters
