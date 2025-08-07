# -*- coding: utf-8 -*-
# src/apytizer/utils/errors.py

# Standard Library Imports
from typing import Any
from typing import Tuple
from typing import Union

# Local Imports
from .. import utils

__all__ = [
    "raise_for_attribute",
    "raise_for_instance",
    "raise_for_none",
]


def raise_for_attribute(__obj: object, __attr: str, /) -> None:
    """Raise error if object does not contain expected attribute.

    Args:
        __obj: Object to check for attribute.
        __attr: Attribute for which to check.

    """
    if not hasattr(__obj, __attr):
        cls = __obj.__class__.__name__
        message = f"type object '{cls!s}' has no attribute '{__attr!s}'"
        raise AttributeError(message)


def raise_for_instance(
    __value: object,
    __expected: Union[type, Tuple[Union[type, Tuple[Any, ...]], ...]],
    /,
) -> None:
    """Raise error if value is not an instance of expected type.

    Args:
        __value: Object to check for type.
        __expected: Expected type(s).

    """
    correct_type = isinstance(__value, __expected)

    if not correct_type and isinstance(__expected, tuple):
        _raise_for_multiple_types(__value, __expected)

    if not correct_type and not isinstance(__expected, tuple):
        _raise_for_single_type(__value, __expected)


def _raise_for_multiple_types(
    __value: object, __types: Tuple[Union[type, Tuple[Any, ...]], ...], /
) -> None:
    """Raise error if value is not among expected types.

    Args:
        __value: Object to check for type.
        __types: Expected types.

    """
    type_names = utils.iter_getattr(__types, "__name__")
    formatted_names = utils.iter_format(type_names, "'{}'")
    expected = utils.syntactic_list(formatted_names, "or")
    actual = type(__value).__name__

    message = f"expected types {expected!s}, got {actual!s} instead"
    raise TypeError(message)


def _raise_for_single_type(__value: object, __type: type, /) -> None:
    """Raise error if value is not an instance of expected type.

    Args:
        __value: Object to check for type.
        __type: Expected type.

    """
    expected, actual = f"'{__type.__name__}'", type(__value).__name__
    message = f"expected type {expected!s}, got {actual!s} instead"
    raise TypeError(message)


def raise_for_none(*args: Any, **kwargs: Any) -> None:
    """Raise error if value is None.

    Args:
        *args: Positional arguments.
        **kwargs: Keyword arguments.

    Raises:
        ValueError: when any argument is ``None``.

    """
    if any(arg is None for arg in args):
        message = "argument cannot be 'None'"
        raise ValueError(message)

    for name, value in kwargs.items():
        if value is None:
            message = f"{name} cannot be 'None'"
            raise ValueError(message)
