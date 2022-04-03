# -*- coding: utf-8 -*-

# Standard Library Imports
from unittest.mock import patch

# Third-Party Imports
import pytest


@pytest.fixture
def mock_request():
    mock_patcher = patch("src.apytizer.apis.base_api.requests.request")
    yield mock_patcher.start()
    mock_patcher.stop()
