# -*- coding: utf-8 -*-

# Standard Library Imports
import time
from unittest.mock import Mock

# Third-Party Imports
import pytest

# Local Imports
from src.decorators import decorators


def test_pagination_repeats_request():
    request = Mock()
    request.return_value = {
        'results': 1,
        'total': 2
    }

    decorator = decorators.pagination(
        lambda state, res: { **state, 'results': state.get('results') + res.get('results') if state.get('results') else res.get('results'), 'total': res.get('total')},
        lambda state, res: state.get('results') >= res.get('total')
    )
    wrapper = decorator(request)
    results = [response for response in wrapper()]
    assert request.called == True
    assert len(results) == 2


def test_pagination_updates_parameters():
    request = Mock()
    request.return_value = {
        'results': 1,
        'total': 2
    }

    decorator = decorators.pagination(
        lambda state, res: {
            **state,
            'results': state.get('results') + res.get('results') if state.get('results') else res.get('results'),
            'total': res.get('total'),
            'params': {
                'startAt': state.get('params', {}).get('startAt') + res.get('results') if state.get('params', {}).get('startAt') else res.get('results')
            }
        },
        lambda state, res: state.get('results') >= res.get('total')
    )
    wrapper = decorator(request)
    results = wrapper(params={'startAt': 0})

    next(results)
    request.assert_called_with(params={'startAt': 0})

    next(results)
    request.assert_called_with(params={'startAt': 1})


def test_pagination_updates_data():
    request = Mock()
    request.return_value = {
        'results': 1,
        'total': 2
    }

    decorator = decorators.pagination(
        lambda state, res: {
            **state,
            'results': state.get('results') + res.get('results') if state.get('results') else res.get('results'),
            'total': res.get('total'),
            'data': {
                'startAt': state.get('data', {}).get('startAt') + res.get('results') if state.get('data', {}).get('startAt') else res.get('results')
            }
        },
        lambda state, res: state.get('results') >= res.get('total')
    )
    wrapper = decorator(request)
    results = wrapper(data={'startAt': 0})

    next(results)
    request.assert_called_with(data={'startAt': 0})

    next(results)
    request.assert_called_with(data={'startAt': 1})
