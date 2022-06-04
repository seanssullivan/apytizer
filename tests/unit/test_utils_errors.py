# -*- coding: utf-8 -*-

# Third-Party Imports
import pytest

# Local Imports
from apytizer.utils import errors


def test_raises_error_when_not_expected_type():
    expected = "expected type 'str', got int instead"
    with pytest.raises(TypeError, match=expected):
        errors.raise_for_instance(1, str)


def test_raises_error_when_not_among_expected_types():
    expected = "expected types 'float', 'int' or 'str', got NoneType instead"
    with pytest.raises(TypeError, match=expected):
        errors.raise_for_instance(None, (float, int, str))
