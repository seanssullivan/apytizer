# -*- coding: utf-8 -*-

# Standard Library Imports
from typing import Any
from typing import Dict
from unittest.mock import Mock

# Third-Party Imports
from requests import Request

# Local Imports
try:
    from apytizer.connections import HttpConnection
    from apytizer.sessions import sessionmaker
    from apytizer.http_methods import HTTPMethod

except ImportError:
    from src.apytizer.connections import HttpConnection
    from src.apytizer.sessions import sessionmaker
    from src.apytizer.http_methods import HTTPMethod

from ... import mocks

# Custom types
Headers = Dict[str, Any]
Params = Dict[str, Any]

# Constants
DEFAULT_FACTORY = sessionmaker(mocks.MockSession)  # type: ignore

# Media Types
APPLICATION_JSON = "application/json"
TEXT_HTML = "text/html"


# ----------------------------------------------------------------------------
# Tests for Request Method
# ----------------------------------------------------------------------------
def test_connection_sends_request_to_session() -> None:
    engine = mocks.MockEngine("testing/")
    connection = HttpConnection(engine, session_factory=DEFAULT_FACTORY)

    with connection:
        connection.request(HTTPMethod.GET)

    result = get_request(connection)
    assert isinstance(result, Request)


def test_connection_updates_request_headers() -> None:
    engine = mocks.MockEngine("testing/", headers={"Accept": APPLICATION_JSON})
    connection = HttpConnection(engine, session_factory=DEFAULT_FACTORY)

    with connection:
        connection.request(HTTPMethod.GET, headers={"Accept": TEXT_HTML})

    assert_headers_equal(connection, {"Accept": TEXT_HTML})


def test_connection_updates_request_params() -> None:
    engine = mocks.MockEngine("testing/", params={"result": "failure"})
    connection = HttpConnection(engine, session_factory=DEFAULT_FACTORY)

    with connection:
        connection.request(HTTPMethod.GET, params={"result": "success"})

    assert_params_equal(connection, {"result": "success"})


# ----------------------------------------------------------------------------
# Tests for HEAD Method
# ----------------------------------------------------------------------------
def test_connection_sends_head_request() -> None:
    engine = mocks.MockEngine("testing/")
    connection = HttpConnection(engine, session_factory=DEFAULT_FACTORY)

    with connection:
        connection.head()

    assert_request_sent(connection)
    assert_method_equal(connection, HTTPMethod.HEAD)


# ----------------------------------------------------------------------------
# Tests for GET Method
# ----------------------------------------------------------------------------
def test_connection_sends_get_request() -> None:
    engine = mocks.MockEngine("testing/")
    connection = HttpConnection(engine, session_factory=DEFAULT_FACTORY)

    with connection:
        connection.get()

    assert_request_sent(connection)
    assert_method_equal(connection, HTTPMethod.GET)


# ----------------------------------------------------------------------------
# Tests for POST Method
# ----------------------------------------------------------------------------
def test_connection_sends_post_request() -> None:
    engine = mocks.MockEngine("testing/")
    connection = HttpConnection(engine, session_factory=DEFAULT_FACTORY)

    with connection:
        connection.post()

    assert_request_sent(connection)
    assert_method_equal(connection, HTTPMethod.POST)


# ----------------------------------------------------------------------------
# Tests for PUT Method
# ----------------------------------------------------------------------------
def test_connection_sends_put_request() -> None:
    engine = mocks.MockEngine("testing/")
    connection = HttpConnection(engine, session_factory=DEFAULT_FACTORY)

    with connection:
        connection.put()

    assert_request_sent(connection)
    assert_method_equal(connection, HTTPMethod.PUT)


# ----------------------------------------------------------------------------
# Tests for PATCH Method
# ----------------------------------------------------------------------------
def test_connection_sends_patch_request() -> None:
    engine = mocks.MockEngine("testing/")
    connection = HttpConnection(engine, session_factory=DEFAULT_FACTORY)

    with connection:
        connection.patch()

    assert_request_sent(connection)
    assert_method_equal(connection, HTTPMethod.PATCH)


# ----------------------------------------------------------------------------
# Tests for DELETE Method
# ----------------------------------------------------------------------------
def test_connection_sends_delete_request() -> None:
    engine = mocks.MockEngine("testing/")
    connection = HttpConnection(engine, session_factory=DEFAULT_FACTORY)

    with connection:
        connection.delete()

    assert_request_sent(connection)
    assert_method_equal(connection, HTTPMethod.DELETE)


# ----------------------------------------------------------------------------
# Tests for OPTIONS Method
# ----------------------------------------------------------------------------
def test_connection_sends_options_request() -> None:
    engine = mocks.MockEngine("testing/")
    connection = HttpConnection(engine, session_factory=DEFAULT_FACTORY)

    with connection:
        connection.options()

    assert_request_sent(connection)
    assert_method_equal(connection, HTTPMethod.OPTIONS)


# ----------------------------------------------------------------------------
# Tests for TRACE Method
# ----------------------------------------------------------------------------
def test_connection_sends_trace_request() -> None:
    engine = mocks.MockEngine("testing/")
    connection = HttpConnection(engine, session_factory=DEFAULT_FACTORY)

    with connection:
        connection.trace()

    assert_request_sent(connection)
    assert_method_equal(connection, HTTPMethod.TRACE)


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
# --------------------------------- Requests ---------------------------------
def assert_request_sent(__conn: HttpConnection) -> None:
    mock: Mock = getattr(__conn.session, "mock")
    mock.assert_called_once()


def get_request(__conn: HttpConnection) -> Request:
    mock: Mock = getattr(__conn.session, "mock")
    return mock.call_args[0][0]


# --------------------------------- Headers ----------------------------------
def assert_headers_equal(__conn: HttpConnection, headers: Headers) -> None:
    result = get_request_headers(__conn)
    assert result == headers


def get_request_headers(__conn: HttpConnection) -> Headers:
    request = get_request(__conn)
    return request.headers


# ---------------------------------- Params ----------------------------------
def assert_params_equal(__conn: HttpConnection, params: Params) -> None:
    result = get_request_params(__conn)
    assert result == params


def get_request_params(__conn: HttpConnection) -> Params:
    request = get_request(__conn)
    return request.params


# ------------------------------- HTTP Method --------------------------------
def assert_method_equal(__conn: HttpConnection, method: HTTPMethod) -> None:
    result = get_request_method(__conn)
    assert result == method


def get_request_method(__conn: HttpConnection) -> str:
    request = get_request(__conn)
    return request.method
