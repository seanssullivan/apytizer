# -*- coding: utf-8 -*-

# Standard Library Imports
from typing import Dict
from typing import Type
from unittest.mock import Mock

# Third-Party Imports
import pytest

# Local Imports
try:
    from apytizer.apis import WebAPI
    from apytizer.endpoints import WebEndpoint
    from apytizer.engines import HTTPEngine
    from apytizer.routes import AbstractRoute
    from apytizer.routes import Route
    from apytizer import errors

except ImportError:
    from src.apytizer.apis import WebAPI
    from src.apytizer.endpoints import WebEndpoint
    from src.apytizer.engines import HTTPEngine
    from src.apytizer.routes import AbstractRoute
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
        WebAPI("testing.com")  # type: ignore


def test_raises_error_when_endpoints_are_not_passed_as_dictionary() -> None:
    with pytest.raises(TypeError):
        WebAPI(HTTPEngine("testing.com"), "/failure")  # type: ignore


def test_apis_with_same_url_are_equal() -> None:
    api1 = WebAPI(HTTPEngine("testing.com"))
    api2 = WebAPI(HTTPEngine("testing.com"))
    assert api1 == api2


def test_apis_with_different_urls_are_not_equal() -> None:
    api1 = WebAPI(HTTPEngine("first.com"))
    api2 = WebAPI(HTTPEngine("second.com"))
    assert api1 != api2


@pytest.mark.parametrize("method", ALLOWED_METHODS)
def test_calling_api_method_sends_request(
    mock_engine: mocks.MockEngine, method: str
) -> None:
    with WebAPI(mock_engine) as api:
        getattr(api, method.lower())()
        assert_method_called(api.connection, method)  # type: ignore


@pytest.mark.parametrize("method", ALLOWED_METHODS)
def test_raises_error_when_connection_not_started(
    mock_engine: mocks.MockEngine, method: str
) -> None:
    with pytest.raises(errors.ConnectionNotStarted):
        api = WebAPI(mock_engine)
        getattr(api, method.lower())()


def test_indexing_returns_endpoint() -> None:
    api = WebAPI(HTTPEngine("testing.com"))
    result = api["home"]
    assert isinstance(result, WebEndpoint)


def test_slash_operator_returns_endpoint() -> None:
    api = WebAPI(HTTPEngine("testing.com"))
    result = api / "home"
    assert isinstance(result, WebEndpoint)


def test_indexing_returns_custom_endpoint() -> None:
    class TestEndpoint(WebEndpoint): ...

    endpoints: Dict[AbstractRoute, Type[WebEndpoint]] = {
        Route("test"): TestEndpoint
    }
    api = WebAPI(HTTPEngine("testing.com"), endpoints)
    result = api["test"]
    assert isinstance(result, TestEndpoint)


def test_slash_operator_returns_custom_endpoint() -> None:
    class TestEndpoint(WebEndpoint): ...

    endpoints: Dict[AbstractRoute, Type[WebEndpoint]] = {
        Route("test"): TestEndpoint
    }
    api = WebAPI(HTTPEngine("testing.com"), endpoints)
    result = api / "test"
    assert isinstance(result, TestEndpoint)


def test_indexing_returns_endpoint_with_path_argument() -> None:
    class TestEndpoint(WebEndpoint): ...

    endpoints: Dict[AbstractRoute, Type[WebEndpoint]] = {
        Route("test"): WebEndpoint,
        Route("test/{}"): TestEndpoint,
        Route("test/failure"): WebEndpoint,
    }
    api = WebAPI(HTTPEngine("testing.com"), endpoints)
    result = api["test/1"]
    assert isinstance(result, TestEndpoint)


def test_slash_operator_returns_endpoint_with_path_argument() -> None:
    class TestEndpoint(WebEndpoint): ...

    endpoints: Dict[AbstractRoute, Type[WebEndpoint]] = {
        Route("test"): WebEndpoint,
        Route("test/{}"): TestEndpoint,
        Route("test/failure"): WebEndpoint,
    }
    api = WebAPI(HTTPEngine("testing.com"), endpoints)
    result = api / "test/1"
    assert isinstance(result, TestEndpoint)


def test_indexing_returns_most_specific_endpoint() -> None:
    class TestEndpoint(WebEndpoint): ...

    endpoints: Dict[AbstractRoute, Type[WebEndpoint]] = {
        Route("test"): WebEndpoint,
        Route("test/{}"): WebEndpoint,
        Route("test/success"): TestEndpoint,
    }
    api = WebAPI(HTTPEngine("testing.com"), endpoints)
    result = api["test/success"]
    assert isinstance(result, TestEndpoint)


def test_slash_operator_returns_most_specific_endpoint() -> None:
    class TestEndpoint(WebEndpoint): ...

    endpoints: Dict[AbstractRoute, Type[WebEndpoint]] = {
        Route("test"): WebEndpoint,
        Route("test/{}"): WebEndpoint,
        Route("test/success"): TestEndpoint,
    }
    api = WebAPI(HTTPEngine("testing.com"), endpoints)
    result = api / "test/success"
    assert isinstance(result, TestEndpoint)


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
def assert_method_called(__connection: Mock, method: str) -> None:
    func: Mock = getattr(__connection, method.lower())
    assert func.called
