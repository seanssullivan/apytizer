# -*- coding: utf-8 -*-
# src/apytizer/utils/errors.py

# Standard Library Imports
from typing import Collection, Type, Union

# Local Imports
from .. import utils


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
    __value: object, __expected: Union[Collection[Type], Type], /
) -> None:
    """Raise error if value is not an instance of expected type.

    Args:
        __value: Object to check for type.
        __expected: Expected type(s).

    """
    correct_type = isinstance(__value, __expected)
    multiple_types = isinstance(__expected, (list, tuple))

    if not correct_type and multiple_types:
        _raise_for_multiple_types(__value, __expected)

    if not correct_type and not multiple_types:
        _raise_for_single_type(__value, __expected)


def _raise_for_multiple_types(
    __value: object, __types: Collection[Type], /
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


def _raise_for_single_type(__value: object, __type: Type, /) -> None:
    """Raise error if value is not an instance of expected type.

    Args:
        __value: Object to check for type.
        __type: Expected type.

    """
    expected, actual = f"'{__type.__name__}'", type(__value).__name__
    message = f"expected type {expected!s}, got {actual!s} instead"
    raise TypeError(message)
