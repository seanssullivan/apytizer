# -*- coding: utf-8 -*-
# src/apytizer/routes/base_route.py

# Standard Library Imports
from typing import List

# Local Imports
from .abstract_route import AbstractRoute

__all__ = ["Route"]


class Route(AbstractRoute):
    """Implements a route.

    Args:
        __value: Value.

    """

    def __init__(self, __value: str = "/", /) -> None:
        if not isinstance(__value, (AbstractRoute, str)):  # type: ignore
            message = f"expected type 'str', got {type(__value)} instead"
            raise TypeError(message)

        self._value = str(__value).strip("/") + "/"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, (AbstractRoute, str)):
            return False

        other_segments = get_segments(str(other))
        self_segments = get_segments(self._value)
        result = segments_are_equal(other_segments, self_segments)
        return result

    def __hash__(self) -> int:
        return hash(self._value.lower())

    def __len__(self) -> int:
        return len(get_segments(self._value))

    def __str__(self) -> str:
        return self._value

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, (AbstractRoute, str)):
            return False

        self_segments = get_segments(self._value)
        other_segments = get_segments(str(other))
        result = tuple(self_segments) > tuple(other_segments)
        return result

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, (AbstractRoute, str)):
            return False

        self_segments = get_segments(self._value)
        other_segments = get_segments(str(other))
        result = tuple(self_segments) < tuple(other_segments)
        return result

    def __add__(self, other: object) -> AbstractRoute:
        if not isinstance(other, str):
            message = f"expected type 'str', got {type(other)} instead"
            raise TypeError(message)

        result = Route(self._value + other.strip("/"))
        return result

    def __truediv__(self, other: object) -> AbstractRoute:
        if not isinstance(other, str):
            message = f"expected type 'str', got {type(other)} instead"
            raise TypeError(message)

        result = Route(self._value + other.strip("/"))
        return result


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
def count_segments(__value: str, /) -> int:
    """Get number of segments.

    Args:
        __value: Value for which to get number of segments.

    Returns:
        Number of segments.

    """
    result = len(get_segments(__value))
    return result


def get_segments(__value: str, /) -> List[str]:
    """Get segments of string seperated by slashes.

    Args:
        __value: Value for which to get segments.

    Returns:
        Segments.

    """
    if not isinstance(__value, str):  # type: ignore
        message = f"expected type 'str', got {type(__value)} instead"
        raise TypeError(message)

    result = __value.strip("/").split("/")
    return result


def segments_are_equal(
    first: List[str], second: List[str], placeholder: str = r"{}"
) -> bool:
    """Check whether segments are equal.

    Args:
        first: First list of segments.
        second: Second list of segments.
        placeholder: Placeholder. Default ``{}``.

    Returns:
        Whether segments are equal.

    """
    if len(first) != len(second):
        return False

    result = all(
        left.lower() == right.lower()
        for left, right in zip(first, second)
        if right != placeholder
    )
    return result
