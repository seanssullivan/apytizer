# -*- coding: utf-8 -*-

# Standard Library Imports
from unittest.mock import Mock, patch

# Third-Party Imports
import pytest
import requests

# Local Imports
from src.base.api import BasicAPI
from src.base.api import SessionAPI


@pytest.fixture
def mock_request():
    mock_patcher = patch('src.base.api.requests.request')
    yield mock_patcher.start()
    mock_patcher.stop()


@pytest.fixture
def mock_session():
    session = Mock()
    session.start = Mock()
    session.close = Mock()
    session.request = Mock()
    return session


def test_api_head_request_when_response_is_ok(mock_request):
    mock_request.return_value.ok = True
    mock_request.return_value.headers = {
        'Content-Type': 'application/json'
    }

    api = BasicAPI(
        url='testing/',
        auth=('test_case', 'token'),
    )

    response = api.head("test")

    mock_request.assert_called_once_with(
        'HEAD',
        'testing/test',
        auth=('test_case', 'token'),
        headers=None
    )
    assert response.headers == {
        'Content-Type': 'application/json'
    }


def test_api_head_request_response_is_cached(mock_request):
    mock_request.return_value.ok = True

    mock_cache = {}

    api = BasicAPI(
        url='testing/',
        auth=('test_case', 'token'),
        cache=mock_cache
    )

    first_response = api.head("test")
    second_response = api.head("test")

    assert first_response == second_response
    assert mock_request.call_count == 1
    assert mock_cache == {
        ('HEAD', 'test'): mock_request.return_value
    }


def test_api_head_request_response_not_cached_when_cache_not_provided(mock_request):
    mock_request.return_value.ok = True

    api = BasicAPI(
        url='testing/',
        auth=('test_case', 'token')
    )

    first_response = api.head("test")
    second_response = api.head("test")

    assert first_response == second_response
    assert mock_request.call_count == 2


def test_api_get_request_when_response_is_ok(mock_request):
    mock_request.return_value.ok = True
    mock_request.return_value.json.return_value = {
        'name': 'example',
        'status': 'testing'
    }

    api = BasicAPI(
        url='testing/',
        auth=('test_case', 'token'),
        headers={'Accept': 'application/json'}
    )

    response = api.get("test")

    mock_request.assert_called_once_with(
        'GET',
        'testing/test',
        auth=('test_case', 'token'),
        headers={'Accept': 'application/json'}
    )
    assert response.json() == {
        'name': 'example',
        'status': 'testing'
    }


def test_api_get_request_response_is_cached(mock_request):
    mock_request.return_value.ok = True

    mock_cache = {}

    api = BasicAPI(
        url='testing/',
        auth=('test_case', 'token'),
        headers={'Accept': 'application/json'},
        cache=mock_cache
    )

    first_response = api.get("test")
    second_response = api.get("test")

    assert first_response == second_response
    assert mock_request.call_count == 1
    assert mock_cache == {
        ('GET', 'test'): mock_request.return_value
    }


def test_api_get_request_response_not_cached_when_cache_not_provided(mock_request):
    mock_request.return_value.ok = True

    api = BasicAPI(
        url='testing/',
        auth=('test_case', 'token'),
        headers={'Accept': 'application/json'}
    )

    first_response = api.get("test")
    second_response = api.get("test")

    assert first_response == second_response
    assert mock_request.call_count == 2


def test_api_post_request_when_response_is_ok(mock_request):
    mock_request.return_value.ok = True
    mock_request.return_value.status_code = 201

    api = BasicAPI(
        url='testing/',
        auth=('test_case', 'token'),
        headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
    )

    data = {
        'name': 'Test',
        'completed': True
    }

    response = api.post("test", data=data)

    mock_request.assert_called_once_with(
        'POST',
        'testing/test',
        auth=('test_case', 'token'),
        headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        data=data
    )
    assert response.status_code == 201


def test_api_post_request_response_is_cached(mock_request):
    mock_request.return_value.ok = True

    mock_cache = {}

    api = BasicAPI(
        url='testing/',
        auth=('test_case', 'token'),
        headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        cache=mock_cache
    )

    data = {
        'name': 'Test',
        'completed': True
    }

    first_response = api.post("test", data=data)
    second_response = api.post("test", data=data)

    assert first_response == second_response
    assert mock_request.call_count == 1
    assert mock_cache == {
        ('POST', 'test', "data={'name': 'Test', 'completed': True}"): mock_request.return_value
    }


