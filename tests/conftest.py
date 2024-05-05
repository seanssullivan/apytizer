# -*- coding: utf-8 -*-

# Standard Library Imports
from unittest.mock import patch

# Third-Party Imports
import pytest


@pytest.fixture
def mock_request():
    import_path = "apytizer.connections.base_connection.requests.request"
    mock_patcher = patch(import_path)
    yield mock_patcher.start()
    mock_patcher.stop()
