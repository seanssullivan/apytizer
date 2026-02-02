# -*- coding: utf-8 -*-
# src/apytizer/errors.py


class ConnectionError(Exception):
    """Base class for connection errors."""


class ConnectionNotStarted(ConnectionError):
    """Error raised when connection not started."""


class EndpointError(Exception):
    """Base class for endpoint errors."""


class EndpointNotFound(Exception):
    """Error raised when endpoint not found."""


class RequestError(Exception):
    """Base class for request errors."""


class MethodNotAllowed(RequestError):
    """Error raised when request method not allowed."""


class SessionError(Exception):
    """Base class for session errors."""


class SessionNotStarted(SessionError):
    """Error raised when session not started."""
