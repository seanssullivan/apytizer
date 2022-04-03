# -*- coding: utf-8 -*-

# pylint: disable=protected-access

# Standard Library Imports
from unittest.mock import Mock

# Third-Party Imports
import pytest

# Local Imports
from apytizer.apis import BaseAPI
from apytizer.endpoints import CompositeEndpoint
from apytizer.endpoints.composite_endpoint import _Children


@pytest.fixture
def mock_api():
    mock = Mock(BaseAPI)
    mock.url = "base/"
    return mock


# --------------------------------------------------------------------------------
# Tests for CompositeEndpoint Class
# --------------------------------------------------------------------------------
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
    test_endpoint.children.add(child_endpoint)

    result = test_endpoint + "success"
    assert len(test_endpoint.children) == 1
    assert result is child_endpoint


def test__add__adds_endpoint_to_children(mock_api):
    test_endpoint = CompositeEndpoint(mock_api, "test")
    child_endpoint = CompositeEndpoint(mock_api, "success")
    test_endpoint + child_endpoint
    assert child_endpoint in test_endpoint.children


def test__add__makes_child_endpoint_when_passed_a_string(mock_api):
    test_endpoint = CompositeEndpoint(mock_api, "test")
    result = test_endpoint + "success"
    assert result in test_endpoint.children


def test__getattr__returns_endpoint_when_passed_a_string(mock_api):
    test_endpoint = CompositeEndpoint(mock_api, "test")
    result = test_endpoint.success
    assert isinstance(result, CompositeEndpoint)


def test__getattr__makes_child_endpoint_when_passed_a_string(mock_api):
    test_endpoint = CompositeEndpoint(mock_api, "test")
    result = test_endpoint.success
    assert result in test_endpoint.children


def test__getattr__returns_existing_endpoint_when_available(mock_api):
    test_endpoint = CompositeEndpoint(mock_api, "test")
    child_endpoint = CompositeEndpoint(mock_api, "success")
    test_endpoint.children.add(child_endpoint)

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
    assert result in test_endpoint.children


def test__truediv__returns_endpoint_when_passed_a_string(mock_api):
    test_endpoint = CompositeEndpoint(mock_api, "test")
    result = test_endpoint / "success"
    assert isinstance(result, CompositeEndpoint)


def test__truediv__adds_endpoint_to_children(mock_api):
    test_endpoint = CompositeEndpoint(mock_api, "test")
    child_endpoint = CompositeEndpoint(mock_api, "success")
    test_endpoint / child_endpoint
    assert child_endpoint in test_endpoint.children


def test__truediv__makes_child_endpoint_when_passed_a_string(mock_api):
    test_endpoint = CompositeEndpoint(mock_api, "test")
    result = test_endpoint / "success"
    assert result in test_endpoint.children


def test__truediv__returns_existing_endpoint_when_available(mock_api):
    test_endpoint = CompositeEndpoint(mock_api, "test")
    child_endpoint = CompositeEndpoint(mock_api, "success")
    test_endpoint.children.add(child_endpoint)

    result = test_endpoint / "success"
    assert len(test_endpoint.children) == 1
    assert result is child_endpoint


# --------------------------------------------------------------------------------
# Tests for _Children Class
# --------------------------------------------------------------------------------
def test__contains__returns_true_when_endpoint_in_children(mock_api):
    parent = CompositeEndpoint(mock_api, "test")
    endpoint = CompositeEndpoint(mock_api, "testing")
    children = _Children(parent, [endpoint])
    assert endpoint in children


def test__add__method_adds_endpoint_to_children(mock_api):
    parent = CompositeEndpoint(mock_api, "test")
    endpoint = CompositeEndpoint(mock_api, "testing")
    children = _Children(parent)
    children.add(endpoint)

    assert len(children) == 1
    assert endpoint in children


def test_add_method_sets_parent_endpoint_as_context(mock_api):
    parent = CompositeEndpoint(mock_api, "test")
    endpoint = CompositeEndpoint(mock_api, "testing")
    _Children(parent).add(endpoint)
    assert endpoint.parent is parent


def test_clear_method_empties_children(mock_api):
    parent = CompositeEndpoint(mock_api, "tests")
    children = _Children(
        parent,
        [
            CompositeEndpoint(mock_api, "1"),
            CompositeEndpoint(mock_api, "2"),
            CompositeEndpoint(mock_api, "3"),
        ],
    )
    children.clear()
    assert len(children) == 0


