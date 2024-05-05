# -*- coding: utf-8 -*-

# Third-Party Imports
# import pytest

# Local Imports
try:
    from apytizer.connections import AbstractConnection
    from apytizer.engines import BaseEngine
except ImportError:
    from src.apytizer.connections import AbstractConnection
    from src.apytizer.engines import BaseEngine


def test_returns_connection() -> None:
    engine = BaseEngine("testing.com")
    result = engine.connect()
    assert isinstance(result, AbstractConnection)
