# -*- coding: utf-8 -*-

# Standard Library Imports
import functools
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping

# Local Imports
from .typing import allinstance


def deep_get(__m: Mapping, keys: str, default: Any = None) -> Any:
    """
    Returns a value from a nested mapping object.

    Args:
        __m: Mapping object.
        keys: String of keys seperated by periods.
        default (optional): Default if value not found.

    Returns:
        Value of key in nested mapping object.

    Raises:
        TypeError: when argument is not an instance of a mapping.

    """

    def _get(data: Mapping, key: str) -> Any:
        return data.get(key, default) if data else None

    if not isinstance(__m, Mapping):
        raise TypeError("must be an instance of a mapping")

    value = functools.reduce(_get, keys.split("."), __m)
    return value


def deep_set(__m: MutableMapping, keys: str, value: Any) -> Dict[str, Any]:
    """
    Sets a key to the provided value in a nested mapping object.

    Args:
        __m: Mapping object.
        keys: String of keys seperated by periods.
        value: Value to which to set the key.

    Returns:
        Updated mapping object.

    Raises:
        TypeError: when argument is not an instance of a mapping.

    """

    if not isinstance(__m, Mapping):
        raise TypeError("must be an instance of a mapping")

    if isinstance(keys, str):
        keys = keys.split(".")

    key = keys[0]

    if len(keys) == 1:
        __m[key] = value

    elif len(keys) > 1:
        __m.setdefault(key, {})
        __m[key] = deep_set(__m[key], keys[1:], value)

    else:
        raise KeyError(keys)

    return __m


def iter_get(__iter: Iterable[Dict[str, Any]], key: str) -> List[Any]:
    """
    Get value for key from each mapping in an iterable object.

    Args:
        __iter: Iterable object containing mappings.
        key: Key for which to retrieve value.

    Raises:
        TypeError: when argument is not an iterable object.
        ValueError: when items are not all mappings.

    """

    if not isinstance(__iter, Iterable):
        raise TypeError("must be an iterable object")

    if not allinstance(__iter, Mapping):
        raise ValueError("all items within iterator must be mappings")

    results = [deep_get(item, key) for item in __iter]
    return results


def pick(__m: Mapping, keys: List[str]) -> Dict[str, Any]:
    """
    Pick multiple values from a mapping.

    Args:
        __m: Mapping object.
        keys: List of keys.

    Returns:
        Dictionary containing the selected key-value pairs.

    Raises:
        TypeError: when argument is not an instance of a mapping.

    """

    if not isinstance(__m, Mapping):
        raise TypeError("must be an instance of a mapping")

    def _last(key: str) -> str:
        return key.split(".")[-1]

    results = {_last(key): deep_get(__m, key) for key in keys}
    return results


def merge(*args: Mapping) -> Dict:
    """
    Combines mapping objects into a single dictionary.

    Args:
        *args: Mapping objects to merge.

    Returns:
        Merged dictionary.

    Raises:
        TypeError: when arguments are not all mappings.

    """

    if not allinstance(args, (Mapping, type(None))):
        raise TypeError("all arguments must be instances of mappings")

    result = {
        key: value
        for mapping in args
        if mapping
        for key, value in mapping.items()
    }
    return result if result else None


def remap_keys(__m: Mapping, key_map: Dict[str, str]) -> Dict[str, Any]:
    """
    Remap mapping object to new keys.

    Note:
        Key-value pairs are dropped if not found in key map.

    Args:
        __m: Mapping object for which keys will be remapped.
        key_map: Dictionary mapping old keys to new ones.

    Returns:
        Remapped dictionary.

    Raises:
        TypeError: when argument is not an instance of a mapping.

    """

    if not isinstance(__m, Mapping):
        raise TypeError("must be an instance of a mapping")

    return {
        key_map[key]: value for key, value in __m.items() if key in key_map
    }


def remove_null(__m: Mapping, null_values: List[Any] = None) -> Dict[str, Any]:
    """
    Remove all null values from a mapping.

    Args:
        __m: Mapping from which to remove null values.
        null_values (optional): Additional values to recognize as null.

    Returns:
        Dictionary without null values.

    Raises:
        TypeError: when argument is not an instance of a mapping.

    """

    if not isinstance(__m, Mapping):
        raise TypeError("must be an instance of a mapping")

    __nulls = null_values or []

    return {
        key: value
        for key, value in __m.items()
        if value is not None and value not in __nulls
    }
