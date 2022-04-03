# -*- coding: utf-8 -*-
# src/apytizer/utils/objects.py

# Standard Library Imports
from typing import Any, Iterable, List

# Local Imports
from .typing import allinstance

__all__ = ["iter_getattr", "iter_setattr"]


def iter_getattr(__iter: Iterable[object], __name: str, /) -> List[Any]:
    """Get a named attribute from each object.

    Args:
        __iter: Iterable object containing objects.
        __name: Attribute for which to retrieve value.

    Raises:
        TypeError: when argument is not an iterable object.
        ValueError: when not all items are mappings.

    """
    if not isinstance(__iter, Iterable):
        raise TypeError("must be an iterable object")

    if not allinstance(__iter, object):
        raise ValueError("all items within iterator must be objects")

    results = [getattr(item, __name) for item in __iter]
    return results


def iter_setattr(
    __iter: Iterable[Any], __name: str, __value: str, /
) -> List[Any]:
    """Sets the named attribute to the specified value on each object.

    Args:
        __iter: Iterable object containing objects.
        __name: Attribute to set to value.
        value: Value to which to set attribute.

    Raises:
        TypeError: when argument is not an iterable object.
        ValueError: when not all items are objects.

    """
    if not isinstance(__iter, Iterable):
        raise TypeError("must be an iterable object")

    if not allinstance(__iter, object):
        raise ValueError("all items within iterator must be objects")

    for item in __iter:
        setattr(item, __name, __value)

    return __iter
