# -*- coding: utf-8 -*-
# src/apytizer/repositories/base_repository.py
"""Base repository class.

This module defines a base implementation of a repository class.

"""

# Standard Library Imports
from typing import Any
from typing import List
from typing import Set
from typing import TYPE_CHECKING

# Local Imports
from .abstract_repository import AbstractRepository

if TYPE_CHECKING:
    from ..managers import AbstractManager
    from ..models import AbstractModel

__all__ = ["BaseRepository"]


class BaseRepository(AbstractRepository):
    """Implements a base repository.

    Args:
        manager: Manager.
        objects (optional): Objects to include in repository.

    """

    def __init__(
        self,
        manager: AbstractManager,
        objects: List[AbstractModel] = None,
    ) -> None:
        self._manager = manager
        self._objects = set(objects or [])  # type: Set[AbstractModel]

    @property
    def objects(self) -> List[AbstractModel]:
        """Objects in repository."""
        result = list(self._objects)
        return result

    def add(self, obj: AbstractModel) -> None:
        """Add an object to the repository.

        Args:
            obj: Object to add.

        """
        self._objects.add(obj)

    def get(self, ref: Any) -> AbstractModel:
        """Get an object from the repository.

        Args:
            ref: Reference to object.

        Returns:
            Object.

        """
        try:
            result = next(obj for obj in self.objects if obj.reference == ref)
        except StopIteration:
            result = self._manager.read(ref)
            self._objects.add(result)

        return result

    def remove(self, obj: AbstractModel) -> None:
        """Remove an object from the repository.

        Args:
            obj: Object to remove.

        """
        self._manager.delete(obj)
        self._objects.discard(obj)

    def commit(self) -> None:
        """Commit changes to objects in the repository."""
        raise NotImplementedError

    def rollback(self) -> None:
        """Rollback changes to objects in the repository."""
        raise NotImplementedError
