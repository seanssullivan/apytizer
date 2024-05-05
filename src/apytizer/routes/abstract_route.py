# -*- coding: utf-8 -*-
# src/apytizer/routes/abstract_route.py

# Standard Library Imports
import abc

__all__ = ["AbstractRoute"]


class AbstractRoute(abc.ABC):
    """Represents an abstract route."""

    @abc.abstractmethod
    def __add__(self, other: object) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def __eq__(self, other: object) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def __hash__(self) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def __truediv__(self, other: object) -> str:
        raise NotImplementedError
