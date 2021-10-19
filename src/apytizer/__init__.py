# -*- coding: utf-8 -*-

from .adapters import TransportAdapter
from .base import BasicAPI as API
from .base import SessionAPI as Session
from .base import BasicEndpoint as Endpoint
from .base import BasicModel as Model


VERSION = (0, 0, 1, 'alpha', 0)

__version__ = '.'.join(str(v) for v in VERSION[:2])

__release__ = '.'.join(str(v) for v in VERSION)
