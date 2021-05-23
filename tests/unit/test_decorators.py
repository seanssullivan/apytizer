# -*- coding: utf-8 -*-

# pylint: disable=protected-access

# Standard Library Imports
from unittest.mock import Mock

# Local Imports
from src.decorators.pagination import pagination


def test_pagination_repeats_request():
    request = Mock()
    request.return_value = {
        'results': 1,
        'total': 2
    }

    reducer = lambda state, res: {
        **state,
        'results': state.get('results') + res.get('results') if state.get('results') else res.get('results'),
        'total': res.get('total')}
    callback = lambda state, res: state.get('results') >= res.get('total')

    wrapper = pagination(request)
    results = [response for response in wrapper(reducer=reducer, callback=callback)]
    assert request.called == True
    assert len(results) == 2


def test_pagination_updates_parameters():
    request = Mock()
    request.return_value = {
        'results': 1,
        'total': 2
    }

    reducer = lambda state, res: {
            **state,
            'results': state.get('results') + res.get('results') if state.get('results') else res.get('results'),
            'total': res.get('total'),
            'params': {
                'startAt': state.get('params', {}).get('startAt') + res.get('results') if state.get('params', {}).get('startAt') else res.get('results')
            }
        }
    callback = lambda state, res: state.get('results') >= res.get('total')

    wrapper = pagination(request)
    results = wrapper(params={'startAt': 0}, reducer=reducer, callback=callback)

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

    reducer = lambda state, res: {
            **state,
            'results': state.get('results') + res.get('results') if state.get('results') else res.get('results'),
            'total': res.get('total'),
            'data': {
                'startAt': state.get('data', {}).get('startAt') + res.get('results') if state.get('data', {}).get('startAt') else res.get('results')
            }
        }
    callback = lambda state, res: state.get('results') >= res.get('total')

    wrapper = pagination(request)
    results = wrapper(data={'startAt': 0}, reducer=reducer, callback=callback)

    next(results)
    request.assert_called_with(data={'startAt': 0})

    next(results)
    request.assert_called_with(data={'startAt': 1})
