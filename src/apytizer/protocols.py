# -*- coding: utf-8 -*-
# src/apytizer/protocols.py

# Standard Library Imports
import enum


@enum.unique
class Protocol(str, enum.Enum):
    """Implements standard application layer protocols."""

    HTTP = "http"
    HTTPS = "https"
