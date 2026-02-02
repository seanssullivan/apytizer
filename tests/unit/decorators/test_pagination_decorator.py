# -*- coding: utf-8 -*-

# pylint: disable=redefined-outer-name

# Standard Library Imports
from typing import Any
from typing import Callable
from typing import Dict
from unittest.mock import Mock

# Third-Party Imports
import pytest

# Local Imports
try:
    from apytizer.decorators import pagination
    from apytizer import utils

except ImportError:
    from src.apytizer.decorators import pagination
    from src.apytizer import utils


@pytest.fixture
def callback() -> Callable[[Dict[str, Any], Dict[str, Any]], bool]:
    """Callback fixture."""

    def _callback(state: Dict[str, Any], resp: Dict[str, Any]) -> bool:
        """Callback function.

        Args:
            state: State.
            resp: Response.

        Returns:
            Whether pagination is complete.

        """
        results: int = state.get("results", 0)
        total: int = resp.get("total", 0)
        return results >= total

    return _callback


@pytest.fixture
def reducer() -> Callable[[Dict[str, Any], Dict[str, Any]], Dict[str, Any]]:
    """Reducer fixture."""

    def _reducer(
        state: Dict[str, Dict[str, Any]],
        resp: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Reducer function.

        Args:
            state: State.
            resp: Response.

        Returns:
            State.

        """
        results = get_results(state, resp)
        total = get_total(state, resp)

        kwargs: Dict[str, Any] = state["kwargs"]
        num_results: int = resp.get("results", 0)
        result: Dict[str, Any] = {**state, "results": results, "total": total}

        if "data" in kwargs and "startAt" in kwargs["data"]:
            old_start: int = utils.deep_get(state, "kwargs.data.startAt", 0)
            result["kwargs"] = {"data": {"startAt": old_start + num_results}}

        if "params" in kwargs and "startAt" in kwargs["params"]:
            old_start: int = utils.deep_get(state, "kwargs.params.startAt", 0)
            result["kwargs"] = {"params": {"startAt": old_start + num_results}}

        return result

    return _reducer


def test_pagination_repeats_request(
    callback: Callable[[Dict[str, Any], Dict[str, Any]], bool],
    reducer: Callable[[Dict[str, Any], Dict[str, Any]], Dict[str, Any]],
) -> None:
    request = create_mock_request(response={"results": 1, "total": 2})
    decorator = pagination(reducer=reducer, callback=callback)

    wrapper = decorator(request)
    results = [response for response in wrapper()]

    assert request.called == True
    assert len(results) == 2


def test_pagination_updates_parameters(
    callback: Callable[[Dict[str, Any], Dict[str, Any]], bool],
    reducer: Callable[[Dict[str, Any], Dict[str, Any]], Dict[str, Any]],
) -> None:
    request = create_mock_request(response={"results": 1, "total": 2})
    decorator = pagination(reducer=reducer, callback=callback)

    wrapper = decorator(request)
    results = wrapper(params={"startAt": 0})

    next(results)
    request.assert_called_with(params={"startAt": 0})

    next(results)
    request.assert_called_with(params={"startAt": 1})


def test_pagination_updates_data(
    callback: Callable[[Dict[str, Any], Dict[str, Any]], bool],
    reducer: Callable[[Dict[str, Any], Dict[str, Any]], Dict[str, Any]],
) -> None:
    request = create_mock_request(response={"results": 1, "total": 2})
    decorator = pagination(reducer=reducer, callback=callback)

    wrapper = decorator(request)
    results = wrapper(data={"startAt": 0})

    next(results)
    request.assert_called_with(data={"startAt": 0})

    next(results)
    request.assert_called_with(data={"startAt": 1})


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
def create_mock_request(*, response: object) -> Mock:
    mock_request = Mock()
    mock_request.return_value = response
    return mock_request


def get_results(state: Dict[str, Any], resp: Dict[str, Any]) -> int:
    """Get number of results from state and response.

    Args:
        state: State.
        resp: Response.

    Returns:
        Number of results.

    """
    from_state: int = state.get("results", 0)
    from_resp: int = resp.get("results", 0)
    result = from_state + from_resp if from_state else from_resp
    return result


def get_total(_, res: Dict[str, Any]) -> int:
    """Get total from state and response.

    Args:
        _: State.
        res: Response.

    Returns:
        Total.

    """
    result: int = res.get("total", 0)
    return result
