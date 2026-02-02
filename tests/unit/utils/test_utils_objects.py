# -*- coding: utf-8 -*-

# Standard Library Imports
from unittest import mock

# Third-Party Imports
# import pytest

# Local Imports
try:
    from apytizer import utils

except ImportError:
    from src.apytizer import utils


def test_deep_getattr_returns_attribute_value() -> None:
    obj = mock.Mock()
    obj.first.second.third = "success"

    result = utils.deep_getattr(obj, "first.second.third")
    assert result == "success"


def test_deep_setattr_sets_attribute() -> None:
    obj = mock.Mock()

    utils.deep_setattr(obj, "first.second.third", "success")
    result = obj.first.second.third
    assert result == "success"


def test_iter_setattr_sets_values() -> None:
    objs = [mock.Mock(), mock.Mock(), mock.Mock()]
    results = utils.iter_setattr(objs, "test", "success")
    assert all(getattr(result, "test") == "success" for result in results)
