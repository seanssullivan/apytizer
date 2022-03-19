# -*- coding: utf-8 -*-

# Standard Library Imports
from http import HTTPStatus

# Local Imports
from apytizer.base import BaseAPI


# --------------------------------------------------------------------------------
# Tests for HEAD Method
# --------------------------------------------------------------------------------
def test_api_head_request_when_response_is_ok(mock_request):
    mock_request.return_value.ok = True
    mock_request.return_value.headers = {"Content-Type": "application/json"}

    api = BaseAPI(
        url="testing/",
        auth=("test_case", "token"),
    )

    response = api.head("test")

    mock_request.assert_called_once_with(
        "HEAD",
        "testing/test",
        auth=("test_case", "token"),
        headers=None,
        params=None,
    )
    assert response.headers == {"Content-Type": "application/json"}


def test_api_head_response_is_cached(mock_request):
    mock_request.return_value.ok = True

    mock_cache = {}

    api = BaseAPI(
        url="testing/", auth=("test_case", "token"), cache=mock_cache
    )

    first_response = api.head("test")
    second_response = api.head("test")

    assert first_response == second_response
    assert mock_request.call_count == 1
    assert mock_cache == {("HEAD", api, "test"): mock_request.return_value}


def test_api_head_response_not_cached_when_cache_not_provided(mock_request):
    mock_request.return_value.ok = True

    api = BaseAPI(url="testing/", auth=("test_case", "token"))

    first_response = api.head("test")
    second_response = api.head("test")

    assert first_response == second_response
    assert mock_request.call_count == 2


# --------------------------------------------------------------------------------
# Tests for GET Method
# --------------------------------------------------------------------------------
def test_api_get_request_when_response_is_ok(mock_request):
    mock_request.return_value.ok = True
    mock_request.return_value.json.return_value = {
        "name": "example",
        "status": "testing",
    }

    api = BaseAPI(
        url="testing/",
        auth=("test_case", "token"),
        headers={"Accept": "application/json"},
    )

    response = api.get("test")

    mock_request.assert_called_once_with(
        "GET",
        "testing/test",
        auth=("test_case", "token"),
        headers={"Accept": "application/json"},
        params=None,
    )
    assert response.json() == {"name": "example", "status": "testing"}


def test_api_get_request_updates_headers(mock_request):
    mock_request.return_value.ok = True

    api = BaseAPI(url="testing/", headers={"Accept": "application/json"})

    api.get("test", headers={"Accept": "text/html"})

    mock_request.assert_called_once_with(
        "GET",
        "testing/test",
        auth=None,
        headers={"Accept": "text/html"},
        params=None,
    )


def test_api_get_response_is_cached(mock_request):
    mock_request.return_value.ok = True

    mock_cache = {}

    api = BaseAPI(
        url="testing/",
        auth=("test_case", "token"),
        headers={"Accept": "application/json"},
        cache=mock_cache,
    )

    first_response = api.get("test")
    second_response = api.get("test")

    assert first_response == second_response
    assert mock_request.call_count == 1
    assert mock_cache == {("GET", api, "test"): mock_request.return_value}


def test_api_get_response_not_cached_when_cache_not_provided(mock_request):
    mock_request.return_value.ok = True

    api = BaseAPI(
        url="testing/",
        auth=("test_case", "token"),
        headers={"Accept": "application/json"},
    )

    first_response = api.get("test")
    second_response = api.get("test")

    assert first_response == second_response
    assert mock_request.call_count == 2


# --------------------------------------------------------------------------------
# Tests for POST Method
# --------------------------------------------------------------------------------
def test_api_post_request_when_response_is_ok(mock_request):
    mock_request.return_value.ok = True
    mock_request.return_value.status_code = 201

    api = BaseAPI(
        url="testing/",
        auth=("test_case", "token"),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )

    data = {"name": "Test", "completed": True}

    response = api.post("test", data=data)

    mock_request.assert_called_once_with(
        "POST",
        "testing/test",
        auth=("test_case", "token"),
        data=data,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        params=None,
    )
    assert response.status_code == HTTPStatus.CREATED


def test_api_post_request_updates_headers(mock_request):
    mock_request.return_value.ok = True

    api = BaseAPI(
        url="testing/",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )

    api.post(
        "test",
        headers={
            "Accept": "application/xml",
            "Content-Type": "application/xml",
        },
    )

    mock_request.assert_called_once_with(
        "POST",
        "testing/test",
        auth=None,
        headers={
            "Accept": "application/xml",
            "Content-Type": "application/xml",
        },
        params=None,
    )


