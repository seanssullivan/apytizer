# -*- coding: utf-8 -*-
# src/apytizer/utils/iterables.py

# Standard Library Imports
import functools
import math
from typing import Any, Iterable, List

# Local Imports
from .typing import allinstance

__all__ = ["deep_append", "deep_extend", "split_list"]


def deep_append(
    __obj: Iterable[list], /, index: int, value: Any
) -> List[List[Any]]:
    """Appends value to list within nested iterable object.

    Args:
        __obj: Iterable object.
        index: Index at which to nested list.
        value: Value to append to nested list.

    Returns:
        Updated iterable object.

    Raises:
        TypeError: when argument does not support indexing.

    """
    if not isinstance(__obj, Iterable):
        message = f"'{type(__obj)}' object is not iterable"
        raise TypeError(message)

    if not allinstance(__obj, list):
        raise ValueError("iterable object must only contain lists")

    __lst = __obj[index]  # type: list
    __lst.append(value)
    return __obj


def deep_extend(
    __obj: Iterable[list], /, index: int, values: List[Any]
) -> List[List[Any]]:
    """Extends list within nested iterable object with provided values.

    Args:
        __obj: Iterable object.
        index: Index at which to nested list.
        values: Values with which to extend nested list.

    Returns:
        Updated iterable object.

    Raises:
        TypeError: when argument does not support indexing.

    """
    if not isinstance(__obj, Iterable):
        message = f"'{type(__obj)}' object is not iterable"
        raise TypeError(message)

    if not allinstance(__obj, list):
        raise ValueError("iterable object must only contain lists")

    __lst = __obj[index]  # type: list
    __lst.extend(values)
    return __obj


def split_list(__lst: List[Any], /, size: int) -> List[List[Any]]:
    """Split list into multiple groups of the same size.

    Args:
        __lst: List to split.
        size: Maximum size of each group.

    Returns:
        Groups.

    """
    num_groups = math.ceil(len(__lst) / size)
    results = functools.reduce(
        lambda acc, val: deep_append(acc, -1, val)
        if len(acc[-1]) < size
        else deep_append([*acc, []], -1, val),
        __lst,
        [[]],
    )
    assert len(results) == num_groups
    return results
