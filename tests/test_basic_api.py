# -*- coding: utf-8 -*-

# Standard Library Imports
import time
from unittest.mock import Mock, patch

# Third-Party Imports
import pytest

# Local Imports
from src.base.api import BasicAPI


@pytest.fixture
def mock_request():
    mock_patcher = patch('src.base.api.requests.request')
    yield mock_patcher.start()
    mock_patcher.stop()

def test_api_get_request_when_response_is_ok(mock_request):
    # Configure the mock to return a response with an OK status code.
    mock_request.return_value.ok = True
    mock_request.return_value = Mock()
    mock_request.return_value.json.return_value = {
        'name': 'example',
        'status': 'testing'
    }

    # Initialize the API.
    api = BasicAPI(
        url='testing/',
        auth=('test_case', 'token'),
        headers={'Content-Type': 'application/json'}
    )

    response = api.get("test")

    mock_request.assert_called_once_with(
        'GET',
        'testing/test',
        auth=('test_case', 'token'),
        headers={'Content-Type': 'application/json'}
    )
    assert response.json() == {
        'name': 'example',
        'status': 'testing'
    }


def test_api_get_request_rate_limit(mock_request):
    # Configure the mock to return a response with an OK status code.
    mock_request.return_value.ok = True
    mock_request.return_value = Mock()

    # Initialize the API.
    api = BasicAPI(
        url='testing/',
        auth=('test_case', 'token'),
        headers={'Content-Type': 'application/json'},
        rate_limit=0.1
    )

    time_start = time.time()
    api.get("test_one")
    api.get("test_two")
    time_end = time.time()

    assert time_end - time_start >= 0.1


def test_api_post_request_when_response_is_ok(mock_request):
    # Configure the mock to return a response with an OK status code.
    mock_request.return_value.ok = True
    mock_request.return_value = Mock()
    mock_request.return_value.status_code = 201

    # Initialize the API.
    api = BasicAPI(
        url='testing/',
        auth=('test_case', 'token'),
        headers={'Content-Type': 'application/json'},
    )

    data = {
        'id': 1,
        'name': 'Test',
        'completed': False
    }

    response = api.post("test", data=data)
    mock_request.assert_called_once_with(
        'POST',
        'testing/test',
        auth=('test_case', 'token'),
        headers={'Content-Type': 'application/json'},
        data=data
    )
    assert response.status_code == 201


def test_api_post_request_rate_limit(mock_request):
    # Configure the mock to return a response with an OK status code.
    mock_request.return_value.ok = True
    mock_request.return_value = Mock()

    # Initialize the API.
    api = BasicAPI(
        url='testing/',
        auth=('test_case', 'token'),
        headers={'Content-Type': 'application/json'},
        rate_limit=0.1
    )

    time_start = time.time()
    api.post("test_one")
    api.post("test_two")
    time_end = time.time()

    assert  time_end - time_start >= 0.1


def test_api_put_request_when_response_is_ok(mock_request):
    # Configure the mock to return a response with an OK status code.
    mock_request.return_value.ok = True
    mock_request.return_value = Mock()
    mock_request.return_value.status_code = 200

    # Initialize the API.
    api = BasicAPI(
        url='testing/',
        auth=('test_case', 'token'),
        headers={'Content-Type': 'application/json'},
    )

    data = {
        'name': 'Test',
        'completed': False
    }

    response = api.put("test/1", data=data)
    mock_request.assert_called_once_with(
        'PUT',
        'testing/test/1',
        auth=('test_case', 'token'),
        headers={'Content-Type': 'application/json'},
        data=data
    )
    assert response.status_code == 200


def test_api_put_request_rate_limit(mock_request):
    # Configure the mock to return a response with an OK status code.
    mock_request.return_value.ok = True
    mock_request.return_value = Mock()

    # Initialize the API.
    api = BasicAPI(
        url='testing/',
        auth=('test_case', 'token'),
        headers={'Content-Type': 'application/json'},
        rate_limit=0.1
    )

    time_start = time.time()
    api.put("test_one")
    api.put("test_two")
    time_end = time.time()

    assert  time_end - time_start >= 0.1


def test_api_delete_request_when_response_is_ok(mock_request):
    # Configure the mock to return a response with an OK status code.
    mock_request.return_value.ok = True
    mock_request.return_value = Mock()
    mock_request.return_value.status_code = 200

    # Initialize the API.
    api = BasicAPI(
        url='testing/',
        auth=('test_case', 'token'),
        headers={'Content-Type': 'application/json'},
    )

    response = api.delete("test/1")
    mock_request.assert_called_once_with(
        'DELETE',
        'testing/test/1',
        auth=('test_case', 'token'),
        headers={'Content-Type': 'application/json'}
    )
    assert response.status_code == 200


def test_api_delete_request_rate_limit(mock_request):
    # Configure the mock to return a response with an OK status code.
    mock_request.return_value.ok = True
    mock_request.return_value = Mock()

    # Initialize the API.
    api = BasicAPI(
        url='testing/',
        auth=('test_case', 'token'),
        headers={'Content-Type': 'application/json'},
        rate_limit=0.1
    )

    time_start = time.time()
    api.delete("test_one")
    api.delete("test_two")
    time_end = time.time()

    assert  time_end - time_start >= 0.1
