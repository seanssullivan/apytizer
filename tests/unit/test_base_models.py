# -*- coding: utf-8 -*-

# pylint: disable=protected-access

# Standard Library Imports
from unittest.mock import Mock

# Third-Party Imports
import pytest

# Local Imports
from src.apytizer.base import BasicModel


def test_model_returns_true_when_key_in_state():
    state = {
        'name': "Test Model"
    }
    model = BasicModel(state)
    assert 'name' in model


def test_models_are_equal_when_they_contain_same_state():
    state = {
        'name': "Test Model",
        'status': "incomplete",
    }
    model_one = BasicModel(state)
    model_two = BasicModel(state)
    assert model_one == model_two


def test_models_are_not_equal_when_they_contain_different_states():
    model_one = BasicModel({
        'name': "Test Model",
        'status': "incomplete",
    })
    model_two = BasicModel({
        'name': "Test Model",
        'status': 'completed',
    })
    assert model_one != model_two


def test_model_state_is_iterable():
    state = {
        'name': "Test Model",
        'description': "For testing purposes only.",
        'status': 'completed',
    }
    model = BasicModel(state)
    assert dict(model) == state


def test_model_gets_attributes_from_state():
    state = {
        'name': "Test Model",
        'status': 'completed',
    }
    model = BasicModel(state)
    assert model.status == 'completed'


def test_model_gets_nested_items_from_string_of_keys():
    state = {
        'name': "Test Model",
        'description': "For testing purposes only.",
        'status': {
            'progress': 'completed',
        },
    }
    model = BasicModel(state)
    assert model.get('status.progress') == 'completed'
    assert model['status.progress'] == 'completed'


def test_model_gets_nested_items_from_list_of_keys():
    state = {
        'name': "Test Model",
        'description': "For testing purposes only.",
        'status': {
            'progress': 'completed',
        },
    }
    model = BasicModel(state)
    assert model.get(['status', 'progress']) == 'completed'
    assert model[['status', 'progress']] == 'completed'


def test_model_gets_nested_items_from_tuple_of_keys():
    state = {
        'name': "Test Model",
        'description': "For testing purposes only.",
        'status': {
            'progress': 'completed',
        },
    }
    model = BasicModel(state)
    assert model.get(('status', 'progress')) == 'completed'
    assert model[('status', 'progress')] == 'completed'


def test_model_raises_type_error_when_get_is_passed_a_dictionary():
    state = {
        'name': "Test Model",
        'description': "For testing purposes only.",
        'status': {
            'progress': 'completed',
        },
    }
    model = BasicModel(state)
    with pytest.raises(TypeError):
        model.get({'status': 'progress'})


def test_update_method_changes_model_state():
    state = {
        'name': "Test Model",
        'description': "For testing purposes only.",
        'status': "in progress",
    }
    model = BasicModel(state)
    model.update({'status': 'completed'})
    assert model.status == 'completed'
