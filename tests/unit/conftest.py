# -*- coding: utf-8 -*-

# Third-Party Imports
import pytest

# Local Imports
from .. import mocks


@pytest.fixture
def mock_engine() -> mocks.MockEngine:
    """Fixture mocks `BaseAPI` interface.

    Returns:
        Mock API.

    """
    result = mocks.MockEngine("testing/")
    return result
