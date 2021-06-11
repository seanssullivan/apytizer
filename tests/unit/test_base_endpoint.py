# -*- coding: utf-8 -*-

# pylint: disable=protected-access

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
    mock.head = Mock()
    mock.get = Mock()
    mock.post = Mock()
    mock.put = Mock()
    mock.patch = Mock()
    mock.delete = Mock()
    mock.options = Mock()
    mock.trace = Mock()
    return mock


# --------------------------------------------------------------------------------
# Tests for Endpoint
# --------------------------------------------------------------------------------

def test_endpoint_uri_contains_base_and_path(mock_api):
    test_endpoint = BasicEndpoint(mock_api, 'test')
    assert test_endpoint.uri == 'testing/test'


# --------------------------------------------------------------------------------
# Tests for HEAD Method
# --------------------------------------------------------------------------------

def test_endpoint_head_method_when_response_is_ok(mock_api):
    mock_api.head.return_value.ok = True
    mock_api.head.return_value.headers = {
        'Content-Type': 'application/json'
    }

    test_endpoint = BasicEndpoint(
        mock_api,
        'test',
        headers={'Accept': 'application/json'}
    )

    response = test_endpoint.head()

    assert response.headers == {
        'Content-Type': 'application/json'
    }
    mock_api.head.assert_called_once_with(
        'test',
        headers={'Accept': 'application/json'},
        params=None,
    )


def test_endpoint_head_method_when_not_allowed(mock_api):
    test_endpoint = BasicEndpoint(
        mock_api,
        'test',
        headers={'Accept': 'application/json'},
        methods=['GET', 'POST', 'PUT', 'DELETE']
    )

    with pytest.raises(NotImplementedError, match=''):
        test_endpoint.head()

    assert not mock_api.head.called


def test_endpoint_head_response_is_cached(mock_api):
    mock_api.head.return_value.ok = True

    mock_cache = {}

    test_endpoint = BasicEndpoint(
        mock_api,
        'test',
        headers={'Accept': 'application/json'},
        cache=mock_cache
    )

    first_response = test_endpoint.head()
    second_response = test_endpoint.head()

    assert first_response == second_response
    assert mock_api.head.call_count == 1
    assert mock_cache == {
        ('HEAD',): mock_api.head.return_value
    }


def test_endpoint_head_response_not_cached_when_cache_not_provided(mock_api):
    mock_api.head.return_value.ok = True

    test_endpoint = BasicEndpoint(
        mock_api,
        'test',
        headers={'Accept': 'application/json'}
    )

    first_response = test_endpoint.head()
    second_response = test_endpoint.head()

    assert first_response == second_response
    assert mock_api.head.call_count == 2


# --------------------------------------------------------------------------------
# Tests for GET Method
# --------------------------------------------------------------------------------

def test_endpoint_get_method_when_response_is_ok(mock_api):
    mock_api.get.return_value.ok = True
    mock_api.get.return_value.json.return_value = {
        'name': 'example',
        'status': 'testing'
    }

    test_endpoint = BasicEndpoint(
        mock_api,
        'test',
        headers={'Accept': 'application/json'}
    )

    response = test_endpoint.get()

    assert response.json() == {
        'name': 'example',
        'status': 'testing'
    }
    mock_api.get.assert_called_once_with(
        'test',
        headers={'Accept': 'application/json'},
        params=None,
    )


def test_endpoint_get_method_when_not_allowed(mock_api):
    test_endpoint = BasicEndpoint(
        mock_api,
        'test',
        headers={'Accept': 'application/json'},
        methods=['POST', 'PUT', 'DELETE']
    )

    with pytest.raises(NotImplementedError, match=''):
        test_endpoint.get()

    assert not mock_api.get.called


def test_endpoint_get_response_is_cached(mock_api):
    mock_api.get.return_value.ok = True

    mock_cache = {}

    test_endpoint = BasicEndpoint(
        mock_api,
        'test',
        headers={'Accept': 'application/json'},
        cache=mock_cache
    )

    first_response = test_endpoint.get()
    second_response = test_endpoint.get()

    assert first_response == second_response
    assert mock_api.get.call_count == 1
    assert mock_cache == {
        ('GET',): mock_api.get.return_value
    }


def test_endpoint_get_response_not_cached_when_cache_not_provided(mock_api):
    mock_api.get.return_value.ok = True

    test_endpoint = BasicEndpoint(
        mock_api,
        'test',
        headers={'Accept': 'application/json'}
    )

    first_response = test_endpoint.get()
    second_response = test_endpoint.get()

    assert first_response == second_response
    assert mock_api.get.call_count == 2


# --------------------------------------------------------------------------------
# Tests for POST Method
# --------------------------------------------------------------------------------

def test_endpoint_post_method_when_response_is_ok(mock_api):
    mock_api.post.return_value.ok = True
    mock_api.post.return_value.text = 'created'

    data = {
        'id': 1,
        'name': 'Test',
        'completed': False
    }

    test_endpoint = BasicEndpoint(
        mock_api,
        'test',
        headers={'Accept': 'application/json'}
    )

    response = test_endpoint.post(data)

    assert response.text == 'created'
    mock_api.post.assert_called_once_with(
        'test',
        data=data,
        headers={'Accept': 'application/json'},
        params=None,
    )


