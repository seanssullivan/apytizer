# -*- coding: utf-8 -*-
# src/apytizer/http_methods.py

# Standard Library Imports
from enum import Enum


class HTTPMethod(Enum):
    """Implements standard HTTP methods."""

    CONNECT = "CONNECT"
    HEAD = "HEAD"
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    OPTIONS = "OPTIONS"
    TRACE = "TRACE"
