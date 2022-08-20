# -*- coding: utf-8 -*-

# Standard Library Imports
from unittest import mock

# Third-Party Imports
# import pytest

# Local Imports
from apytizer import utils


def test_iter_setattr_sets_values() -> None:
    objs = [mock.Mock(), mock.Mock(), mock.Mock()]
    results = utils.iter_setattr(objs, "test", "success")
    assert all(getattr(result, "test") == "success" for result in results)