def test_api_post_request_response_not_cached_when_cache_not_provided(mock_request):
    mock_request.return_value.ok = True

    api = BasicAPI(
        url='testing/',
        auth=('test_case', 'token'),
        headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    )

    data = {
        'name': 'Test',
        'completed': True
    }

    first_response = api.post("test", data=data)
    second_response = api.post("test", data=data)

    assert first_response == second_response
    assert mock_request.call_count == 2


def test_api_put_request_when_response_is_ok(mock_request):
    mock_request.return_value.ok = True
    mock_request.return_value.status_code = 204

    api = BasicAPI(
        url='testing/',
        auth=('test_case', 'token'),
        headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
    )

    data = {
        'name': 'Test',
        'completed': True
    }

    response = api.put("test", data=data)

    mock_request.assert_called_once_with(
        'PUT',
        'testing/test',
        auth=('test_case', 'token'),
        headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        data=data
    )
    assert response.status_code == 204


def test_api_put_request_response_is_cached(mock_request):
    mock_request.return_value.ok = True

    mock_cache = {}

    api = BasicAPI(
        url='testing/',
        auth=('test_case', 'token'),
        headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        cache=mock_cache
    )

    data = {
        'name': 'Test',
        'completed': True
    }

    first_response = api.put("test", data=data)
    second_response = api.put("test", data=data)

    assert first_response == second_response
    assert mock_request.call_count == 1
    assert mock_cache == {
        ('PUT', 'test', "data={'name': 'Test', 'completed': True}"): mock_request.return_value
    }


def test_api_put_request_response_not_cached_when_cache_not_provided(mock_request):
    mock_request.return_value.ok = True

    api = BasicAPI(
        url='testing/',
        auth=('test_case', 'token'),
        headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    )

    data = {
        'name': 'Test',
        'completed': True
    }

    first_response = api.put("test", data=data)
    second_response = api.put("test", data=data)

    assert first_response == second_response
    assert mock_request.call_count == 2


def test_api_patch_request_when_response_is_ok(mock_request):
    mock_request.return_value.ok = True
    mock_request.return_value.status_code = 204

    api = BasicAPI(
        url='testing/',
        auth=('test_case', 'token'),
        headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
    )

    data = {
        'name': 'Test',
        'completed': True
    }

    response = api.patch("test", data=data)

    mock_request.assert_called_once_with(
        'PATCH',
        'testing/test',
        auth=('test_case', 'token'),
        headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        data=data
    )
    assert response.status_code == 204


def test_api_patch_request_response_is_cached(mock_request):
    mock_request.return_value.ok = True

    mock_cache = {}

    api = BasicAPI(
        url='testing/',
        auth=('test_case', 'token'),
        headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        cache=mock_cache
    )

    data = {
        'name': 'Test',
        'completed': True
    }

    first_response = api.patch("test", data=data)
    second_response = api.patch("test", data=data)

    assert first_response == second_response
    assert mock_request.call_count == 1
    assert mock_cache == {
        ('PATCH', 'test', "data={'name': 'Test', 'completed': True}"): mock_request.return_value
    }


def test_api_patch_request_response_not_cached_when_cache_not_provided(mock_request):
    mock_request.return_value.ok = True

    api = BasicAPI(
        url='testing/',
        auth=('test_case', 'token'),
        headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    )

    data = {
        'name': 'Test',
        'completed': True
    }

    first_response = api.patch("test", data=data)
    second_response = api.patch("test", data=data)

    assert first_response == second_response
    assert mock_request.call_count == 2


def test_api_delete_request_when_response_is_ok(mock_request):
    mock_request.return_value.ok = True
    mock_request.return_value.status_code = 204

    api = BasicAPI(
        url='testing/',
        auth=('test_case', 'token'),

    )

    response = api.delete("test")

    mock_request.assert_called_once_with(
        'DELETE',
        'testing/test',
        auth=('test_case', 'token'),
        headers=None
    )
    assert response.status_code == 204


def test_api_delete_request_response_is_cached(mock_request):
    mock_request.return_value.ok = True

    mock_cache = {}

    api = BasicAPI(
        url='testing/',
        auth=('test_case', 'token'),
        cache=mock_cache
    )

    first_response = api.delete("test")
    second_response = api.delete("test")

    assert first_response == second_response
    assert mock_request.call_count == 1
    assert mock_cache == {
        ('DELETE', 'test'): mock_request.return_value
    }


def test_api_delete_request_response_not_cached_when_cache_not_provided(mock_request):
    mock_request.return_value.ok = True

    api = BasicAPI(
        url='testing/',
        auth=('test_case', 'token')
    )

    first_response = api.delete("test")
    second_response = api.delete("test")

    assert first_response == second_response
    assert mock_request.call_count == 2


