# -*- coding: utf-8 -*-

# pylint: disable=protected-access

# Third-Party Imports
import pytest

# Local Imports
from apytizer.base import BaseState


def test_state_returns_true_when_key_in_state():
    state = BaseState({"test": True})
    assert "test" in state


def test_models_are_equal_when_they_contain_same_state():
    state_one = BaseState({"name": "Test State", "status": "incomplete"})
    state_two = BaseState({"name": "Test State", "status": "incomplete"})
    assert state_one == state_two


def test_states_are_not_equal_when_they_contain_different_key_values():
    state_one = BaseState({"name": "Test State", "status": "incomplete"})
    state_two = BaseState({"name": "Test State", "status": "completed"})
    assert state_one != state_two


def test_state_is_iterable():
    state = BaseState(
        {
            "name": "Test State",
            "description": "For testing purposes only.",
            "status": "completed",
        }
    )
    assert dict(state) == {
        "name": "Test State",
        "description": "For testing purposes only.",
        "status": "completed",
    }


def test_iterating_through_state_includes_updates():
    state = BaseState(
        {
            "name": "Test State",
            "description": "For testing purposes only.",
            "status": "pending",
        }
    )
    state.update(status="completed")
    assert dict(state) == {
        "name": "Test State",
        "description": "For testing purposes only.",
        "status": "completed",
    }


def test_state_gets_nested_items_from_string_of_keys():
    state = BaseState(
        {
            "name": "Test Model",
            "description": "For testing purposes only.",
            "status": {
                "progress": "completed",
            },
        }
    )
    assert state["status.progress"] == "completed"


def test_getitem_method_raises_type_error_when_passed_a_dictionary():
    state = BaseState(
        {
            "name": "Test Model",
            "description": "For testing purposes only.",
            "status": {
                "progress": "completed",
            },
        }
    )
    with pytest.raises(TypeError):
        state[{"status": "progress"}]


def test_update_method_changes_state():
    state = BaseState(
        {
            "name": "Test Model",
            "description": "For testing purposes only.",
            "status": "in progress",
        }
    )
    state.update({"status": "completed"})
    assert state["status"] == "completed"


def test_update_does_not_overwrite_default_context():
    data = {
        "name": "Test Model",
        "description": "For testing purposes only.",
        "status": "in progress",
    }
    state = BaseState(default=data)
    state.update({"status": "completed"})
    assert state._state.maps[0] == {"status": "completed"}
    assert state._state.maps[-1] == data


def test_save_adds_new_context_to_state():
    state = BaseState(
        default={
            "name": "Test Model",
            "description": "For testing purposes only.",
            "status": "in progress",
        }
    )
    state.update({"status": "completed"})
    state.save()
    assert not state._state.maps[0]
    assert state._state.maps[1] == {"status": "completed"}


def test_save_does_not_add_a_context_when_there_are_no_updates():
    data = {
        "name": "Test Model",
        "description": "For testing purposes only.",
        "status": "in progress",
    }
    state = BaseState(default=data)
    assert not state._state.maps[0]

    state.save()
    assert len(state._state.maps) == 2
    assert state._state.maps[1] == data
