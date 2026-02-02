# -*- coding: utf-8 -*-

# Third-Party Imports
import pytest

# Local Imports
try:
    from apytizer.media_types import MediaType

except ImportError:
    from src.apytizer.media_types import MediaType


@pytest.mark.parametrize(
    "value,expected",
    [
        ("application/json", MediaType.APPLICATION_JSON),
        ("image/jpeg", MediaType.IMAGE_JPEG),
        ("text/plain", MediaType.TEXT_PLAIN),
    ],
)
def test_returns_media_type(value: str, expected: MediaType) -> None:
    assert MediaType(value) == expected


@pytest.mark.parametrize(
    "value", ["application/json", "image/jpeg", "text/plain"]
)
def test_media_type_has_type_attribute(value: str) -> None:
    media_type = MediaType(value)
    assert media_type.type == value.split("/")[0]


@pytest.mark.parametrize(
    "value", ["application/json", "image/jpeg", "text/plain"]
)
def test_media_type_has_subtype(value: str) -> None:
    media_type = MediaType(value)
    assert media_type.subtype == value.split("/")[-1]
