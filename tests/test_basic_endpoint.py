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
    mock.url = 'http://www.testing.com'
    mock.headers = {'Content-Type': 'application/json'}
    mock.get = Mock()
    mock.post = Mock()
    mock.put = Mock()
    mock.delete = Mock()
    return mock


def test_endpoint_properties(mock_api):
    headers = {'status': 'testing'}
    test_endpoint = BasicEndpoint(mock_api, 'test', headers=headers)

    assert test_endpoint.url == 'http://www.testing.com/test'
    assert test_endpoint.headers == headers


def test_endpoint_add_method_when_response_is_ok(mock_api):
    # Configure the mock to return a response with an OK status code.
    mock_api.post.return_value.ok = True
    mock_api.post.return_value.text = 'created'

    data = {
        'id': 1,
        'name': 'Test',
        'completed': False
    }

    test_endpoint = BasicEndpoint(mock_api, 'test', headers={'status': 'testing'})
    response = test_endpoint.add(data)

    assert response.text == 'created'
    mock_api.post.assert_called_once_with(
        'test',
        headers={'status': 'testing'},
        data=data
    )


def test_endpoint_add_method_when_post_not_allowed(mock_api):
    # Configure the mock to return a response with an OK status code.
    mock_api.post.return_value.ok = True

    test_endpoint = BasicEndpoint(mock_api, 'test', headers={'status': 'testing'}, methods=['GET', 'PUT', 'DELETE'])

    with pytest.raises(NotImplementedError, match=''):
        test_endpoint.add({})

    assert not mock_api.post.called


def test_endpoint_all_method_when_response_is_ok(mock_api):
    # Configure the mock to return a response with an OK status code.
    mock_api.get.return_value.ok = True
    mock_api.get.return_value.json = [{
        'name': 'example',
        'status': 'testing'
    }]

    test_endpoint = BasicEndpoint(mock_api, 'test', headers={'status': 'testing'})
    response = test_endpoint.all()

    assert response.json == [{
        'name': 'example',
        'status': 'testing'
    }]
    mock_api.get.assert_called_once_with(
        'test',
        headers={'status': 'testing'}
    )


def test_endpoint_all_method_when_get_not_allowed(mock_api):
    # Configure the mock to return a response with an OK status code.
    mock_api.get.return_value.ok = True

    test_endpoint = BasicEndpoint(mock_api, 'test', headers={'status': 'testing'}, methods=['POST', 'PUT', 'DELETE'])

    with pytest.raises(NotImplementedError, match=''):
        test_endpoint.all()

    assert not mock_api.get.called


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


def test_endpoint_get_method_when_get_not_allowed(mock_api):
    # Configure the mock to return a response with an OK status code.
    mock_api.get.return_value.ok = True

    test_endpoint = BasicEndpoint(mock_api, 'test', headers={'status': 'testing'}, methods=['POST', 'PUT', 'DELETE'])

    with pytest.raises(NotImplementedError, match=''):
        test_endpoint.get(1)

    assert not mock_api.get.called


def test_endpoint_update_method_when_response_is_ok(mock_api):
    # Configure the mock to return a response with an OK status code.
    mock_api.put.return_value.ok = True
    mock_api.put.return_value.text = 'success'

    data = {
        'name': 'Test',
        'completed': False
    }

    test_endpoint = BasicEndpoint(mock_api, 'test', headers={'status': 'testing'})
    response = test_endpoint.update(1, data)

    assert response.text == 'success'
    mock_api.put.assert_called_once_with(
        'test/1',
        headers={'status': 'testing'},
        data=data
    )


def test_endpoint_update_method_when_put_not_allowed(mock_api):
    # Configure the mock to return a response with an OK status code.
    mock_api.put.return_value.ok = True

    test_endpoint = BasicEndpoint(mock_api, 'test', headers={'status': 'testing'}, methods=['GET', 'POST', 'DELETE'])

    with pytest.raises(NotImplementedError, match=''):
        test_endpoint.update(1, {})

    assert not mock_api.put.called


def test_endpoint_remove_method_when_response_is_ok(mock_api):
    # Configure the mock to return a response with an OK status code.
    mock_api.delete.return_value.ok = True
    mock_api.delete.return_value.text = 'success'

    test_endpoint = BasicEndpoint(mock_api, 'test', headers={'status': 'testing'})
    response = test_endpoint.remove(1)

    assert response.text == 'success'
    mock_api.delete.assert_called_once_with(
        'test/1',
        headers={'status': 'testing'}
    )


def test_endpoint_remove_method_when_delete_not_allowed(mock_api):
    # Configure the mock to return a response with an OK status code.
    mock_api.delete.return_value.ok = True

    test_endpoint = BasicEndpoint(mock_api, 'test', headers={'status': 'testing'}, methods=['GET', 'POST', 'PUT'])

    with pytest.raises(NotImplementedError, match=''):
        test_endpoint.remove(1)

    assert not mock_api.delete.called
