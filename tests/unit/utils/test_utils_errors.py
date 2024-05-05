# -*- coding: utf-8 -*-

# Third-Party Imports
import pytest

# Local Imports
try:
    from apytizer.utils import errors
except ImportError:
    from src.apytizer.utils import errors


def test_raises_error_when_not_expected_type() -> None:
    expected = "expected type 'str', got int instead"
    with pytest.raises(TypeError, match=expected):
        errors.raise_for_instance(1, str)


def test_raises_error_when_not_among_expected_types() -> None:
    expected = "expected types 'float', 'int' or 'str', got NoneType instead"
    with pytest.raises(TypeError, match=expected):
        errors.raise_for_instance(None, (float, int, str))


def test_raises_error_when_positional_argument_is_none() -> None:
    with pytest.raises(ValueError, match="cannot be 'None'"):
        errors.raise_for_none(None)