def test_api_post_response_is_cached(mock_request):
    mock_request.return_value.ok = True

    mock_cache = {}

    api = BaseAPI(
        url="testing/",
        auth=("test_case", "token"),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        cache=mock_cache,
    )

    data = {"name": "Test", "completed": True}

    first_response = api.post("test", data=data)
    second_response = api.post("test", data=data)

    assert first_response == second_response
    assert mock_request.call_count == 1
    assert mock_cache == {
        (
            "POST",
            api,
            "test",
            "data={'name': 'Test', 'completed': True}",
        ): mock_request.return_value
    }


def test_api_post_response_not_cached_when_cache_not_provided(mock_request):
    mock_request.return_value.ok = True

    api = BaseAPI(
        url="testing/",
        auth=("test_case", "token"),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )

    data = {"name": "Test", "completed": True}

    first_response = api.post("test", data=data)
    second_response = api.post("test", data=data)

    assert first_response == second_response
    assert mock_request.call_count == 2


# --------------------------------------------------------------------------------
# Tests for PUT Method
# --------------------------------------------------------------------------------
def test_api_put_request_when_response_is_ok(mock_request):
    mock_request.return_value.ok = True
    mock_request.return_value.status_code = 204

    api = BaseAPI(
        url="testing/",
        auth=("test_case", "token"),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )

    data = {"name": "Test", "completed": True}

    response = api.put("test", data=data)

    mock_request.assert_called_once_with(
        "PUT",
        "testing/test",
        auth=("test_case", "token"),
        data=data,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        params=None,
    )
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_api_put_request_updates_headers(mock_request):
    mock_request.return_value.ok = True

    api = BaseAPI(
        url="testing/",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )

    api.put(
        "test",
        headers={
            "Accept": "application/xml",
            "Content-Type": "application/xml",
        },
    )

    mock_request.assert_called_once_with(
        "PUT",
        "testing/test",
        auth=None,
        headers={
            "Accept": "application/xml",
            "Content-Type": "application/xml",
        },
        params=None,
    )


def test_api_put_response_is_cached(mock_request):
    mock_request.return_value.ok = True

    mock_cache = {}

    api = BaseAPI(
        url="testing/",
        auth=("test_case", "token"),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        cache=mock_cache,
    )

    data = {"name": "Test", "completed": True}

    first_response = api.put("test", data=data)
    second_response = api.put("test", data=data)

    assert first_response == second_response
    assert mock_request.call_count == 1
    assert mock_cache == {
        (
            "PUT",
            api,
            "test",
            "data={'name': 'Test', 'completed': True}",
        ): mock_request.return_value
    }


def test_api_put_response_not_cached_when_cache_not_provided(mock_request):
    mock_request.return_value.ok = True

    api = BaseAPI(
        url="testing/",
        auth=("test_case", "token"),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )

    data = {"name": "Test", "completed": True}

    first_response = api.put("test", data=data)
    second_response = api.put("test", data=data)

    assert first_response == second_response
    assert mock_request.call_count == 2


# --------------------------------------------------------------------------------
# Tests for PATCH Method
# --------------------------------------------------------------------------------
def test_api_patch_request_when_response_is_ok(mock_request):
    mock_request.return_value.ok = True
    mock_request.return_value.status_code = 204

    api = BaseAPI(
        url="testing/",
        auth=("test_case", "token"),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )

    data = {"name": "Test", "completed": True}

    response = api.patch("test", data=data)

    mock_request.assert_called_once_with(
        "PATCH",
        "testing/test",
        auth=("test_case", "token"),
        data=data,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        params=None,
    )
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_api_patch_request_updates_headers(mock_request):
    mock_request.return_value.ok = True

    api = BaseAPI(
        url="testing/",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )

    api.patch(
        "test",
        headers={
            "Accept": "application/xml",
            "Content-Type": "application/xml",
        },
    )

    mock_request.assert_called_once_with(
        "PATCH",
        "testing/test",
        auth=None,
        headers={
            "Accept": "application/xml",
            "Content-Type": "application/xml",
        },
        params=None,
    )


def test_api_patch_response_is_cached(mock_request):
    mock_request.return_value.ok = True

    mock_cache = {}

    api = BaseAPI(
        url="testing/",
        auth=("test_case", "token"),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        cache=mock_cache,
    )

    data = {"name": "Test", "completed": True}

    first_response = api.patch("test", data=data)
    second_response = api.patch("test", data=data)

    assert first_response == second_response
    assert mock_request.call_count == 1
    assert mock_cache == {
        (
            "PATCH",
            api,
            "test",
            "data={'name': 'Test', 'completed': True}",
        ): mock_request.return_value
    }


