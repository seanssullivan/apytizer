# -*- coding: utf-8 -*-

# Standard Library Imports
from typing import Any
from unittest.mock import Mock

# Third-Party Imports
from requests import Request

# Local Imports
try:
    from apytizer.sessions import AbstractSession

except ImportError:
    from src.apytizer.sessions import AbstractSession

__all__ = ["MockSession"]


class MockSession(AbstractSession):
    def __init__(self, **_) -> None:
        self.mock = Mock()

    def start(self) -> None:
        """Starts the session."""
        pass

    def close(self) -> None:
        """Stops the session."""
        pass

    def mount(self, *args: Any, **kwargs: Any) -> None:
        """Mount adapter."""
        pass

    def send(self, request: Request, **kwargs: Any):
        """Send an HTTP request."""
        return self.mock(request, **kwargs)
