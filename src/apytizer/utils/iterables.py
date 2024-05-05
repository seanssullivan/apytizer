# -*- coding: utf-8 -*-
# src/apytizer/utils/iterables.py

# Standard Library Imports
from typing import Any
from typing import Iterable
from typing import List
from typing import SupportsIndex

# Local Imports
from .typing import allinstance

__all__ = ["deep_append", "deep_extend", "split_list"]


def deep_append(
    __obj: List[list], __index: SupportsIndex, __item: Any, /
) -> List[list]:
    """Appends value to a list within an iterable object.

    Args:
        __obj: Iterable object.
        __index: Index at which to append item.
        __item: Item to append to nested list.

    Returns:
        Updated iterable object.

    Raises:
        TypeError: when argument does not support indexing.

    """
    if not isinstance(__obj, list):
        message = f"expected type 'list', got {type(__obj)} instead"
        raise TypeError(message)

    if not allinstance(__obj, list):
        raise ValueError("must contain only lists")

    target = __obj[__index]  # type: list
    target.append(__item)
    return __obj


def deep_extend(
    __obj: List[list], __index: SupportsIndex, __items: list, /
) -> List[list]:
    """Extends list within nested iterable object with provided values.

    Args:
        __obj: Iterable object.
        __index: Index at which to extend list.
        __items: Items with which to extend nested list.

    Returns:
        Updated iterable object.

    Raises:
        TypeError: when argument does not support indexing.

    """
    if not isinstance(__obj, list):
        message = f"expected type 'list', got {type(__obj)} instead"
        raise TypeError(message)

    if not allinstance(__obj, list):
        raise ValueError("iterable object must contain only lists")

    target = __obj[__index]  # type: List[Any]
    target.extend(__items)
    return __obj


def split_list(__lst: List[Any], /, size: int) -> List[List[Any]]:
    """Split list into multiple groups of the same size.

    Args:
        __lst: List to split into groups.
        size: Maximum size of each group.

    Returns:
        Groups.

    .. _Based On:
        https://stackoverflow.com/questions/2231663/slicing-a-list-into-a-list-of-sub-lists

    """
    results = [__lst[i : i + size] for i in range(0, len(__lst), size)]
    return results