def test_api_patch_response_not_cached_when_cache_not_provided(mock_request):
    mock_request.return_value.ok = True

    api = BaseAPI(
        url="testing/",
        auth=("test_case", "token"),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )

    data = {"name": "Test", "completed": True}

    first_response = api.patch("test", data=data)
    second_response = api.patch("test", data=data)

    assert first_response == second_response
    assert mock_request.call_count == 2


# --------------------------------------------------------------------------------
# Tests for DELETE Method
# --------------------------------------------------------------------------------
def test_api_delete_request_when_response_is_ok(mock_request):
    mock_request.return_value.ok = True
    mock_request.return_value.status_code = 204

    api = BaseAPI(
        url="testing/",
        auth=("test_case", "token"),
    )

    response = api.delete("test")

    mock_request.assert_called_once_with(
        "DELETE",
        "testing/test",
        auth=("test_case", "token"),
        headers=None,
        params=None,
    )
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_api_delete_response_is_cached(mock_request):
    mock_request.return_value.ok = True

    mock_cache = {}

    api = BaseAPI(
        url="testing/", auth=("test_case", "token"), cache=mock_cache
    )

    first_response = api.delete("test")
    second_response = api.delete("test")

    assert first_response == second_response
    assert mock_request.call_count == 1
    assert mock_cache == {("DELETE", api, "test"): mock_request.return_value}


def test_api_delete_response_not_cached_when_cache_not_provided(mock_request):
    mock_request.return_value.ok = True

    api = BaseAPI(url="testing/", auth=("test_case", "token"))

    first_response = api.delete("test")
    second_response = api.delete("test")

    assert first_response == second_response
    assert mock_request.call_count == 2


# --------------------------------------------------------------------------------
# Tests for OPTIONS Method
# --------------------------------------------------------------------------------
def test_api_options_request_when_response_is_ok(mock_request):
    mock_request.return_value.ok = True
    mock_request.return_value.headers = {
        "Allow": ["OPTIONS", "GET", "POST", "PUT", "DELETE"]
    }

    api = BaseAPI(
        url="testing/",
        auth=("test_case", "token"),
    )

    response = api.options("test")

    mock_request.assert_called_once_with(
        "OPTIONS",
        "testing/test",
        auth=("test_case", "token"),
        headers=None,
        params=None,
    )
    assert response.headers == {
        "Allow": ["OPTIONS", "GET", "POST", "PUT", "DELETE"]
    }


def test_api_options_response_is_cached(mock_request):
    mock_request.return_value.ok = True

    mock_cache = {}

    api = BaseAPI(
        url="testing/", auth=("test_case", "token"), cache=mock_cache
    )

    first_response = api.options("test")
    second_response = api.options("test")

    assert first_response == second_response
    assert mock_request.call_count == 1
    assert mock_cache == {("OPTIONS", api, "test"): mock_request.return_value}


def test_api_options_response_not_cached_when_cache_not_provided(mock_request):
    mock_request.return_value.ok = True

    api = BaseAPI(url="testing/", auth=("test_case", "token"))

    first_response = api.options("test")
    second_response = api.options("test")

    assert first_response == second_response
    assert mock_request.call_count == 2


# --------------------------------------------------------------------------------
# Tests for TRACE Method
# --------------------------------------------------------------------------------
def test_api_trace_request_when_response_is_ok(mock_request):
    mock_request.return_value.ok = True
    mock_request.return_value.headers = {"Content-Type": "application/json"}

    api = BaseAPI(
        url="testing/",
        auth=("test_case", "token"),
    )

    response = api.trace("test")

    mock_request.assert_called_once_with(
        "TRACE",
        "testing/test",
        auth=("test_case", "token"),
        headers=None,
        params=None,
    )
    assert response.headers == {"Content-Type": "application/json"}


def test_api_trace_response_is_cached(mock_request):
    mock_request.return_value.ok = True

    mock_cache = {}

    api = BaseAPI(
        url="testing/", auth=("test_case", "token"), cache=mock_cache
    )

    first_response = api.trace("test")
    second_response = api.trace("test")

    assert first_response == second_response
    assert mock_request.call_count == 1
    assert mock_cache == {("TRACE", api, "test"): mock_request.return_value}


def test_api_trace_response_not_cached_when_cache_not_provided(mock_request):
    mock_request.return_value.ok = True

    api = BaseAPI(url="testing/", auth=("test_case", "token"))

    first_response = api.trace("test")
    second_response = api.trace("test")

    assert first_response == second_response
    assert mock_request.call_count == 2
