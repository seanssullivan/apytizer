# -*- coding: utf-8 -*-
# src/apytizer/protocols.py

# Standard Library Imports
import enum
import re
from typing import Optional

__all__ = ["Protocol", "get_protocol"]


@enum.unique
class Protocol(str, enum.Enum):
    """Implements standard application layer protocols."""

    HTTP = "http"
    HTTPS = "https"


# ----------------------------------------------------------------------------
# Selectors
# ----------------------------------------------------------------------------
def get_protocol(
    url: str, default: Optional[Protocol] = None
) -> Optional[Protocol]:
    """Get protocol from URL.

    Args:
        url: URL from which to get protocol.
        default (optional): Default protocol. Default ``None``.

    Returns:
        Protocol.

    """
    match = re.match(r"\w+(?=://)", url, re.I)
    result = Protocol(match.group(0)) if match else default
    return result
