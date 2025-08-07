# -*- coding: utf-8 -*-

# Standard Library Imports
from typing import Any
from typing import Iterable
from typing import Tuple
from typing import Type
from typing import Union

__all__ = ["allinstance"]


def allinstance(
    __objs: Iterable[Any],
    __class_or_tuple: Union[Tuple[Type[Any], ...], type],
    /,
) -> bool:
    """Whether all elements in an iterable object are instances of provided type(s).

    Args:
        __objs: Iterable object containing elements.
        __class_or_tuple: Class or tuple of classes.

    Returns:
        Whether all elements are instances of the provided type(s).

    """
    result = all(isinstance(elem, __class_or_tuple) for elem in __objs)
    return result
