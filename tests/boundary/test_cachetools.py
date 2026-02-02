# -*- coding: utf-8 -*-

# Standard Library Imports
import operator
from typing import Any
from typing import Hashable
from typing import Optional

# Third-Party Imports
from cachetools import Cache
from cachetools import cachedmethod
from cachetools.keys import hashkey
import pytest


class ExampleClass:

    def __init__(self, cache: Optional[Cache[Hashable, Any]] = None) -> None:
        self.cache = cache

    @cachedmethod(operator.attrgetter("cache"), key=hashkey)
    def test(self) -> None: ...


@pytest.mark.skip("fails")
def test_cachedmethod_accepts_none() -> None:
    cls = ExampleClass()
    cls.test()


def test_cachedmethod_accepts_cache_with_length_zero() -> None:
    cls = ExampleClass(cache=Cache(0))
    cls.test()
