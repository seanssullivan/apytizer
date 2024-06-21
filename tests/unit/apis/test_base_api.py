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
    from apytizer.routes import Route
    from apytizer import errors

except ImportError:
    from src.apytizer.apis import BaseWebAPI
    from src.apytizer.endpoints import BaseEndpoint
    from src.apytizer.engines import BaseEngine
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


def test_raises_error_when_argument_is_not_type_engine() -> None:
    with pytest.raises(TypeError):
        BaseWebAPI("testing.com")


def test_raises_error_when_endpoints_are_not_passed_as_dictionary() -> None:
    with pytest.raises(TypeError):
        BaseWebAPI(BaseEngine("testing.com"), "/failure")


def test_apis_with_same_url_are_equal() -> None:
    api1 = BaseWebAPI(BaseEngine("testing.com"))
    api2 = BaseWebAPI(BaseEngine("testing.com"))
    assert api1 == api2


def test_apis_with_different_urls_are_not_equal() -> None:
    api1 = BaseWebAPI(BaseEngine("first.com"))
    api2 = BaseWebAPI(BaseEngine("second.com"))
    assert api1 != api2


@pytest.mark.parametrize("method", ALLOWED_METHODS)
def test_calling_api_method_sends_request(
    mock_engine: mocks.MockEngine, method: str
) -> None:
    with BaseWebAPI(mock_engine) as api:
        getattr(api, method.lower())()
        assert_method_called(api.connection, method)


@pytest.mark.parametrize("method", ALLOWED_METHODS)
def test_raises_error_when_connection_not_started(
    mock_engine: mocks.MockEngine, method: str
) -> None:
    with pytest.raises(errors.ConnectionNotStarted):
        api = BaseWebAPI(mock_engine)
        getattr(api, method.lower())()


def test_indexing_returns_endpoint() -> None:
    api = BaseWebAPI(BaseEngine("testing.com"))
    result = api["home"]
    assert isinstance(result, BaseEndpoint)


def test_slash_operator_returns_endpoint() -> None:
    api = BaseWebAPI(BaseEngine("testing.com"))
    result = api / "home"
    assert isinstance(result, BaseEndpoint)


def test_indexing_returns_custom_endpoint() -> None:
    class TestEndpoint(BaseEndpoint): ...

    endpoints = {Route("test"): TestEndpoint}
    api = BaseWebAPI(BaseEngine("testing.com"), endpoints)
    result = api["test"]
    assert isinstance(result, TestEndpoint)


def test_slash_operator_returns_custom_endpoint() -> None:
    class TestEndpoint(BaseEndpoint): ...

    endpoints = {Route("test"): TestEndpoint}
    api = BaseWebAPI(BaseEngine("testing.com"), endpoints)
    result = api / "test"
    assert isinstance(result, TestEndpoint)


def test_indexing_returns_endpoint_with_path_argument() -> None:
    class TestEndpoint(BaseEndpoint): ...

    endpoints = {
        Route("test"): BaseEndpoint,
        Route("test/{}"): TestEndpoint,
        Route("test/failure"): BaseEndpoint,
    }
    api = BaseWebAPI(BaseEngine("testing.com"), endpoints)
    result = api["test/1"]
    assert isinstance(result, TestEndpoint)


def test_slash_operator_returns_endpoint_with_path_argument() -> None:
    class TestEndpoint(BaseEndpoint): ...

    endpoints = {
        Route("test"): BaseEndpoint,
        Route("test/{}"): TestEndpoint,
        Route("test/failure"): BaseEndpoint,
    }
    api = BaseWebAPI(BaseEngine("testing.com"), endpoints)
    result = api / "test/1"
    assert isinstance(result, TestEndpoint)


def test_indexing_returns_most_specific_endpoint() -> None:
    class TestEndpoint(BaseEndpoint): ...

    endpoints = {
        Route("test"): BaseEndpoint,
        Route("test/{}"): BaseEndpoint,
        Route("test/success"): TestEndpoint,
    }
    api = BaseWebAPI(BaseEngine("testing.com"), endpoints)
    result = api["test/success"]
    assert isinstance(result, TestEndpoint)


def test_slash_operator_returns_most_specific_endpoint() -> None:
    class TestEndpoint(BaseEndpoint): ...

    endpoints = {
        Route("test"): BaseEndpoint,
        Route("test/{}"): BaseEndpoint,
        Route("test/success"): TestEndpoint,
    }
    api = BaseWebAPI(BaseEngine("testing.com"), endpoints)
    result = api / "test/success"
    assert isinstance(result, TestEndpoint)


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
def assert_method_called(__connection: Mock, method: str) -> None:
    func = getattr(__connection, method.lower())  # type: Mock
    assert func.called
