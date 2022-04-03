# -*- coding: utf-8 -*-

# Third-Party Imports
import pytest

# Local Imports
from apytizer.models import BaseModel
from apytizer.models.base_model import _State


# --------------------------------------------------------------------------------
# Tests for BaseModel Class
# --------------------------------------------------------------------------------
def test_model_returns_true_when_key_in_state():
    model = BaseModel(name="Test Model")
    assert "name" in model


def test_model_is_iterable():
    model = BaseModel(
        name="Test Model",
        description="For testing purposes only.",
        status="completed",
    )
    assert dict(model) == {
        "name": "Test Model",
        "description": "For testing purposes only.",
        "status": "completed",
    }


def test_model_gets_attributes_from_state():
    model = BaseModel(name="Test Model", status="completed")
    assert model.status == "completed"


def test_model_gets_nested_items_from_string_of_keys():
    model = BaseModel(
        name="Test Model",
        description="For testing purposes only.",
        status={
            "progress": "completed",
        },
    )
    assert model["status.progress"] == "completed"


def test_get_method_raises_type_error_when_passed_a_dictionary():
    model = BaseModel(
        name="Test Model",
        description="For testing purposes only.",
        status={
            "progress": "completed",
        },
    )
    with pytest.raises(TypeError):
        model[{"status": "progress"}]


def test_update_method_changes_model_state():
    model = BaseModel(
        name="Test Model",
        description="For testing purposes only.",
        status="in progress",
    )
    model.update({"status": "completed"})
    assert model.status == "completed"


# --------------------------------------------------------------------------------
# Tests for _State Class
# --------------------------------------------------------------------------------
def test_state_returns_true_when_key_in_state():
    state = _State({"test": True})
    assert "test" in state


def test_models_are_equal_when_they_contain_same_state():
    state_one = _State({"name": "Test State", "status": "incomplete"})
    state_two = _State({"name": "Test State", "status": "incomplete"})
    assert state_one == state_two


def test_states_are_not_equal_when_they_contain_different_key_values():
    state_one = _State({"name": "Test State", "status": "incomplete"})
    state_two = _State({"name": "Test State", "status": "completed"})
    assert state_one != state_two


def test_state_is_iterable():
    state = _State(
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
    state = _State(
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


def test_gets_nested_items_from_string_of_keys():
    state = _State(
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
    state = _State(
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


def test_sets_nested_items_from_string_of_keys():
    state = _State(
        {
            "name": "Test Model",
            "description": "For testing purposes only.",
            "status": None,
        }
    )
    state["status.progress"] = "completed"
    assert dict(state) == {
        "name": "Test Model",
        "description": "For testing purposes only.",
        "status": {
            "progress": "completed",
        },
    }


def test_update_method_changes_state():
    state = _State(
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
    state = _State(default=data)
    state.update({"status": "completed"})
    assert state._state.maps[0] == {"status": "completed"}
    assert state._state.maps[-1] == data


def test_save_adds_new_context_to_state():
    state = _State(
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
    state = _State(default=data)
    assert not state._state.maps[0]

    state.save()
    assert len(state._state.maps) == 2
    assert state._state.maps[1] == data
