# -*- coding: utf-8 -*-

# Third-Party Imports
import pytest

# Local Imports
from src.apytizer.protocols import Protocol
from src.apytizer.protocols import get_protocol


@pytest.mark.parametrize("url", ["http://testing.com"])
def test_returns_protocol(url: str) -> None:
    result = get_protocol(url)
    assert isinstance(result, Protocol)


@pytest.mark.parametrize("url", ["testing.com"])
def test_returns_none_when_no_protocol_found(url: str) -> None:
    result = get_protocol(url)
    assert result is None


@pytest.mark.parametrize("url", ["testing.com"])
def test_returns_default_protocol_when_provided(url: str) -> None:
    result = get_protocol(url, Protocol.HTTPS)
    assert result == Protocol.HTTPS


@pytest.mark.parametrize("url", ["http://testing.com"])
def test_returns_http_protocol(url: str) -> None:
    result = get_protocol(url)
    assert result == Protocol.HTTP


@pytest.mark.parametrize("url", ["https://testing.com"])
def test_returns_https_protocol(url: str) -> None:
    result = get_protocol(url)
    assert result == Protocol.HTTPS
