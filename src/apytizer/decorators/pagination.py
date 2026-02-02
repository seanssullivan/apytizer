# -*- coding: utf-8 -*-
# src/apytizer/decorators/pagination.py

# Standard Library Imports
import functools
from typing import Any
from typing import Callable
from typing import Dict
from typing import Generator
from typing import TypeVar

__all__ = ["pagination"]


# Custom types
T = TypeVar("T")


class pagination:
    """Implements pagination for requests to an API endpoint.

    Args:
        reducer (Callable): Function to update state from response.
        callback (Callable): Function which returns 'True' when request is
            complete, otherwise returns 'False'. Stop condition must depend
            on either state or response.

    """

    def __init__(
        self,
        reducer: Callable[[Dict[str, Any], Any], Dict[str, Any]],
        callback: Callable[[Dict[str, Any], Any], bool],
    ) -> None:
        self._reducer = reducer
        self._callback = callback

    def __call__(
        self, func: Callable[..., T]
    ) -> Callable[..., Generator[T, None, None]]:
        """Wrap function to handle paginated results.

        Args:
            func: Decorated function.

        Returns:
            Function wrapper.

        """

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Generator[T, None, None]:
            """Wrapper applied to decorated function.

            Args:
                *args: Positional arguments to pass to wrapped function.
                **kwargs: Keyword arguments to pass to wrapped function.

            """
            completed = False
            state: Dict[str, Any] = {"args": args, "kwargs": kwargs}

            while not completed:
                response = func(*state["args"], **state["kwargs"])
                yield response

                state = self._reducer(state, response)
                completed = self._callback(state, response)

        functools.update_wrapper(wrapper, func)
        return wrapper
