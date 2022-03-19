# -*- coding: utf-8 -*-

# Third-Party Imports
import pytest

# Local Imports
from apytizer.base import BaseModel


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
