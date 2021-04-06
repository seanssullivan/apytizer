# -*- coding: utf-8 -*-

# Third-Party Imports
import pytest

# Local Imports
from src.abstracts.api import AbstractAPI
from src.base.endpoint import BasicEndpoint


class MockAPI(AbstractAPI):

    def __init__(self, url: str, **responses):
        self.url = url
        self.request = {}
        self.responses = responses

    def get(self, endpoint: str, headers: dict = None, **kwargs):
        self.request = {
            'method': 'GET',
            'url': endpoint,
            'headers': headers,
            'params': kwargs.get('params')
        }
        return self.responses['get']

    def post(self, endpoint: str, headers: dict = None, **kwargs):
        self.request = {
            'method': 'POST',
            'url': endpoint,
            'headers': headers,
            'params': kwargs.get('params'),
            'data': kwargs.get('data')
        }
        return self.responses['post']

    def put(self, endpoint: str, headers: dict = None, **kwargs):
        self.request = {
            'method': 'PUT',
            'url': endpoint,
            'headers': headers,
            'params': kwargs.get('params'),
            'data': kwargs.get('data')
        }
        return self.responses['put']

    def delete(self, endpoint: str, headers: dict = None, **kwargs):
        self.request = {
            'method': 'DELETE',
            'url': endpoint,
            'headers': headers,
            'params': kwargs.get('params')
        }
        return self.responses['delete']


def test_endpoint_add_method():
    mock_api = MockAPI('http://www.testing.com', post='created')
    test_endpoint = BasicEndpoint(mock_api, 'test', headers={'status': 'testing'})
    response = test_endpoint.add({'name': 'example'})

    assert response == 'created'
    assert test_endpoint.url == 'http://www.testing.com/test'
    assert mock_api.request['method'] == 'POST'
    assert mock_api.request['url'] == 'http://www.testing.com/test'
    assert mock_api.request['headers'] == {'status': 'testing'}
    assert mock_api.request['data'] == {'name': 'example'}


def test_endpoint_all_method():
    mock_api = MockAPI('http://www.testing.com', get=['success'])
    test_endpoint = BasicEndpoint(mock_api, 'test', headers={'status': 'testing'})
    response = test_endpoint.all()

    assert response == ['success']
    assert test_endpoint.url == 'http://www.testing.com/test'
    assert mock_api.request['method'] == 'GET'
    assert mock_api.request['url'] == 'http://www.testing.com/test'
    assert mock_api.request['headers'] == {'status': 'testing'}


def test_endpoint_get_method():
    mock_api = MockAPI('http://www.testing.com', get='success')
    test_endpoint = BasicEndpoint(mock_api, 'test', headers={'status': 'testing'})
    response = test_endpoint.get(1)

    assert response == 'success'
    assert test_endpoint.url == 'http://www.testing.com/test'
    assert mock_api.request['method'] == 'GET'
    assert mock_api.request['url'] == 'http://www.testing.com/test/1'
    assert mock_api.request['headers'] == {'status': 'testing'}


def test_endpoint_update_method():
    mock_api = MockAPI('http://www.testing.com', put='updated')
    test_endpoint = BasicEndpoint(mock_api, 'test', headers={'status': 'testing'})
    response = test_endpoint.update(1, data={'type': 'result'})

    assert response == 'updated'
    assert test_endpoint.url == 'http://www.testing.com/test'
    assert mock_api.request['method'] == 'PUT'
    assert mock_api.request['url'] == 'http://www.testing.com/test/1'
    assert mock_api.request['headers'] == {'status': 'testing'}
    assert mock_api.request['data'] == {'type': 'result'}


def test_endpoint_delete_method():
    mock_api = MockAPI('http://www.testing.com', delete='deleted')
    test_endpoint = BasicEndpoint(mock_api, 'test', headers={'status': 'testing'})
    response = test_endpoint.delete(1)

    assert response == 'deleted'
    assert test_endpoint.url == 'http://www.testing.com/test'
    assert mock_api.request['method'] == 'DELETE'
    assert mock_api.request['url'] == 'http://www.testing.com/test/1'
    assert mock_api.request['headers'] == {'status': 'testing'}
