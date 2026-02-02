# -*- coding: utf-8 -*-

# Standard Library Imports
from unittest.mock import Mock
from unittest.mock import create_autospec

# Local Imports
try:
    from apytizer.engines import HTTPEngine
    from apytizer.connections import HttpConnection

except ImportError:
    from src.apytizer.engines import HTTPEngine
    from src.apytizer.connections import HttpConnection

__all__ = ["MockEngine"]


class MockEngine(HTTPEngine):
    def connect(self) -> Mock:
        """Establish mock connection."""
        return create_autospec(HttpConnection)
