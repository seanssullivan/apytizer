# -*- coding: utf-8 -*-

# Standard Library Imports
from unittest.mock import Mock

# Third-Party Imports
import pytest

# Local Imports
try:
    from apytizer.apis import BaseWebAPI
    from apytizer.endpoints import BaseEndpoint
    from apytizer.engines import BaseEngine
    from apytizer.http_methods import HTTPMethod
    from apytizer.routes import Route
    from apytizer import errors

except ImportError:
    from src.apytizer.apis import BaseWebAPI
    from src.apytizer.endpoints import BaseEndpoint
    from src.apytizer.engines import BaseEngine
    from src.apytizer.http_methods import HTTPMethod
    from src.apytizer.routes import Route
    from src.apytizer import errors

from ... import mocks


# Constants:
ALLOWED_METHODS = {
    "HEAD",
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
    "TRACE",
}


# ----------------------------------------------------------------------------
# Tests for Base Endpoint
# ----------------------------------------------------------------------------
def test_url_contains_base_and_path(mock_api: mocks.MockAPI) -> None:
    endpoint = BaseEndpoint(mock_api, "test")
    assert endpoint.url == mock_api.url + "test"


@pytest.mark.parametrize("method", ALLOWED_METHODS)
def test_endpoint_method_sends_request(
    mock_api: mocks.MockAPI, method: str
) -> None:
    endpoint = BaseEndpoint(mock_api, "test")
    getattr(endpoint, method.lower())()
    assert_method_called(mock_api, method)


@pytest.mark.parametrize("method", ALLOWED_METHODS)
def test_endpoint_raises_error_when_method_not_allowed(
    mock_api: mocks.MockAPI, method: str
) -> None:
    allowed_methods = [HTTPMethod(m) for m in ALLOWED_METHODS if m != method]
    endpoint = BaseEndpoint(mock_api, "test", methods=allowed_methods)

    with pytest.raises(errors.MethodNotAllowed):
        getattr(endpoint, method.lower())()

    assert_method_not_called(mock_api, method)


@pytest.mark.parametrize("method", ALLOWED_METHODS)
def test_endpoint_caches_response_when_cache_provided(
    mock_api: mocks.MockAPI, method: str
) -> None:
    endpoint = BaseEndpoint(mock_api, "test", cache={})

    getattr(endpoint, method.lower())()
    getattr(endpoint, method.lower())()

    assert_method_call_count(mock_api, method, 1)


@pytest.mark.parametrize("method", ALLOWED_METHODS)
def test_endpoint_does_not_cache_response_when_no_cache_provided(
    mock_api: mocks.MockAPI, method: str
) -> None:
    endpoint = BaseEndpoint(mock_api, "test")

    getattr(endpoint, method.lower())()
    getattr(endpoint, method.lower())()

    assert_method_call_count(mock_api, method, 2)


def test_indexing_returns_endpoint() -> None:
    api = BaseWebAPI(BaseEngine("testing.com"))
    endpoint = BaseEndpoint(api, "test")
    result = endpoint["success"]
    assert isinstance(result, BaseEndpoint)


def test_slash_operator_returns_endpoint() -> None:
    api = BaseWebAPI(BaseEngine("testing.com"))
    endpoint = BaseEndpoint(api, "test")
    result = endpoint / "success"
    assert isinstance(result, BaseEndpoint)


def test_indexing_returns_custom_endpoint() -> None:
    class TestEndpoint(BaseEndpoint): ...

    endpoints = {Route("test/success"): TestEndpoint}
    api = BaseWebAPI(BaseEngine("testing.com"), endpoints)
    endpoint = BaseEndpoint(api, "test")
    result = endpoint["success"]
    assert isinstance(result, TestEndpoint)


def test_slash_operator_returns_custom_endpoint() -> None:
    class TestEndpoint(BaseEndpoint): ...

    endpoints = {Route("test/success"): TestEndpoint}
    api = BaseWebAPI(BaseEngine("testing.com"), endpoints)
    endpoint = BaseEndpoint(api, "test")
    result = endpoint / "success"
    assert isinstance(result, TestEndpoint)


def test_indexing_returns_endpoint_with_path_argument() -> None:
    class TestEndpoint(BaseEndpoint): ...

    endpoints = {
        Route("test"): BaseEndpoint,
        Route("test/{}"): TestEndpoint,
        Route("test/failure"): BaseEndpoint,
    }
    api = BaseWebAPI(BaseEngine("testing.com"), endpoints)
    endpoint = BaseEndpoint(api, "test")
    result = endpoint["1"]
    assert isinstance(result, TestEndpoint)


def test_slash_operator_returns_endpoint_with_path_argument() -> None:
    class TestEndpoint(BaseEndpoint): ...

    endpoints = {
        Route("test"): BaseEndpoint,
        Route("test/{}"): TestEndpoint,
        Route("test/failure"): BaseEndpoint,
    }
    api = BaseWebAPI(BaseEngine("testing.com"), endpoints)
    endpoint = BaseEndpoint(api, "test")
    result = endpoint / "1"
    assert isinstance(result, TestEndpoint)


def test_indexing_returns_most_specific_endpoint() -> None:
    class TestEndpoint(BaseEndpoint): ...

    endpoints = {
        Route("test"): BaseEndpoint,
        Route("test/{}"): BaseEndpoint,
        Route("test/success"): TestEndpoint,
    }
    api = BaseWebAPI(BaseEngine("testing.com"), endpoints)
    endpoint = BaseEndpoint(api, "test")
    result = endpoint["success"]
    assert isinstance(result, TestEndpoint)


def test_slash_operator_returns_most_specific_endpoint() -> None:
    class TestEndpoint(BaseEndpoint): ...

    endpoints = {
        Route("test"): BaseEndpoint,
        Route("test/{}"): BaseEndpoint,
        Route("test/success"): TestEndpoint,
    }
    api = BaseWebAPI(BaseEngine("testing.com"), endpoints)
    endpoint = BaseEndpoint(api, "test")
    result = endpoint / "success"
    assert isinstance(result, TestEndpoint)


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
def assert_method_called(__api: mocks.MockAPI, method: str) -> None:
    func = getattr(__api.connection, method.lower())  # type: Mock
    assert func.called


def assert_method_call_count(
    __api: mocks.MockAPI, method: str, count: int
) -> None:
    func = getattr(__api.connection, method.lower())  # type: Mock
    assert func.call_count == count


def assert_method_not_called(__api: mocks.MockAPI, method: str) -> None:
    func = getattr(__api.connection, method.lower())  # type: Mock
    assert not func.called
