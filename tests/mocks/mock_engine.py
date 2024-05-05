# -*- coding: utf-8 -*-

# Standard Library Imports
from unittest.mock import Mock

# Local Imports
try:
    from apytizer.engines import BaseEngine
except ImportError:
    from src.apytizer.engines import BaseEngine

__all__ = ["MockEngine"]


class MockEngine(BaseEngine):
    def connect(self) -> Mock:
        """Establish mock connection."""
        return Mock()
