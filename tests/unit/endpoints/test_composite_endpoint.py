# -*- coding: utf-8 -*-

# pylint: disable=protected-access

# Standard Library Imports
from unittest.mock import Mock

# Third-Party Imports
import pytest

# Local Imports
from apytizer.apis import BaseAPI
from apytizer.endpoints import CompositeEndpoint


@pytest.fixture
def mock_api():
    mock = Mock(BaseAPI)
    mock.url = "base/"
    return mock


def test_prepends_parent_to_endpoint_path(mock_api):
    parent = CompositeEndpoint(mock_api, "test")
    endpoint = CompositeEndpoint(mock_api, "success")
    endpoint.parent = parent
    assert endpoint.path == "test/success"


def test_endpoint_uri_contains_base_url_and_path(mock_api):
    parent = CompositeEndpoint(mock_api, "test")
    endpoint = CompositeEndpoint(mock_api, "success")
    endpoint.parent = parent
    assert endpoint.uri == "base/test/success"


def test__add__returns_endpoint_when_passed_a_string(mock_api):
    test_endpoint = CompositeEndpoint(mock_api, "test")
    result = test_endpoint + "success"
    assert isinstance(result, CompositeEndpoint)


def test__add__returns_existing_endpoint_when_available(mock_api):
    test_endpoint = CompositeEndpoint(mock_api, "test")
    child_endpoint = CompositeEndpoint(mock_api, "success")
    test_endpoint.children.data["success"] = child_endpoint

    result = test_endpoint + "success"
    assert len(test_endpoint.children) == 1
    assert result is child_endpoint


def test__add__adds_endpoint_to_children(mock_api):
    test_endpoint = CompositeEndpoint(mock_api, "test")
    child_endpoint = CompositeEndpoint(mock_api, "success")
    test_endpoint + child_endpoint
    assert child_endpoint in test_endpoint.children.values()


def test__add__makes_child_endpoint_when_passed_a_string(mock_api):
    test_endpoint = CompositeEndpoint(mock_api, "test")
    result = test_endpoint + "success"
    assert result in test_endpoint.children.values()


def test__getattr__returns_endpoint_when_passed_a_string(mock_api):
    test_endpoint = CompositeEndpoint(mock_api, "test")
    result = test_endpoint.success
    assert isinstance(result, CompositeEndpoint)


def test__getattr__makes_child_endpoint_when_passed_a_string(mock_api):
    test_endpoint = CompositeEndpoint(mock_api, "test")
    result = test_endpoint.success
    assert result in test_endpoint.children.values()


def test__getattr__returns_existing_endpoint_when_available(mock_api):
    test_endpoint = CompositeEndpoint(mock_api, "test")
    child_endpoint = CompositeEndpoint(mock_api, "success")
    test_endpoint.children.data["success"] = child_endpoint

    result = test_endpoint.success
    assert len(test_endpoint.children) == 1
    assert result is child_endpoint


def test__getitem__returns_endpoint_when_passed_a_string(mock_api):
    test_endpoint = CompositeEndpoint(mock_api, "test")
    result = test_endpoint["success"]
    assert isinstance(result, CompositeEndpoint)


def test__getitem__makes_child_endpoint_when_passed_a_string(mock_api):
    test_endpoint = CompositeEndpoint(mock_api, "test")
    result = test_endpoint["success"]
    assert result in test_endpoint.children.values()


def test__truediv__returns_endpoint_when_passed_a_string(mock_api):
    test_endpoint = CompositeEndpoint(mock_api, "test")
    result = test_endpoint / "success"
    assert isinstance(result, CompositeEndpoint)


def test__truediv__adds_endpoint_to_children(mock_api):
    test_endpoint = CompositeEndpoint(mock_api, "test")
    child_endpoint = CompositeEndpoint(mock_api, "success")
    test_endpoint / child_endpoint
    assert child_endpoint in test_endpoint.children.values()


def test__truediv__makes_child_endpoint_when_passed_a_string(mock_api):
    test_endpoint = CompositeEndpoint(mock_api, "test")
    result = test_endpoint / "success"
    assert result in test_endpoint.children.values()


def test__truediv__returns_existing_endpoint_when_available(mock_api):
    test_endpoint = CompositeEndpoint(mock_api, "test")
    child_endpoint = CompositeEndpoint(mock_api, "success")
    test_endpoint.children.data["success"] = child_endpoint

    result = test_endpoint / "success"
    assert len(test_endpoint.children) == 1
    assert result is child_endpoint