def test_endpoint_post_method_when_not_allowed(mock_api):
    test_endpoint = BasicEndpoint(
        mock_api,
        'test',
        headers={'Accept': 'application/json'},
        methods=['GET', 'PUT', 'DELETE']
    )

    with pytest.raises(NotImplementedError, match=''):
        test_endpoint.post({})

    assert not mock_api.post.called


# --------------------------------------------------------------------------------
# Tests for PUT Method
# --------------------------------------------------------------------------------

def test_endpoint_put_method_when_response_is_ok(mock_api):
    mock_api.put.return_value.ok = True
    mock_api.put.return_value.text = 'success'

    data = {
        'name': 'Test',
        'completed': False
    }

    test_endpoint = BasicEndpoint(
        mock_api,
        'test',
        headers={'Accept': 'application/json'}
    )

    response = test_endpoint.put(data)

    assert response.text == 'success'
    mock_api.put.assert_called_once_with(
        'test',
        data=data,
        headers={'Accept': 'application/json'},
        params=None,
    )


def test_endpoint_put_method_when_not_allowed(mock_api):
    test_endpoint = BasicEndpoint(
        mock_api,
        'test',
        headers={'Accept': 'application/json'},
        methods=['GET', 'POST', 'DELETE']
    )

    with pytest.raises(NotImplementedError, match=''):
        test_endpoint.put({})

    assert not mock_api.put.called


# --------------------------------------------------------------------------------
# Tests for PATCH Method
# --------------------------------------------------------------------------------

def test_endpoint_patch_method_when_response_is_ok(mock_api):
    mock_api.patch.return_value.ok = True
    mock_api.patch.return_value.text = 'success'

    data = {
        'name': 'Test',
        'completed': False
    }

    test_endpoint = BasicEndpoint(
        mock_api,
        'test',
        headers={'Accept': 'application/json'}
    )

    response = test_endpoint.patch(data)

    assert response.text == 'success'
    mock_api.patch.assert_called_once_with(
        'test',
        data=data,
        headers={'Accept': 'application/json'},
        params=None,
    )


def test_endpoint_patch_method_when_not_allowed(mock_api):
    test_endpoint = BasicEndpoint(
        mock_api,
        'test',
        headers={'Accept': 'application/json'},
        methods=['GET', 'POST', 'DELETE']
    )

    with pytest.raises(NotImplementedError, match=''):
        test_endpoint.patch({})

    assert not mock_api.patch.called


# --------------------------------------------------------------------------------
# Tests for DELETE Method
# --------------------------------------------------------------------------------

def test_endpoint_delete_method_when_response_is_ok(mock_api):
    mock_api.delete.return_value.ok = True
    mock_api.delete.return_value.text = 'success'

    test_endpoint = BasicEndpoint(
        mock_api,
        'test',
        headers={'Accept': 'application/json'}
    )

    response = test_endpoint.delete()

    assert response.text == 'success'
    mock_api.delete.assert_called_once_with(
        'test',
        headers={'Accept': 'application/json'},
        params=None,
    )


def test_endpoint_delete_method_when_not_allowed(mock_api):
    test_endpoint = BasicEndpoint(
        mock_api,
        'test',
        headers={'Accept': 'application/json'},
        methods=['GET', 'POST', 'PUT']
    )

    with pytest.raises(NotImplementedError, match=''):
        test_endpoint.delete()

    assert not mock_api.delete.called


# --------------------------------------------------------------------------------
# Tests for OPTIONS Method
# --------------------------------------------------------------------------------

def test_endpoint_options_method_when_response_is_ok(mock_api):
    mock_api.options.return_value.ok = True
    mock_api.options.return_value.headers = {
        'Allow': ['OPTIONS', 'GET', 'POST', 'PUT', 'DELETE']
    }

    test_endpoint = BasicEndpoint(
        mock_api,
        'test',
        headers={'Accept': 'application/json'}
    )

    response = test_endpoint.options()

    assert response.headers == {
        'Allow': ['OPTIONS', 'GET', 'POST', 'PUT', 'DELETE']
    }
    mock_api.options.assert_called_once_with(
        'test',
        headers={'Accept': 'application/json'},
        params=None,
    )


def test_endpoint_options_method_when_not_allowed(mock_api):
    test_endpoint = BasicEndpoint(
        mock_api,
        'test',
        headers={'Accept': 'application/json'},
        methods=['GET', 'POST', 'PUT', 'DELETE']
    )

    with pytest.raises(NotImplementedError, match=''):
        test_endpoint.options()

    assert not mock_api.options.called



# --------------------------------------------------------------------------------
# Tests for TRACE Method
# --------------------------------------------------------------------------------

