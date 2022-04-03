# -*- coding: utf-8 -*-
# src/apytizer/protocols.py

# Standard Library Imports
from enum import Enum


class Protocol(Enum):
    """Implements standard application layer protocols."""

    HTTP = "http"
    HTTPS = "https"
