# -*- coding: utf-8 -*-

# Local Imports
try:
    from apytizer.routes import Route
except ImportError:
    from src.apytizer.routes import Route


def test_routes_are_equal_when_segments_are_the_same() -> None:
    route1 = Route("first/second/third/")
    route2 = Route("/first/second/third")
    assert route1 == route2


def test_routes_are_not_equal_when_segments_are_different() -> None:
    route1 = Route("first/second/third")
    route2 = Route("second/third/fourth")
    assert route1 != route2


def test_returns_true_when_route_equal_to_string() -> None:
    route = Route("first/second/third/")
    result = route == "/first/second/third"
    assert result is True


def test_returns_false_when_route_not_equal_to_string() -> None:
    route = Route("first/second/third")
    result = route == "second/third/fourth"
    assert result is False


def test_returns_true_when_only_difference_is_placeholder_text() -> None:
    route = Route("first/{}/second/")
    result = route == "/first/test/second"
    assert result is True


def test_returns_false_when_difference_is_not_placeholder_text() -> None:
    route = Route("first/{}/second/")
    result = route == "/first/test/second/third"
    assert result is False


def test_returns_number_of_segments_in_route() -> None:
    route = Route("first/second/third")
    result = len(route)
    assert result == 3


def test_returns_true_when_route_contains_more_segments() -> None:
    route1 = Route("first/second/third")
    route2 = Route("first/second")
    result = route1 > route2
    assert result is True


def test_returns_true_when_route_contains_fewer_segments() -> None:
    route1 = Route("first/second")
    route2 = Route("first/second/third")
    result = route1 < route2
    assert result is True
