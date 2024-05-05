# -*- coding: utf-8 -*-

# Standard Library Imports
from unittest.mock import Mock

# Third-Party Imports
import pytest

# Local Imports
from .. import mocks


@pytest.fixture
def mock_engine() -> Mock:
    """Fixture mocks `BaseAPI` interface.

    Returns:
        Mock API.

    """
    result = mocks.MockEngine("testing/")
    return result
