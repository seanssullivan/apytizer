# -*- coding: utf-8 -*-

# Standard Library Imports
from unittest.mock import Mock

# Third-Party Imports
import pytest

# Local Imports
from src.base.endpoint import BasicEndpoint


@pytest.fixture
def mock_api():
    mock = Mock()
    mock.url = 'testing/'
    mock.headers = {'Content-Type': 'application/json'}
    mock.get = Mock()
    mock.post = Mock()
    mock.put = Mock()
    mock.delete = Mock()
    return mock


def test_endpoint_properties(mock_api):
    headers = {'status': 'testing'}
    test_endpoint = BasicEndpoint(mock_api, 'test', headers=headers)

    assert test_endpoint.url == 'testing/test'
    assert test_endpoint.headers == headers


def test_endpoint_get_method_when_response_is_ok(mock_api):
    # Configure the mock to return a response with an OK status code.
    mock_api.get.return_value.ok = True
    mock_api.get.return_value.json = {
        id: 1,
        'name': 'example',
        'status': 'testing'
    }

    test_endpoint = BasicEndpoint(mock_api, 'test', headers={'status': 'testing'})
    response = test_endpoint.get(1)

    assert response.json == {
        id: 1,
        'name': 'example',
        'status': 'testing'
    }
    mock_api.get.assert_called_once_with(
        'test/1',
        headers={'status': 'testing'}
    )


def test_endpoint_get_method_when_not_allowed(mock_api):
    # Configure the mock to return a response with an OK status code.
    mock_api.get.return_value.ok = True

    test_endpoint = BasicEndpoint(mock_api, 'test', headers={'status': 'testing'}, methods=['POST', 'PUT', 'DELETE'])

    with pytest.raises(NotImplementedError, match=''):
        test_endpoint.get(1)

    assert not mock_api.get.called


def test_endpoint_post_method_when_response_is_ok(mock_api):
    # Configure the mock to return a response with an OK status code.
    mock_api.post.return_value.ok = True
    mock_api.post.return_value.text = 'created'

    data = {
        'id': 1,
        'name': 'Test',
        'completed': False
    }

    test_endpoint = BasicEndpoint(mock_api, 'test', headers={'status': 'testing'})
    response = test_endpoint.post(data)

    assert response.text == 'created'
    mock_api.post.assert_called_once_with(
        'test',
        headers={'status': 'testing'},
        data=data
    )


def test_endpoint_post_method_when_not_allowed(mock_api):
    # Configure the mock to return a response with an OK status code.
    mock_api.post.return_value.ok = True

    test_endpoint = BasicEndpoint(mock_api, 'test', headers={'status': 'testing'}, methods=['GET', 'PUT', 'DELETE'])

    with pytest.raises(NotImplementedError, match=''):
        test_endpoint.post({})

    assert not mock_api.post.called


def test_endpoint_put_method_when_response_is_ok(mock_api):
    # Configure the mock to return a response with an OK status code.
    mock_api.put.return_value.ok = True
    mock_api.put.return_value.text = 'success'

    data = {
        'name': 'Test',
        'completed': False
    }

    test_endpoint = BasicEndpoint(mock_api, 'test', headers={'status': 'testing'})
    response = test_endpoint.put(1, data)

    assert response.text == 'success'
    mock_api.put.assert_called_once_with(
        'test/1',
        headers={'status': 'testing'},
        data=data
    )


def test_endpoint_put_method_when_not_allowed(mock_api):
    # Configure the mock to return a response with an OK status code.
    mock_api.put.return_value.ok = True

    test_endpoint = BasicEndpoint(mock_api, 'test', headers={'status': 'testing'}, methods=['GET', 'POST', 'DELETE'])

    with pytest.raises(NotImplementedError, match=''):
        test_endpoint.put(1, {})

    assert not mock_api.put.called


def test_endpoint_delete_method_when_response_is_ok(mock_api):
    # Configure the mock to return a response with an OK status code.
    mock_api.delete.return_value.ok = True
    mock_api.delete.return_value.text = 'success'

    test_endpoint = BasicEndpoint(mock_api, 'test', headers={'status': 'testing'})
    response = test_endpoint.delete(1)

    assert response.text == 'success'
    mock_api.delete.assert_called_once_with(
        'test/1',
        headers={'status': 'testing'}
    )


def test_endpoint_delete_method_when_delete_not_allowed(mock_api):
    # Configure the mock to return a response with an OK status code.
    mock_api.delete.return_value.ok = True

    test_endpoint = BasicEndpoint(mock_api, 'test', headers={'status': 'testing'}, methods=['GET', 'POST', 'PUT'])

    with pytest.raises(NotImplementedError, match=''):
        test_endpoint.delete(1)

    assert not mock_api.delete.called


def test_endpoint__getitem__returns_new_endpoint(mock_api):
    # Configure the mock to return a response with an OK status code.
    mock_api.get.return_value.ok = True

    initial_endpoint = BasicEndpoint(mock_api, 'test', headers={'status': 'testing'}, methods=['GET'])
    assert initial_endpoint.path == 'test'

    extended_endpoint = initial_endpoint[1]
    assert extended_endpoint.path == 'test/1'

    final_endpoint = extended_endpoint['stuff']
    assert final_endpoint.path == 'test/1/stuff'

    assert not mock_api.called


def test_endpoint__add__returns_new_endpoint(mock_api):
    # Configure the mock to return a response with an OK status code.
    mock_api.get.return_value.ok = True

    initial_endpoint = BasicEndpoint(mock_api, 'test', headers={'status': 'testing'}, methods=['GET'])
    assert initial_endpoint.path == 'test'

    extended_endpoint = initial_endpoint + 1
    assert extended_endpoint.path == 'test/1'

    final_endpoint = extended_endpoint + 'stuff'
    assert final_endpoint.path == 'test/1/stuff'

    assert not mock_api.called


def test_endpoint__truediv__returns_new_endpoint(mock_api):
    # Configure the mock to return a response with an OK status code.
    mock_api.get.return_value.ok = True

    initial_endpoint = BasicEndpoint(mock_api, 'test', headers={'status': 'testing'}, methods=['GET'])
    assert initial_endpoint.path == 'test'

    extended_endpoint = initial_endpoint / 1
    assert extended_endpoint.path == 'test/1'

    final_endpoint = extended_endpoint / 'stuff'
    assert final_endpoint.path == 'test/1/stuff'

    assert not mock_api.called
