# -*- coding: utf-8 -*-
# src/apytizer/http_methods.py

# Standard Library Imports
import enum
from typing import Optional


@enum.unique
class HTTPMethod(str, enum.Enum):
    """Implements standard HTTP methods."""

    @classmethod
    def _missing_(cls, value: object) -> Optional[enum.Enum]:
        result = (
            HTTPMethod(value.upper())
            if (
                isinstance(value, str)
                and not value.isupper()
                and value.upper() in HTTPMethod
            )
            else None
        )
        return result

    CONNECT = "CONNECT"
    HEAD = "HEAD"
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    OPTIONS = "OPTIONS"
    TRACE = "TRACE"
