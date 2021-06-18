# -*- coding: utf-8 -*-

# pylint: disable=protected-access

# Standard Library Imports
from unittest.mock import Mock, patch

# Third-Party Imports
import pytest


@pytest.fixture
def mock_request():
    mock_patcher = patch('src.apytizer.base.api.requests.request')
    yield mock_patcher.start()
    mock_patcher.stop()


@pytest.fixture
def mock_api():
    mock = Mock()
    mock.url = 'testing/'
    mock.get = Mock()
    mock.post = Mock()
    mock.put = Mock()
    mock.delete = Mock()
    return mock


@pytest.fixture
def mock_session():
    session = Mock()
    session.start = Mock()
    session.close = Mock()
    session.request = Mock()
    return session
