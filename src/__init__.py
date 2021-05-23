# -*- coding: utf-8 -*-

# pylint: skip-file

from .base.adapters import TransportAdapter
from .base.api import BasicAPI as API
from .base.api import SessionAPI as Session
from .base.endpoint import BasicEndpoint as Endpoint
from .base.model import BasicModel as Model


VERSION = (0, 0, 1, 'dev', 0)

__version__ = '.'.join(str(v) for v in VERSION[:2])

__release__ = '.'.join(str(v) for v in VERSION)
