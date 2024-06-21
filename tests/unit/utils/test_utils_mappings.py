# -*- coding: utf-8 -*-

# Third-Party Imports
import pytest

# Local Imports
try:
    from apytizer import utils

except ImportError:
    from src.apytizer import utils


def test_deep_get_returns_value() -> None:
    dict_ = {"first": "success"}
    result = utils.deep_get(dict_, "first")
    assert result == "success"


def test_deep_get_returns_value_from_nested_dictionary() -> None:
    dict_ = {"first": {"second": "success"}}
    result = utils.deep_get(dict_, "first.second")
    assert result == "success"


def test_deep_set_returns_dictionary() -> None:
    result = utils.deep_set({}, "key", "test")
    assert isinstance(result, dict)


def test_deep_set_updates_nested_dictionary() -> None:
    dict_ = {"parent": {"child": {"name": "failure"}}}
    result = utils.deep_set(dict_, "parent.child.name", "success")
    assert result == {"parent": {"child": {"name": "success"}}}


def test_deep_set_creates_nested_dictionaries() -> None:
    result = utils.deep_set({}, "parent.child.name", "success")
    assert result == {"parent": {"child": {"name": "success"}}}


def test_deep_set_replaces_none_with_dictionary() -> None:
    dict_ = {"parent": {"child": None}}
    result = utils.deep_set(dict_, "parent.child.name", "success")
    assert result == {"parent": {"child": {"name": "success"}}}


@pytest.mark.parametrize("value", ["test", 1.0, [1, 2, 3]])
def test_raises_key_error(value) -> None:
    dict_ = {"parent": {"child": value}}
    with pytest.raises(KeyError, match="parent.child"):
        utils.deep_set(dict_, "parent.child.name", "success")


def test_iter_get_returns_values() -> None:
    data = [{"value": 1}, {"value": 2}, {"value": 3}]
    results = utils.iter_get(data, "value")
    assert results == [1, 2, 3]


def test_iter_get_returns_nested_values() -> None:
    data = [
        {"current": {"value": 1}},
        {"current": {"value": 2}},
        {"current": {"value": 3}},
    ]
    results = utils.iter_get(data, "current.value")
    assert results == [1, 2, 3]


def test_iter_set_updates_mappings() -> None:
    data = [{"value": 1}, {"value": 2}, {"value": 3}]
    results = utils.iter_set(data, "value", "success")
    assert results == [
        {"value": "success"},
        {"value": "success"},
        {"value": "success"},
    ]


def test_iter_set_updates_nested_mappings() -> None:
    data = [
        {"data": {"value": 1}},
        {"data": {"value": 2}},
        {"data": {"value": 3}},
    ]
    results = utils.iter_set(data, "data.value", "success")
    assert results == [
        {"data": {"value": "success"}},
        {"data": {"value": "success"}},
        {"data": {"value": "success"}},
    ]


def test_merge_combines_dictionaries() -> None:
    first_dict = {"a": 1, "b": 2}
    second_dict = {"c": 3, "d": 4}
    result = utils.merge(first_dict, second_dict)
    assert result == {"a": 1, "b": 2, "c": 3, "d": 4}


def test_merge_combines_multiple_dictionaries() -> None:
    all_dicts = [{"a": 0, "b": 1}, {"c": 2, "d": 3}, {"e": 4, "f": 5}]
    result = utils.merge(*all_dicts)
    assert result == {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5}


def test_merge_combines_nested_dictionaries() -> None:
    first_dict = {"first": {"a": 1, "b": 2}, "second": {"e": 5, "f": 6}}
    second_dict = {"first": {"c": 3, "d": 4}, "second": {"g": 7, "h": 8}}
    result = utils.merge(first_dict, second_dict)
    assert result == {
        "first": {"a": 1, "b": 2, "c": 3, "d": 4},
        "second": {"e": 5, "f": 6, "g": 7, "h": 8},
    }


def test_merge_combines_list_values() -> None:
    first_dict = {"a": [1], "b": [3]}
    second_dict = {"a": [2], "b": [4]}
    result = utils.merge(first_dict, second_dict)
    assert result == {"a": [1, 2], "b": [3, 4]}


def test_merge_combines_set_values() -> None:
    first_dict = {"a": {1, 2}, "b": {4, 5}}
    second_dict = {"a": {2, 3}, "b": {5, 6}}
    result = utils.merge(first_dict, second_dict)
    assert result == {"a": {1, 2, 3}, "b": {4, 5, 6}}


def test_merge_overwrites_keys_with_subsequent_values() -> None:
    first_dict = {"a": 1, "b": 2}
    second_dict = {"b": 3, "c": 4}
    third_dict = {"c": 5, "d": 6}
    fourth_dict = {"d": 7}
    result = utils.merge(
        first_dict, second_dict, third_dict, fourth_dict, overwrite=True
    )
    assert result == {"a": 1, "b": 3, "c": 5, "d": 7}


def test_merge_returns_first_dictionary_if_second_is_none() -> None:
    first_dict = {"a": 1, "b": 2}
    second_dict = None
    result = utils.merge(first_dict, second_dict)
    assert result == {"a": 1, "b": 2}


def test_merge_returns_second_dictionary_if_first_is_none() -> None:
    first_dict = None
    second_dict = {"c": 3, "d": 4}
    result = utils.merge(first_dict, second_dict)
    assert result == {"c": 3, "d": 4}


def test_omit_removes_key_value_pairs() -> None:
    data = {"first": 1, "second": 2, "third": 3}
    result = utils.omit(data, ["first", "second"])
    assert result == {"third": 3}


def test_pick_returns_key_value_pairs() -> None:
    data = {"first": 1, "second": 2, "third": 3}
    result = utils.pick(data, ["first", "second"])
    assert result == {"first": 1, "second": 2}


def test_remap_keys_returns_new_dictionary() -> None:
    data = {"first": 1, "second": 2, "third": 3}
    mapper = {"first": "one", "second": "two", "third": "three"}
    result = utils.remap_keys(data, mapper)
    assert result == {"one": 1, "two": 2, "three": 3}


def test_remove_null_returns_values_which_are_not_none() -> None:
    data = {"a": 0, "b": 1, "c": None, "d": 3}
    result = utils.remove_nulls(data)
    assert list(result.keys()) == ["a", "b", "d"]


def test_remove_null_returns_values_which_are_not_provided() -> None:
    data = {"a": 0, "b": 1, "c": None, "d": 3}
    result = utils.remove_nulls(data, null_values=[0])
    assert list(result.keys()) == ["b", "d"]
