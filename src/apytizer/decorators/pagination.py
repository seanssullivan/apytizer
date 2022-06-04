# -*- coding: utf-8 -*-
# src/apytizer/decorators/pagination.py

# Standard Library Imports
import functools
import logging
from typing import Any, Callable, Dict, Generator

__all__ = ["Pagination"]


# Define custom types.
State = Dict[str, Any]
Response = Dict[str, Any]

# Initialize logger.
log = logging.getLogger(__name__)


class Pagination:
    """Implements pagination for requests to an API endpoint.

    Args:
        reducer (Callable): Function to update state from response.
        callback (Callable): Function which returns 'True' when request is
            complete, otherwise returns 'False'. Stop condition must depend
            on either state or response.

    """

    def __init__(
        self,
        reducer: Callable[[State, Response], State],
        callback: Callable[[State, Response], bool],
    ) -> None:
        self.reducer = reducer
        self.callback = callback

    def __call__(self, func: Callable) -> Callable[..., Generator]:
        """Wrap function to handle paginated results.

        Args:
            func: Decorated function.

        Returns:
            Function wrapper.

        """

        @functools.wraps(func)
        def __wrapper(*args, **kwargs) -> Generator[Any, None, None]:
            """Wrapper applied to decorated function.

            Args:
                *args: Positional arguments to pass to wrapped function.
                **kwargs: Keyword arguments to pass to wrapped function.

            """
            completed = False
            state = {
                "params": kwargs.pop("params", None),
                "data": kwargs.pop("data", None),
            }

            while not completed:
                if state.get("params"):
                    kwargs.update({"params": state.get("params")})

                if state.get("data"):
                    kwargs.update({"data": state.get("data")})

                response = func(*args, **kwargs)
                yield response

                state = self.reducer(state, response)
                completed = self.callback(state, response)

        return __wrapper
