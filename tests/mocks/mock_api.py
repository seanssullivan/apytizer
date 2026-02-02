# -*- coding: utf-8 -*-

# Local Imports
try:
    from apytizer.apis import WebAPI
    from apytizer.engines import AbstractEngine

except ImportError:
    from src.apytizer.apis import WebAPI
    from src.apytizer.engines import AbstractEngine

__all__ = ["MockAPI"]


class MockAPI(WebAPI):
    def __init__(self, __engine: AbstractEngine, /) -> None:
        self._engine = __engine
        self._connection = self._engine.connect()

    @property
    def url(self) -> str:
        """Base URL."""
        return self._engine.url

    def __eq__(self, other: object) -> bool:
        result = (
            other.url.strip("/").lower() == self.url.strip("/").lower()
            if isinstance(other, WebAPI)
            else False
        )
        return result

    def __hash__(self) -> int:
        result = hash(self.url)
        return result
