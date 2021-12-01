# -*- coding: utf-8 -*-
"""Basic model class.

This module defines the implementation of a basic model class.

"""

# Standard Library Imports
from __future__ import annotations
import collections
import logging
from typing import Any, Mapping

# Local Imports
from .. import abstracts
from .. import utils


# Initialize logger.
log = logging.getLogger(__name__)


class BasicModel(abstracts.AbstractModel):
    """
    Class for representing a basic object model.

    Args:
        **kwargs: Data with which to set model state.

    """

    state: collections.ChainMap

    def __init__(self, **kwargs):
        self.state = collections.ChainMap({}, kwargs)

    def __contains__(self, key: str) -> bool:
        return key in self.state

    def __eq__(self, other: abstracts.AbstractModel) -> bool:
        return (
            dict(other) == dict(self)
            if isinstance(other, self.__class__)
            else False
        )

    def __getattr__(self, name: str) -> Any:
        """
        Get attribute from local state.

        Args:
            name: Name of attribute.

        Returns:
            Value of attribute in state.

        """

        attr = self.state.get(name)
        if not attr:
            cls = self.__class__.__name__
            message = f"type object '{cls!s}' has no attribute '{attr!s}'"
            raise AttributeError(message)

        return attr

    def __getitem__(self, key: str) -> Any:
        """
        Get item from local state.

        Function allows lookups even within nested dictionaries. When passed
        multiple keys, separated by periods, the function looks up each key
        in sequence.

        Args:
            key: Key(s) to use to retrieve value.

        Returns:
            Value for key in state.

        """

        if not isinstance(key, str):
            raise TypeError('argument must be a string')

        value = utils.deep_get(self.state, key)
        return value

    def __iter__(self):
        yield from self.state.items()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.state!s})"

    def commit(self) -> None:
        """
        Commits changes to local state.

        """

        if self.state.maps[0]:
            self.state = self.state.new_child()

    def update(self, __m: Mapping = None, **kwargs) -> None:
        """
        Update local state of model with provided data.

        Args:
            __m (optional): Mapping with which to update local state.
            **kwargs: Data with which to update local state.

        """

        # TODO: Develop method for recursively updating nested dictionaries in local state.
        if __m:
            self.state.update(__m, **kwargs)
        else:
            self.state.update(**kwargs)

        return self

    def rollback(self) -> None:
        """
        Rollback changes to local state.

        """

        self.state.clear()