def test_api_options_request_when_response_is_ok(mock_request):
    mock_request.return_value.ok = True
    mock_request.return_value.headers = {
        'Allow': ['OPTIONS', 'GET', 'POST', 'PUT', 'DELETE']
    }

    api = BasicAPI(
        url='testing/',
        auth=('test_case', 'token'),

    )

    response = api.options("test")

    mock_request.assert_called_once_with(
        'OPTIONS',
        'testing/test',
        auth=('test_case', 'token'),
        headers=None
    )
    assert response.headers == {
        'Allow': ['OPTIONS', 'GET', 'POST', 'PUT', 'DELETE']
    }


def test_api_options_request_response_is_cached(mock_request):
    mock_request.return_value.ok = True

    mock_cache = {}

    api = BasicAPI(
        url='testing/',
        auth=('test_case', 'token'),
        cache=mock_cache
    )

    first_response = api.options("test")
    second_response = api.options("test")

    assert first_response == second_response
    assert mock_request.call_count == 1
    assert mock_cache == {
        ('OPTIONS', 'test'): mock_request.return_value
    }


def test_api_options_request_response_not_cached_when_cache_not_provided(mock_request):
    mock_request.return_value.ok = True

    api = BasicAPI(
        url='testing/',
        auth=('test_case', 'token')
    )

    first_response = api.options("test")
    second_response = api.options("test")

    assert first_response == second_response
    assert mock_request.call_count == 2


def test_api_trace_request_when_response_is_ok(mock_request):
    mock_request.return_value.ok = True
    mock_request.return_value.headers = {
        'Content-Type': 'application/json'
    }

    api = BasicAPI(
        url='testing/',
        auth=('test_case', 'token'),
    )

    response = api.trace("test")

    mock_request.assert_called_once_with(
        'TRACE',
        'testing/test',
        auth=('test_case', 'token'),
        headers=None
    )
    assert response.headers == {
        'Content-Type': 'application/json'
    }


def test_api_trace_request_response_is_cached(mock_request):
    mock_request.return_value.ok = True

    mock_cache = {}

    api = BasicAPI(
        url='testing/',
        auth=('test_case', 'token'),
        cache=mock_cache
    )

    first_response = api.trace("test")
    second_response = api.trace("test")

    assert first_response == second_response
    assert mock_request.call_count == 1
    assert mock_cache == {
        ('TRACE', 'test'): mock_request.return_value
    }


def test_api_trace_request_response_not_cached_when_cache_not_provided(mock_request):
    mock_request.return_value.ok = True

    api = BasicAPI(
        url='testing/',
        auth=('test_case', 'token')
    )

    first_response = api.trace("test")
    second_response = api.trace("test")

    assert first_response == second_response
    assert mock_request.call_count == 2


def test_api_request_updates_headers(mock_request):
    mock_request.return_value.ok = True

    api = BasicAPI(
        url='testing/',
        headers={'Accept': 'application/json'}
    )

    api.request("GET", "test", headers={'Accept': 'text/html'})

    mock_request.assert_called_once_with(
        'GET',
        'testing/test',
        auth=None,
        headers={'Accept': 'text/html'}
    )


def test_session_request_updates_headers(mock_session):
    api = SessionAPI(
        url='testing/',
        headers={'Accept': 'application/json'},
        session=mock_session
    )

    data  = {
        'id': 1,
        'name': 'Test',
        'completed': True
    }

    with api:
        api.post("test", headers={'Content-Type': 'application/json'}, data=data)

    mock_session.request.assert_called_once_with(
        'POST',
        'testing/test',
        headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        data=data
    )


def test_session_start_method_creates_session():
    api = SessionAPI(url='testing/')
    assert not api.session

    api.start()

    assert isinstance(api.session, requests.Session)


def test_session_start_method_sets_authentication():
    api = SessionAPI(
        url='testing/',
        auth=('test_case', 'token'),
    )

    api.start()

    assert api.session.auth == ('test_case', 'token')


def test_session_start_method_updates_headers():
    api = SessionAPI(
        url='testing/',
        headers={'Accept': 'application/json'}
    )

    api.start()

    assert ('Accept', 'application/json') in api.session.headers.items()


def test_session_start_method_mounts_adapter():
    api = SessionAPI(
        url='testing/',
        adapter='Mock Adapter',
    )

    api.start()

    assert api.session.adapters['https://'] == 'Mock Adapter'
    assert api.session.adapters['http://'] == 'Mock Adapter'


def test_context_manager_closes_session(mock_session):
    api = SessionAPI(
        url='testing/',
        session=mock_session
    )

    with api:
        assert api.session.close.call_count == 0

    assert api.session.close.call_count == 1
