# -*- coding: utf-8 -*-

# Standard Library Imports
import functools
from typing import Any, Dict, List, Mapping, MutableMapping


def deep_get(__m: Mapping, keys: str, default: Any = None) -> Any:
    """
    Returns a value from a nested mapping object.

    Args:
        __m: Mapping object.
        keys: String of keys seperated by periods.
        default (optional): Default if value not found.

    Returns:
        Value of key in nested mapping object.

    """

    def _get(data: Mapping, key: str) -> Any:
        return data.get(key, default) if data else None

    if not isinstance(__m, Mapping):
        raise TypeError('must be an instance of a mapping')

    value = functools.reduce(_get, keys.split("."), __m)
    return value


def deep_set(
    __m: MutableMapping, keys: str, value: Any
) -> Dict[str, Any]:
    """
    Sets a key to the provided value in a nested mapping object.

    Args:
        __m: Mapping object.
        keys: String of keys seperated by periods.
        value: Value to which to set the key.

    Returns:
        Updated mapping object.

    """

    if isinstance(keys, str):
        keys = keys.split('.')

    key = keys[0]

    if len(keys) == 1:
        __m[key] = value

    elif len(keys) > 1:
        __m.setdefault(key, {})
        __m[key] = deep_set(__m[key], keys[1:], value)

    else:
        raise KeyError(keys)

    return __m


def pick(__m: Mapping, keys: List[str]) -> Dict[str, Any]:
    """
    Pick multiple values from a mapping.

    Args:
        __m: Mapping object.
        keys: List of keys.

    Returns:
        Dictionary containing the selected key-value pairs.

    """
    def _last(key: str) -> str:
        return key.split('.')[-1]

    results = {_last(key): deep_get(__m, key) for key in keys}
    return results


def merge(*args: Mapping) -> Dict:
    """
    Combines mapping objects into a single dictionary.

    Args:
        *args: Mapping objects to merge.

    Returns:
        Merged dictionary.

    """

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

    """

    return {
        key_map[key]: value for key, value in __m.items() if key in key_map
    }


def remove_null(__m: Mapping) -> Dict[str, Any]:
    """
    Remove all null values from a mapping.

    Args:
        __m: Mapping from which to remove null values.

    Returns:
        Dictionary without null values.

    """

    return {key: value for key, value in __m.items() if value}
