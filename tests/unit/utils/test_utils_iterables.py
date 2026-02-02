# -*- coding: utf-8 -*-

# Third-Party Imports
# import pytest

# Local Imports
try:
    from apytizer import utils

except ImportError:
    from src.apytizer import utils


def test_deep_append_updates_nested_list() -> None:
    list_ = [[0, 1, 2], [3, 4], [6, 7, 8]]
    result = utils.deep_append(list_, 1, 5)
    assert result == [[0, 1, 2], [3, 4, 5], [6, 7, 8]]


def test_deep_append_updates_nested_list_at_first_index() -> None:
    list_ = [[0, 1], [3, 4, 5], [6, 7, 8]]
    result = utils.deep_append(list_, 0, 2)
    assert result == [[0, 1, 2], [3, 4, 5], [6, 7, 8]]


def test_deep_append_updates_nested_list_at_last_index() -> None:
    list_ = [[0, 1, 2], [3, 4, 5], [6, 7]]
    result = utils.deep_append(list_, -1, 8)
    assert result == [[0, 1, 2], [3, 4, 5], [6, 7, 8]]


def test_deep_extend_updates_nested_list() -> None:
    list_ = [[0, 1, 2], [3], [6, 7, 8]]
    result = utils.deep_extend(list_, 1, [4, 5])
    assert result == [[0, 1, 2], [3, 4, 5], [6, 7, 8]]


def test_deep_extend_updates_nested_list_at_first_index() -> None:
    list_ = [[0], [3, 4, 5], [6, 7, 8]]
    result = utils.deep_extend(list_, 0, [1, 2])
    assert result == [[0, 1, 2], [3, 4, 5], [6, 7, 8]]


def test_deep_extend_updates_nested_list_at_last_index() -> None:
    list_ = [[0, 1, 2], [3, 4, 5], [6]]
    result = utils.deep_extend(list_, -1, [7, 8])
    assert result == [[0, 1, 2], [3, 4, 5], [6, 7, 8]]


def test_split_list_returns_grouped_items() -> None:
    list_ = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    results = utils.split_list(list_, 3)
    assert results == [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]


def test_split_list_returns_groups_no_larger_than_provided_size() -> None:
    list_ = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    results = utils.split_list(list_, 3)
    for group in results:
        assert len(group) <= 3
