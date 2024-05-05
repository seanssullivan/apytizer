# -*- coding: utf-8 -*-
# src/apytizer/errors.py


class ConnectionError(Exception):
    """Base class for connection errors."""


class ConnectionNotStarted(ConnectionError):
    """Error raised when connection not started."""


class RequestError(Exception):
    """Base class for request errors."""


class MethodNotAllowed(RequestError):
    """Error raised when request method not allowed."""
