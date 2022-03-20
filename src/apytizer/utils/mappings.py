# -*- coding: utf-8 -*-
# src/apytizer/utils/mappings.py

# Standard Library Imports
import functools
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping

# Local Imports
from .typing import allinstance

__all__ = [
    "deep_get",
    "deep_set",
    "iter_get",
    "pick",
    "merge",
    "remap_keys",
    "remove_null",
]


def deep_get(__m: Mapping, keys: str, default: Any = None) -> Any:
    """Returns a value from a nested mapping object.

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
    """Sets a key to the provided value in a nested mapping object.

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
    """Get value for key from each mapping in an iterable object.

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
    """Pick multiple values from a mapping.

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


def merge(*args: Mapping, overwrite: bool = False) -> Dict:
    """Combines mapping objects into a single dictionary.

    Args:
        *args: Mapping objects to merge.
        overwrite (optional): Overwrite existing keys. Default false.

    Returns:
        Merged dictionary.

    Raises:
        TypeError: when arguments are not all mappings.
        ValueError: when keys conflict and overwrite is false.

    """
    if not allinstance(args, (Mapping, type(None))):
        raise TypeError("all arguments must be instances of mappings")

    def _merge(a: Mapping, b: Mapping, path=None, overwrite=False) -> Mapping:
        """Merge two mappings.

        Args:
            a: First mapping.
            b: Second mapping.
            path: Path of keys in nested mapping.
            overwrite (optional): Overwrite existing keys. Default false.

        Raises:
            ValueError: when keys conflict and overwrite is false.

        .. _Based On:
            https://stackoverflow.com/questions/7204805/how-to-merge-dictionaries-of-dictionaries.

        """
        __path = [] if path is None else path

        for key in b:
            if key in a:
                if isinstance(a[key], dict) and isinstance(b[key], dict):
                    a[key] = _merge(
                        a[key],
                        b[key],
                        path=__path + [str(key)],
                        overwrite=overwrite,
                    )

                elif isinstance(a[key], list) and isinstance(b[key], list):
                    a[key] = [*a[key], *b[key]]

                elif isinstance(a[key], set) and isinstance(b[key], set):
                    a[key] = a[key].union(b[key])

                elif overwrite:
                    a[key] = b[key]

                else:
                    msg = "Conflict at {path}".format(
                        path=".".join(k for k in [*__path, key] if k)
                    )
                    raise ValueError(msg)

            else:
                a[key] = b[key]

        return a

    result = functools.reduce(
        lambda acc, cur: _merge(acc, cur, overwrite=overwrite) if cur else acc,
        args,
        {},
    )
    return result if result else None


def remap_keys(
    __m: Mapping, key_map: Dict[str, str], remove: bool = False
) -> Dict[str, Any]:
    """Remap mapping object to new keys.

    Args:
        __m: Mapping object for which keys will be remapped.
        key_map: Dictionary mapping old keys to new ones.
        remove (optional): Whether to drop key-value pairs if key is not found
            in key map. Default `False`.

    Returns:
        Remapped dictionary.

    Raises:
        TypeError: when argument is not an instance of a mapping.

    """
    if not isinstance(__m, Mapping):
        raise TypeError("must be an instance of a mapping")

    return {
        key_map.get(key, key): value
        for key, value in __m.items()
        if key in key_map or remove is False
    }


def remove_null(__m: Mapping, null_values: List[Any] = None) -> Dict[str, Any]:
    """Remove all null values from a mapping.

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
