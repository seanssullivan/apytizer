# -*- coding: utf-8 -*-
# src/apytizer/sessions/__init__.py

# Standard Library Imports
from typing import Type
from typing import TYPE_CHECKING

# Local Imports
from .abstract_session import *
from .base_session import *

if TYPE_CHECKING:
    from ..engines import AbstractEngine


class sessionmaker:
    """Implements a sessionmaker."""

    def __init__(self, class_: Type[BaseSession] = BaseSession) -> None:
        self._session_type = class_

    def __call__(self, __engine: "AbstractEngine", /) -> BaseSession:
        result = self._session_type(
            adapters=getattr(__engine, "adapters", None),
            cert=getattr(__engine, "cert", None),
            logger=getattr(__engine, "logger", None),
            proxies=getattr(__engine, "proxies", None),
            stream=getattr(__engine, "stream", False),
            verify=getattr(__engine, "verify", True),
        )
        return result
