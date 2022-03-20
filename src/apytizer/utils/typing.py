# -*- coding: utf-8 -*-

# Standard Library Imports
from typing import Iterable, Tuple, Union

__all__ = ["allinstance"]


def allinstance(
    __objs: Iterable, __class_or_tuple: Union[Tuple[type], type]
) -> bool:
    """Whether all elements of an iterable are instances of provided type(s).

    Args:
        __objs: Iterable object containing elements.
        __class_or_tuple: Class or tuple of classes.

    Returns:
        Whether all elements are instances of the provided type(s).

    """
    result = all(isinstance(elem, __class_or_tuple) for elem in __objs)
    return result