def test_discard_method_removes_endpoint_from_children(mock_api):
    parent = CompositeEndpoint(mock_api, "tests")
    endpoint1 = CompositeEndpoint(mock_api, "1")
    endpoint2 = CompositeEndpoint(mock_api, "2")
    endpoint3 = CompositeEndpoint(mock_api, "3")
    children = _Children(parent, [endpoint1, endpoint2, endpoint3])

    children.discard(endpoint1)
    assert len(children) == 2
    assert endpoint1 not in children


def test_discard_method_deletes_parent_endpoint_from_child(mock_api):
    parent = CompositeEndpoint(mock_api, "test")
    endpoint = CompositeEndpoint(mock_api, "testing")
    children = _Children(parent, [endpoint])
    assert endpoint.parent is parent

    children.discard(endpoint)
    assert endpoint.parent is None


def test_get_method_retrieves_endpoint(mock_api):
    parent = CompositeEndpoint(mock_api, "test")
    endpoint1 = CompositeEndpoint(mock_api, "1")
    endpoint2 = CompositeEndpoint(mock_api, "2")
    endpoint3 = CompositeEndpoint(mock_api, "3")
    children = _Children(parent, [endpoint1, endpoint2, endpoint3])

    result = children.get("1")
    assert result is endpoint1


def test_pop_method_removes_endpoint_from_children(mock_api):
    parent = CompositeEndpoint(mock_api, "tests")
    endpoint1 = CompositeEndpoint(mock_api, "1")
    endpoint2 = CompositeEndpoint(mock_api, "2")
    endpoint3 = CompositeEndpoint(mock_api, "3")
    children = _Children(parent, [endpoint1, endpoint2, endpoint3])

    result = children.pop("1")
    assert result not in children


def test_pop_method_returns_removed_endpoint(mock_api):
    parent = CompositeEndpoint(mock_api, "test")
    endpoint1 = CompositeEndpoint(mock_api, "1")
    endpoint2 = CompositeEndpoint(mock_api, "2")
    endpoint3 = CompositeEndpoint(mock_api, "3")
    children = _Children(parent, [endpoint1, endpoint2, endpoint3])

    result = children.pop("2")
    assert result is endpoint2


def test_pop_method_deletes_parent_endpoint_from_child(mock_api):
    parent = CompositeEndpoint(mock_api, "test")
    endpoint = CompositeEndpoint(mock_api, "testing")
    children = _Children(parent, [endpoint])
    assert endpoint.parent is parent

    children.pop("testing")
    assert endpoint.parent is None


def test_remove_method_removes_endpoint_from_children(mock_api):
    parent = CompositeEndpoint(mock_api, "tests")
    endpoint1 = CompositeEndpoint(mock_api, "1")
    endpoint2 = CompositeEndpoint(mock_api, "2")
    endpoint3 = CompositeEndpoint(mock_api, "3")
    children = _Children(parent, [endpoint1, endpoint2, endpoint3])

    children.remove(endpoint2)
    assert len(children) == 2
    assert endpoint2 not in children


def test_remove_method_deletes_parent_endpoint_from_child(mock_api):
    parent = CompositeEndpoint(mock_api, "test")
    endpoint = CompositeEndpoint(mock_api, "testing")
    children = _Children(parent, [endpoint])
    assert endpoint.parent is parent

    children.remove(endpoint)
    assert endpoint.parent is None


def test_update_method_adds_endpoints(mock_api):
    parent = CompositeEndpoint(mock_api, "test")
    endpoint1 = CompositeEndpoint(mock_api, "1")
    children = _Children(parent, [endpoint1])

    endpoint2 = CompositeEndpoint(mock_api, "2")
    endpoint3 = CompositeEndpoint(mock_api, "3")
    children.update([endpoint2, endpoint3])
    assert endpoint2 in children
    assert endpoint3 in children


def test_update_method_sets_parents_as_context(mock_api):
    parent = CompositeEndpoint(mock_api, "test")
    endpoint1 = CompositeEndpoint(mock_api, "test1")
    children = _Children(parent, [endpoint1])

    endpoint2 = CompositeEndpoint(mock_api, "test2")
    endpoint3 = CompositeEndpoint(mock_api, "test3")
    children.update([endpoint2, endpoint3])
    assert endpoint2.parent is parent
    assert endpoint3.parent is parent
