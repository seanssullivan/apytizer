# -*- coding: utf-8 -*-

# Standard Library Imports
from unittest import mock

# Local Imports
from apytizer import utils


def test_deep_get_returns_value():
    obj = {"first": "Success"}
    result = utils.deep_get(obj, "first")
    assert result == "Success"


def test_deep_get_returns_value_from_nested_object():
    obj = {"first": {"second": "Success"}}
    result = utils.deep_get(obj, "first.second")
    assert result == "Success"


def test_deep_set_returns_mapping():
    result = utils.deep_set({}, "key", "test")
    assert isinstance(result, dict)


def test_deep_set_updates_nested_object():
    result = utils.deep_set({}, "parent.child", "test")
    assert result == {"parent": {"child": "test"}}


def test_iter_get_returns_values():
    data = [{"value": 1}, {"value": 2}, {"value": 3}]
    results = utils.iter_get(data, "value")
    assert results == [1, 2, 3]


def test_iter_get_returns_nested_values():
    data = [
        {"current": {"value": 1}},
        {"current": {"value": 2}},
        {"current": {"value": 3}},
    ]
    results = utils.iter_get(data, "current.value")
    assert results == [1, 2, 3]


def test_iter_setattr_sets_values():
    objs = [mock.Mock(), mock.Mock(), mock.Mock()]
    results = utils.iter_setattr(objs, "test", "success")
    assert all(result.test == "success" for result in results)


def test_merge_combines_dictionaries():
    first_dict = {"a": 1, "b": 2}
    second_dict = {"c": 3, "d": 4}
    result = utils.merge(first_dict, second_dict)
    assert result == {"a": 1, "b": 2, "c": 3, "d": 4}


def test_merge_combines_multiple_dictionaries():
    all_dicts = [
        {"a": 0, "b": 1},
        {"c": 2, "d": 3},
        {"e": 4, "f": 5},
        {"g": 6, "h": 7},
        {"i": 8, "j": 9},
    ]
    result = utils.merge(*all_dicts)
    assert result == {
        "a": 0,
        "b": 1,
        "c": 2,
        "d": 3,
        "e": 4,
        "f": 5,
        "g": 6,
        "h": 7,
        "i": 8,
        "j": 9,
    }


def test_merge_combines_nested_dictionaries():
    first_dict = {"first": {"a": 1, "b": 2}, "second": {"e": 5, "f": 6}}
    second_dict = {"first": {"c": 3, "d": 4}, "second": {"g": 7, "h": 8}}
    result = utils.merge(first_dict, second_dict)
    assert result == {
        "first": {"a": 1, "b": 2, "c": 3, "d": 4},
        "second": {"e": 5, "f": 6, "g": 7, "h": 8},
    }


def test_merge_combines_list_values():
    first_dict = {"a": [1], "b": [3]}
    second_dict = {"a": [2], "b": [4]}
    result = utils.merge(first_dict, second_dict)
    assert result == {"a": [1, 2], "b": [3, 4]}


def test_merge_combines_set_values():
    first_dict = {"a": {1, 2}, "b": {4, 5}}
    second_dict = {"a": {2, 3}, "b": {5, 6}}
    result = utils.merge(first_dict, second_dict)
    assert result == {"a": {1, 2, 3}, "b": {4, 5, 6}}


def test_merge_overwrites_keys_with_subsequent_values():
    first_dict = {"a": 1, "b": 2}
    second_dict = {"b": 3, "c": 4}
    third_dict = {"c": 5, "d": 6}
    fourth_dict = {"d": 7}
    result = utils.merge(
        first_dict, second_dict, third_dict, fourth_dict, overwrite=True
    )
    assert result == {"a": 1, "b": 3, "c": 5, "d": 7}


def test_merge_returns_first_dictionary_if_second_is_none():
    first_dict = {"a": 1, "b": 2}
    second_dict = None
    result = utils.merge(first_dict, second_dict)
    assert result == {"a": 1, "b": 2}


def test_merge_returns_second_dictionary_if_first_is_none():
    first_dict = None
    second_dict = {"c": 3, "d": 4}
    result = utils.merge(first_dict, second_dict)
    assert result == {"c": 3, "d": 4}


def test_remap_keys_returns_new_dictionary():
    data = {"first": 1, "second": 2, "third": 3}
    mapper = {"first": "one", "second": "two", "third": "three"}
    result = utils.remap_keys(data, mapper)
    assert result == {"one": 1, "two": 2, "three": 3}


def test_remove_null_returns_values_which_are_not_none():
    data = {"a": 0, "b": 1, "c": None, "d": 3}
    result = utils.remove_null(data)
    assert list(result.keys()) == ["a", "b", "d"]


def test_remove_null_returns_values_which_are_not_provided():
    data = {"a": 0, "b": 1, "c": None, "d": 3}
    result = utils.remove_null(data, null_values=[0])
    assert list(result.keys()) == ["b", "d"]
