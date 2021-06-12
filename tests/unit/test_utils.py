# -*- coding: utf-8 -*-

# pylint: disable=protected-access

# Local Imports
from src.base.utils import merge


def test_merge_combines_dictionaries():
    first_dict = {'a': 1, 'b': 2}
    second_dict = {'c': 3, 'd': 4}
    result = merge(first_dict, second_dict)
    assert result == {'a': 1, 'b': 2, 'c': 3, 'd': 4}


def test_merge_combines_multiple_dictionaries():
    all_dicts = [
        {'a': 0, 'b': 1},
        {'c': 2, 'd': 3},
        {'e': 4, 'f': 5},
        {'g': 6, 'h': 7},
        {'i': 8, 'j': 9},
    ]
    result = merge(*all_dicts)
    assert result == {
        'a': 0,
        'b': 1,
        'c': 2,
        'd': 3,
        'e': 4,
        'f': 5,
        'g': 6,
        'h': 7,
        'i': 8,
        'j': 9,
    }


def test_merge_overwrites_keys_with_subsequent_values():
    first_dict = {'a': 1, 'b': 2}
    second_dict = {'b': 3, 'c': 4}
    third_dict = {'c': 5, 'd': 6}
    fourth_dict = {'d': 7}
    result = merge(first_dict, second_dict, third_dict, fourth_dict)
    assert result == {'a': 1, 'b': 3, 'c': 5, 'd': 7}


def test_merge_combined_two_dictionaries():
    first_dict = {'a': 1, 'b': 2}
    second_dict = {'c': 3, 'd': 4}
    result = merge(first_dict, second_dict)
    assert result == {'a': 1, 'b': 2, 'c': 3, 'd': 4}


def test_merge_returns_first_dictionary_if_second_is_none():
    first_dict = {'a': 1, 'b': 2}
    second_dict = None
    result = merge(first_dict, second_dict)
    assert result == {'a': 1, 'b': 2}


def test_merge_returns_second_dictionary_if_first_is_none():
    first_dict = None
    second_dict = {'c': 3, 'd': 4}
    result = merge(first_dict, second_dict)
    assert result == {'c': 3, 'd': 4}
