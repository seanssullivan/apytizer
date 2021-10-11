# -*- coding: utf-8 -*-

# Third-Party Imports
import pytest

# Local Imports
from src.apytizer.base import BasicModel


def test_model_returns_true_when_key_in_state():
    model = BasicModel(
        name='Test Model'
    )
    assert 'name' in model


def test_models_are_equal_when_they_contain_same_state():
    model_one = BasicModel(name='Test Model', status='incomplete')
    model_two = BasicModel(name='Test Model', status='incomplete')
    assert model_one == model_two


def test_models_are_not_equal_when_they_contain_different_states():
    model_one = BasicModel(name='Test Model', status='incomplete')
    model_two = BasicModel(name='Test Model', status='completed')
    assert model_one != model_two


def test_model_state_is_iterable():
    model = BasicModel(
        name='Test Model',
        description='For testing purposes only.',
        status='completed'
    )
    assert dict(model) == {
        'name': 'Test Model',
        'description': 'For testing purposes only.',
        'status': 'completed',
    }


def test_model_gets_attributes_from_state():
    model = BasicModel(name='Test Model', status='completed')
    assert model.status == 'completed'


def test_model_gets_nested_items_from_string_of_keys():
    model = BasicModel(
        name='Test Model',
        description='For testing purposes only.',
        status={
            'progress': 'completed',
        },
    )
    assert model.get('status.progress') == 'completed'
    assert model['status.progress'] == 'completed'


def test_model_gets_nested_items_from_list_of_keys():
    model = BasicModel(
        name='Test Model',
        description='For testing purposes only.',
        status={
            'progress': 'completed',
        },
    )
    assert model.get(['status', 'progress']) == 'completed'
    assert model[['status', 'progress']] == 'completed'


def test_model_gets_nested_items_from_tuple_of_keys():
    model = BasicModel(
        name='Test Model',
        description='For testing purposes only.',
        status={
            'progress': 'completed',
        },
    )
    assert model.get(('status', 'progress')) == 'completed'
    assert model[('status', 'progress')] == 'completed'


def test_get_method_raises_type_error_when_passed_a_dictionary():
    model = BasicModel(
        name='Test Model',
        description='For testing purposes only.',
        status={
            'progress': 'completed',
        },
    )
    with pytest.raises(TypeError):
        model.get({'status': 'progress'})


def test_update_method_changes_model_state():
    model = BasicModel(
        name='Test Model',
        description='For testing purposes only.',
        status='in progress'
    )
    model.update({'status': 'completed'})
    assert model.status == 'completed'


def test_update_does_not_overwrite_initial_context():
    data = {
        'name': 'Test Model',
        'description': 'For testing purposes only.',
        'status': 'in progress',
    }
    model = BasicModel(**data)
    model.update({'status': 'completed'})
    assert model.state.maps[0] == {'status': 'completed'}
    assert model.state.maps[-1] == data


def test_commit_adds_new_context_to_state():
    model = BasicModel(
        name='Test Model',
        description='For testing purposes only.',
        status='in progress'
    )
    model.update({'status': 'completed'})
    model.commit()
    assert not model.state.maps[0]
    assert model.state.maps[1] == {'status': 'completed'}


def test_commit_does_not_add_a_context_when_there_are_no_updates():
    data = {
        'name': 'Test Model',
        'description': 'For testing purposes only.',
        'status': 'in progress',
    }
    model = BasicModel(**data)
    assert not model.state.maps[0]

    model.commit()
    assert len(model.state.maps) == 2
    assert model.state.maps[1] == data
