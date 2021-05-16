# -*- coding: utf-8 -*-
"""Basic model class.

This module defines the implementation of a basic model class.

"""

# Standard Library Imports
from __future__ import annotations
import functools
from typing import Dict, List, Tuple, Union

# Local Imports
from ..abstracts.model import AbstractModel


class BasicModel(AbstractModel):
    """
    Class for representing a basic object model.
    """

    def __init__(self, data: Dict = None):
        self._state = data or {}

    def __contains__(self, key: str) -> bool:
        return key in self._state

    def __eq__(self, other: AbstractModel) -> bool:
        return dict(other) == dict(self) if isinstance(other, self.__class__) else False

    def __getattr__(self, name: str):
        attr = self.get(name)
        if not attr:
            raise AttributeError
        return attr

    def __getitem__(self, keys: Union[List[str], str, Tuple[str]]):
        return self.get(keys)

    def __iter__(self):
        yield from self._state.items()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._state!s})"

    def get(self, keys: Union[List[str], str, Tuple[str]], default = None):
        """
        Get value for key(s) in local state.

        Function allows lookups even within nested dictionaries. When passed multiple keys,
        either separated by periods or as a list or tuple, the function looks up each key
        in sequence.

        Args:
            keys: Key(s) to use to retrieve value.

        Returns:
            Value for key in state.

        """
        if (isinstance(keys, (list, tuple))) \
            and all(isinstance(k, str) for k in keys):
            keys = '.'.join(keys)

        if not isinstance(keys, str):
            raise TypeError

        return functools.reduce(
            lambda data, key: data.get(key, default) \
                if isinstance(data, dict) \
                else data if data else default,
            keys.split('.'),
            self._state
        )

    def update(self, data: Dict) -> BasicModel:
        """
        Update local state with provided data.

        Args:
            data: Data with which to update local state.

        Returns:
            Updated object instance.

        """
        # TODO: Develop method for recursively updating nested dictionaries in local state.
        self._state.update(data)
        return self
