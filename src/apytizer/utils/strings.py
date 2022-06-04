# -*- coding: utf-8 -*-
# src/apytizer/utils/strings.py

# Standard Library Imports
import re
from typing import Any, Collection, Iterable, List

__all__ = ["camel_to_snake", "iter_format", "syntactic_list"]


# Patterns
CAMEL_TO_SNAKE = re.compile(r"(?<=[a-z0-9])(?=[A-Z][a-z]+)")


def camel_to_snake(__s: str, /) -> str:
    """Convert camelcase string to snakecase.

    Args:
        __s: Camelcase string to convert.

    Returns:
        Snakecase string.

    .. _Based On:
        https://stackoverflow.com/a/1176023.

    """
    result = CAMEL_TO_SNAKE.sub("_", __s).lower()
    return result


def iter_format(__iter: Iterable[Any], __format: str, /) -> List[str]:
    """Format each item in an iterable object.

    Args:
        __iter: Iterable object containing items to format.
        __format: String format to apply to each item.

    Returns:
        Formatted items.

    """
    result = [__format.format(item) for item in __iter]
    return result


def syntactic_list(
    __l: Collection[str], /, conjunction: str, *, oxford: bool = False
) -> str:
    """Apply syntax to a list of strings.

    Args:
        __l: List of strings.
        conjunction: Conjunction with which to join list.
        oxford (optional): Whether to use an oxford comma. Default `False`.

    Returns:
        Syntactically-correct list.

    """
    if len(__l) < 2:
        raise ValueError("list must contain at least two items")

    separator = f"{',' if oxford else ''} {conjunction!s} "
    result = separator.join([", ".join(__l[:-1]), __l[-1]])
    return result
