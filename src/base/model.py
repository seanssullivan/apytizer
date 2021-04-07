# -*- coding: utf-8 -*-

# Standard Library Imports
from __future__ import annotations
from datetime import datetime
from pprint import pformat

# Local Imports
from ..abstracts.model import AbstractModel


class BasicModel(AbstractModel):
    """
    Class for representing a basic object model.
    """

    def __init__(self, data: dict = None):
        self._state = data or {}

    def __repr__(self):
        return f"{self.__class__.__name__}({pformat(self._state)})"

    @property
    def data(self) -> dict:
        return self._state

    # def __getattribute__(self, name: str) -> any:
    #     return self._state[name] if name in self._state else super().__getattribute__(name)

    # def __getitem__(self, key: str) -> any:
    #     return self._state.get(key) if key in self._state else super().__getitem__(key)
