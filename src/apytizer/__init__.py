# -*- coding: utf-8 -*-
# src/apytizer/__init__.py

from .adapters import TransportAdapter
from .base import BaseAPI as API
from .base import SessionAPI as Session
from .base import BaseEndpoint as Endpoint
from .base import BaseModel as Model


VERSION = (0, 0, 1, "alpha", 0)

__version__ = ".".join(str(v) for v in VERSION[:2])

__release__ = ".".join(str(v) for v in VERSION)
