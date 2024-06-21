# -*- coding: utf-8 -*-

# Standard Library Imports
from typing import Generator
from unittest.mock import Mock
from unittest.mock import patch

# Third-Party Imports
import pytest


@pytest.fixture
def mock_request() -> Generator[Mock, None, None]:
    import_path = "requests.request"
    mock_patcher = patch(import_path)
    yield mock_patcher.start()
    mock_patcher.stop()
