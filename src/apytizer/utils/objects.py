# -*- coding: utf-8 -*-
# src/apytizer/utils/objects.py

# Standard Library Imports
import collections
import functools
from typing import Any
from typing import Iterable
from typing import List
from typing import Optional

# Local Imports
from .typing import allinstance

__all__ = [
    "deep_getattr",
    "deep_setattr",
    "getattrs",
    "setattrs",
    "iter_getattr",
    "iter_setattr",
]


def deep_getattr(__o: object, __name: Iterable[str], /) -> Any:
    """Get value of attribute in nested object.

    Args:
        __o: Object on which to get attribute.
        __name: Name of attribute from which to get value.

    Returns:
        Value of attribute in nested object.

    """
    if not isinstance(__name, Iterable):  # type: ignore
        message = f"'{type(__name)}' object is not iterable"
        raise TypeError(message)

    attrs = __name.split(".") if isinstance(__name, str) else __name
    result = functools.reduce(lambda acc, cur: getattr(acc, cur), attrs, __o)
    return result


def deep_setattr(__o: object, __name: str, __value: Any, /) -> None:
    """Sets attribute to value in nested object.

    Args:
        __o: Object on which to set attributes.
        __name: Name of attribute to set on object.
        __value: Value to set attribute on object.

    Returns:
        Updated object.

    """
    attrs = collections.deque(__name.split("."))
    target = attrs.pop()

    obj = functools.reduce(lambda acc, cur: getattr(acc, cur), attrs, __o)
    setattr(obj, target, __value)


def getattrs(
    __o: object, __names: List[str], __default: Optional[Any] = None, /
) -> List[Any]:
    """Get named attributes from an object.

    Args:
        __o: Object from which to get attributes.
        __names: Names of attributes to get from object.
        __default (optional): Default value when attribute doesn't exist.
            Default ``None``.

    Returns:
        Attributes.

    """
    results = [getattr(__o, __name, __default) for __name in __names]
    return results


def setattrs(__o: object, __names: List[str], __values: List[Any], /) -> None:
    """Set named attributes on an object.

    Args:
        __o: Object on which to set attributes.
        __names: Names of attributes to set on object.
        __values: Values to set for keys on object.

    Returns:
        Updated object.

    """
    for __name, __value in zip(__names, __values):
        setattr(__o, __name, __value)


def iter_getattr(__iter: Iterable[object], __name: str, /) -> List[Any]:
    """Get a named attribute from each object.

    Args:
        __iter: Iterable object containing objects.
        __name: Attribute for which to retrieve value.

    Raises:
        TypeError: when argument is not an iterable object.
        ValueError: when not all items are mappings.

    """
    if not isinstance(__iter, Iterable):  # type: ignore
        raise TypeError("must be an iterable object")

    if not allinstance(__iter, object):
        raise ValueError("all items within iterator must be objects")

    results = [getattr(item, __name) for item in __iter]
    return results


def iter_setattr(
    __iter: Iterable[Any], __name: str, __value: Any, /
) -> Iterable[Any]:
    """Sets the named attribute to the specified value on each object.

    Args:
        __iter: Iterable object containing objects.
        __name: Attribute to set to value.
        value: Value to which to set attribute.

    Raises:
        TypeError: when argument is not an iterable object.
        ValueError: when not all items are objects.

    """
    if not isinstance(__iter, Iterable):  # type: ignore
        raise TypeError("must be an iterable object")

    if not allinstance(__iter, object):
        raise ValueError("all items within iterator must be objects")

    for item in __iter:
        setattr(item, __name, __value)

    return __iter
