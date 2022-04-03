# -*- coding: utf-8 -*-

# Standard Library Imports
from unittest.mock import Mock

# Third-Party Imports
import requests
from requests.adapters import HTTPAdapter

# Local Imports
from apytizer.apis import SessionAPI
from apytizer.apis.session_api import _RequestsSessionBuilder
from apytizer.apis.session_api import _RequestsSessionFactory


# --------------------------------------------------------------------------------
# Tests for Session API
# --------------------------------------------------------------------------------
def test_session_start_method_creates_session():
    api = SessionAPI(url="testing/")
    assert not api.session

    api.start()
    result = api.session
    api.close()

    assert isinstance(result, requests.Session)


def test_session_start_method_sets_authentication():
    api = SessionAPI(
        url="testing/",
        auth=("test_case", "token"),
    )

    api.start()
    result = api.session.auth
    api.close()

    assert result == ("test_case", "token")


def test_session_start_method_updates_headers():
    api = SessionAPI(url="testing/", headers={"Accept": "application/json"})

    api.start()
    result = api.session.headers.items()
    api.close()

    assert ("Accept", "application/json") in result


def test_session_start_method_mounts_adapter():
    mock_adapter = Mock(HTTPAdapter)
    api = SessionAPI(url="testing/", adapter=mock_adapter)

    api.start()
    result = api.session.adapters
    api.close()

    print(result)
    assert result["https://"] is mock_adapter
    assert result["http://"] is mock_adapter


# --------------------------------------------------------------------------------
# Tests for Requests Session Builder
# --------------------------------------------------------------------------------
def test_builder_returns_requests_session():
    builder = _RequestsSessionBuilder()
    result = builder.session
    assert isinstance(result, requests.Session)


def test_builder_adds_adapter_to_requests_session():
    builder = _RequestsSessionBuilder()
    builder.include_adapter("Mock Adapter")
    result = builder.session
    assert result.adapters["https://"] == "Mock Adapter"
    assert result.adapters["http://"] == "Mock Adapter"


def test_builder_adds_authentication_to_requests_session():
    builder = _RequestsSessionBuilder()
    builder.include_auth(("test", "token"))
    result = builder.session
    assert result.auth == ("test", "token")


def test_builder_adds_default_headers_to_requests_session():
    default_headers = {"Accept": "application/json"}
    builder = _RequestsSessionBuilder()
    builder.include_default_headers(default_headers)
    result = builder.session
    assert "application/json" in result.headers["Accept"]


# --------------------------------------------------------------------------------
# Tests for Requests Session Factory
# --------------------------------------------------------------------------------
def test_factory_returns_requests_session():
    factory = _RequestsSessionFactory()
    result = factory.make_session(
        adapter="Mock Adapter",
        auth=("test", "token"),
        headers={"Accept": "application/json"},
    )
    assert isinstance(result, requests.Session)
    assert result.adapters["http://"] == "Mock Adapter"
    assert result.auth == ("test", "token")
    assert "application/json" in result.headers["Accept"]
