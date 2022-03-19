# -*- coding: utf-8 -*-

# pylint: disable=protected-access

# Standard Library Imports
from unittest.mock import Mock, patch

# Third-Party Imports
import pytest


@pytest.fixture
def mock_request():
    mock_patcher = patch("src.apytizer.base.base_api.requests.request")
    yield mock_patcher.start()
    mock_patcher.stop()
