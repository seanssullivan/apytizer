# -*- coding: utf-8 -*-

# Third-Party Imports
import pytest

# Local Imports
from ... import mocks


@pytest.fixture
def mock_api(mock_engine: mocks.MockEngine) -> mocks.MockAPI:
    """Fixture mocks `BaseAPI` interface.

    Returns:
        Mock API.

    """
    result = mocks.MockAPI(mock_engine)
    return result
