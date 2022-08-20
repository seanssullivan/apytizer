# -*- coding: utf-8 -*-
# src/apytizer/utils/mappings.py

# Standard Library Imports
import functools
from typing import (
    Any,
    Collection,
    Dict,
    Iterable,
    List,
    Mapping,
    MutableMapping,
    Optional,
    Union,
)

# Local Imports
from .typing import allinstance

__all__ = [
    "deep_get",
    "deep_set",
    "iter_get",
    "iter_set",
    "omit",
    "pick",
    "merge",
    "remap_keys",
    "remove_null",
]


def deep_get(__m: Mapping, /, keys: str, default: Any = None) -> Any:
    """Get value from nested mapping object.

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
        """Get value of key from mapping.

        Args:
            data: Mapping object.
            key: Key for which to get value.

        Returns:
            Value.

        """
        try:
            result = data.get(key, default)
        except AttributeError:  # if data is `None`
            return None
        else:
            return result

    if not isinstance(__m, Mapping):
        message = f"expected mapping, got {type(__m)} instead"
        raise TypeError(message)

    if not isinstance(keys, str):
        message = f"expected str, got {keys} instead"
        raise TypeError(message)

    value = functools.reduce(_get, keys.split("."), __m)
    return value


def deep_set(
    __m: MutableMapping, /, keys: Union[List[str], str], value: Any
) -> MutableMapping[str, Any]:
    """Sets key to value in nested mapping object.

    Args:
        __m: Mapping object.
        keys: Either list of keys, or string of keys seperated by periods.
        value: Value to set for key.

    Returns:
        Updated mapping object.

    Raises:
        TypeError: when argument is not an instance of a mapping.

    """
    if not isinstance(__m, Mapping):
        message = f"expected mapping, got {type(__m)} instead"
        raise TypeError(message)

    if isinstance(keys, str):
        keys = keys.split(".")

    try:
        key, remaining = keys[0], keys[1:]
        __m[key] = (
            deep_set(__m.get(key) or {}, remaining, value)
            if len(remaining) >= 1
            else value
        )
    except KeyError as error:
        raise KeyError(f"{key}.{error.args[0]}") from error
    except (IndexError, TypeError) as error:
        raise KeyError(keys[0]) from error
    else:
        return __m


def iter_get(__iter: Iterable[Dict[str, Any]], /, key: str) -> List[Any]:
    """Get value for key from each mapping in an iterable object.

    Args:
        __iter: Iterable object containing mappings.
        key: Key for which to retrieve value.

    Raises:
        TypeError: when argument is not an iterable object.
        ValueError: when not all items are mappings.

    """
    if not isinstance(__iter, Iterable):
        raise TypeError("must be an iterable object")

    if not allinstance(__iter, Mapping):
        raise ValueError("iterable object must contain mappings")

    results = [deep_get(item, key) for item in __iter]
    return results


def iter_set(
    __iter: Iterable[Dict[str, Any]], /, key: str, value: Any
) -> List[Dict[str, Any]]:
    """Set value of key on each mapping in an iterable object.

    Args:
        __iter: Iterable object containing mappings.
        key: Key for which to set value.
        value: Value to set.

    Returns:
        List of updated mapping objects.

    Raises:
        TypeError: when argument is not an iterable object.
        ValueError: when not all items are mappings.

    """
    if not isinstance(__iter, Iterable):
        raise TypeError("must be an iterable object")

    if not allinstance(__iter, Mapping):
        raise ValueError("iterable object must contain mappings")

    results = [deep_set(item, key, value) for item in __iter]
    return results


def merge(
    *args: Optional[Mapping], overwrite: bool = False
) -> Optional[MutableMapping]:
    """Combines mapping objects into a single dictionary.

    Args:
        *args: Mapping objects to merge.
        overwrite (optional): Overwrite existing keys. Default `False`.

    Returns:
        Merged dictionary.

    Raises:
        TypeError: when arguments are not all mappings.
        ValueError: when keys conflict and overwrite is false.

    """
    if not allinstance(args, (Mapping, type(None))):
        raise TypeError("all arguments must be instances of mappings")

    def _merge_dictionaries(
        first: dict,
        second: dict,
        /,
        path: Optional[List[str]] = None,
        overwrite: bool = False,
    ) -> dict:
        """Merge two dictionaries.

        Args:
            first: First dictionary.
            second: Second dictionary.
            path: Path of keys in nested dictionary.
            overwrite (optional): Overwrite existing keys. Default `False`.

        Raises:
            ValueError: when keys conflict and overwrite is false.

        .. _Based On:
            https://stackoverflow.com/questions/7204805/how-to-merge-dictionaries-of-dictionaries.

        """
        __path = [] if path is None else path

        for key in second:
            if key in first:
                if allinstance((first[key], second[key]), dict):
                    first[key] = _merge_dictionaries(
                        first[key],
                        second[key],
                        path=[*__path, str(key)],
                        overwrite=overwrite,
                    )

                elif allinstance((first[key], second[key]), list):
                    first[key] = _merge_lists(first[key], second[key])

                elif allinstance((first[key], second[key]), set):
                    first[key] = _merge_sets(first[key], second[key])

                elif overwrite is True:
                    first[key] = second[key]

                else:
                    path = ".".join(k for k in [*__path, key] if k)
                    message = "Conflict at {path}".format(path=path)
                    raise ValueError(message)

            else:
                first[key] = second[key]

        return first

    def _merge_lists(first: list, second: list) -> list:
        return [*first, *second]

    def _merge_sets(first: set, second: set) -> set:
        return first.union(second)

    func = functools.partial(_merge_dictionaries, overwrite=overwrite)
    result = functools.reduce(
        lambda acc, cur: func(acc, cur) if cur else acc, args, {}
    )  # type: MutableMapping
    return result if result else None


def omit(__m: Mapping, /, keys: Collection[str]) -> Dict[str, Any]:
    """Omit multiple key-value pairs from a mapping.

    Args:
        __m: Mapping object.
        keys: Collection of keys.

    Returns:
        Dictionary without the selected key-value pairs.

    Raises:
        TypeError: when argument is not an instance of a mapping.

    """
    if not isinstance(__m, Mapping):
        message = f"expected mapping, got {type(__m)} instead"
        raise TypeError(message)

    # TODO: Add support for omitting key-value pairs from nested mappings.
    results = {key: __m[key] for key in __m if key not in keys}
    return results


def pick(__m: Mapping, /, keys: Collection[str]) -> Dict[str, Any]:
    """Pick multiple values from a mapping.

    Args:
        __m: Mapping object.
        keys: Collection of keys.

    Returns:
        Dictionary containing the selected key-value pairs.

    Raises:
        TypeError: when argument is not an instance of a mapping.

    """
    if not isinstance(__m, Mapping):
        message = f"expected mapping, got {type(__m)} instead"
        raise TypeError(message)

    def _last(key: str) -> str:
        return key.split(".")[-1]

    results = {_last(key): deep_get(__m, key) for key in keys}
    return results


def remap_keys(
    __m: Mapping, /, key_map: Dict[str, str], remove: bool = False
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
        message = f"expected mapping, got {type(__m)} instead"
        raise TypeError(message)

    result = {
        key_map.get(key, key): value
        for key, value in __m.items()
        if key in key_map or remove is False
    }
    return result


def remove_null(
    __m: Mapping, /, null_values: Collection[Any] = None
) -> Dict[str, Any]:
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
        message = f"expected mapping, got {type(__m)} instead"
        raise TypeError(message)

    __nulls = null_values or []

    result = {
        key: value
        for key, value in __m.items()
        if value is not None and value not in __nulls
    }
    return result