def test_endpoint_trace_method_when_response_is_ok(mock_api):
    mock_api.trace.return_value.ok = True
    mock_api.trace.return_value.headers = {
        'Content-Type': 'application/json'
    }

    test_endpoint = BasicEndpoint(
        mock_api,
        'test',
        headers={'Accept': 'application/json'}
    )

    response = test_endpoint.trace()

    assert response.headers == {
        'Content-Type': 'application/json'
    }
    mock_api.trace.assert_called_once_with(
        'test',
        headers={'Accept': 'application/json'},
        params=None,
    )


def test_endpoint_trace_method_when_not_allowed(mock_api):
    test_endpoint = BasicEndpoint(
        mock_api,
        'test',
        headers={'Accept': 'application/json'},
        methods=['GET', 'POST', 'PUT', 'DELETE']
    )

    with pytest.raises(NotImplementedError, match=''):
        test_endpoint.trace()

    assert not mock_api.trace.called


# --------------------------------------------------------------------------------
# Tests for Magic Methods
# --------------------------------------------------------------------------------

def test_endpoint__call__returns_new_endpoint(mock_api):
    initial_endpoint = BasicEndpoint(
        mock_api,
        'test',
        headers={'Accept': 'application/json'},
        methods=['GET']
    )
    assert initial_endpoint.path == 'test'

    extended_endpoint = initial_endpoint(1)
    assert isinstance(extended_endpoint, BasicEndpoint)
    assert extended_endpoint.path == 'test/1'

    final_endpoint = extended_endpoint('stuff')
    assert isinstance(final_endpoint, BasicEndpoint)
    assert final_endpoint.path == 'test/1/stuff'

    assert not mock_api.called


def test_endpoint__call_raises_type_error_when_passed_invalid_argument(mock_api):
    endpoint = BasicEndpoint(
        mock_api,
        'test',
        headers={'Accept': 'application/json'},
        methods=[]
    )

    with pytest.raises(TypeError):
        endpoint(['stuff'])

    with pytest.raises(TypeError):
        endpoint(('stuff', 'things'))

    with pytest.raises(TypeError):
        endpoint({'stuff': 'junk'})


def test_endpoint__getitem__returns_new_endpoint(mock_api):
    initial_endpoint = BasicEndpoint(
        mock_api,
        'test',
        headers={'Accept': 'application/json'},
        methods=['GET']
    )
    assert initial_endpoint.path == 'test'

    extended_endpoint = initial_endpoint[1]
    assert extended_endpoint.path == 'test/1'

    final_endpoint = extended_endpoint['stuff']
    assert final_endpoint.path == 'test/1/stuff'

    assert not mock_api.called


def test_endpoint__getitem__raises_type_error_when_passed_invalid_argument(mock_api):
    endpoint = BasicEndpoint(
        mock_api,
        'test',
        headers={'Accept': 'application/json'},
        methods=[]
    )

    with pytest.raises(TypeError):
        endpoint[['stuff']]

    with pytest.raises(TypeError):
        endpoint[('stuff', 'things')]

    with pytest.raises(TypeError):
        endpoint[{'stuff': 'junk'}]


def test_endpoint__add__returns_new_endpoint(mock_api):
    initial_endpoint = BasicEndpoint(
        mock_api,
        'test',
        headers={'Accept': 'application/json'},
        methods=['GET']
    )
    assert initial_endpoint.path == 'test'

    extended_endpoint = initial_endpoint + 1
    assert extended_endpoint.path == 'test/1'

    final_endpoint = extended_endpoint + 'stuff'
    assert final_endpoint.path == 'test/1/stuff'

    assert not mock_api.called


def test_endpoint__add__raises_type_error_when_passed_invalid_argument(mock_api):
    endpoint = BasicEndpoint(
        mock_api,
        'test',
        headers={'Accept': 'application/json'},
        methods=[]
    )

    with pytest.raises(TypeError):
        endpoint + ['stuff']

    with pytest.raises(TypeError):
        endpoint + ('stuff', 'things')

    with pytest.raises(TypeError):
        endpoint + {'stuff': 'junk'}


def test_endpoint__truediv__returns_new_endpoint(mock_api):
    initial_endpoint = BasicEndpoint(
        mock_api,
        'test',
        headers={'Accept': 'application/json'},
        methods=['GET']
    )
    assert initial_endpoint.path == 'test'

    extended_endpoint = initial_endpoint / 1
    assert extended_endpoint.path == 'test/1'

    final_endpoint = extended_endpoint / 'stuff'
    assert final_endpoint.path == 'test/1/stuff'

    assert not mock_api.called


def test_endpoint__truediv__raises_type_error_when_passed_invalid_argument(mock_api):
    endpoint = BasicEndpoint(
        mock_api,
        'test',
        headers={'Accept': 'application/json'},
        methods=[]
    )

    with pytest.raises(TypeError):
        endpoint / ['stuff']

    with pytest.raises(TypeError):
        endpoint / ('stuff', 'things')

    with pytest.raises(TypeError):
        endpoint / {'stuff': 'junk'}
