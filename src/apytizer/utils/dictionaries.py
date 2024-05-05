# -*- coding: utf-8 -*-
# src/apytizer/utils/dictionaries.py

# Standard Library Imports
from collections import ChainMap
import functools
from typing import Any
from typing import Collection
from typing import Dict
from typing import List
from typing import Optional
from typing import TypeVar
from typing import Union

# Local Imports
from .errors import raise_for_instance
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
    "remove_nulls",
]

# Custom types:
T = TypeVar("T")


def deep_get(__d: dict, /, keys: str, default: Optional[object] = None) -> Any:
    """Get value from nested dictionary object.

    Args:
        __d: Mapping object.
        keys: String of keys seperated by periods.
        default (optional): Default if value not found. Default ``None``.

    Returns:
        Value of key in nested dictionary object.

    Raises:
        TypeError: when argument is not an instance of 'dict'.

    """

    def _get(data: dict, key: str) -> Any:
        """Get value of key from dictionary.

        Args:
            data: Dictionary object.
            key: Key for which to get value.

        Returns:
            Value.

        """
        try:
            result = data.get(key, default)
        except AttributeError:  # if data is `None`
            return default
        else:
            return result

    raise_for_instance(__d, (dict, ChainMap))
    raise_for_instance(keys, str)

    value = functools.reduce(_get, keys.split("."), __d)
    return value


def deep_set(__d: dict, /, keys: Union[List[str], str], value: Any) -> dict:
    """Sets key to value in nested dictionary object.

    Args:
        __d: Mapping object.
        keys: Either list of keys, or string of keys seperated by periods.
        value: Value to set for key.

    Returns:
        Updated dictionary object.

    Raises:
        TypeError: when argument is not an instance of 'dict'.

    """
    raise_for_instance(__d, (dict, ChainMap))

    if isinstance(keys, str):
        keys = keys.split(".")

    try:
        key, remaining = keys[0], keys[1:]
        __d[key] = (
            deep_set(__d.get(key) or {}, remaining, value)
            if len(remaining) >= 1
            else value
        )
    except KeyError as error:
        raise KeyError(f"{key}.{error.args[0]}") from error
    except (IndexError, TypeError) as error:
        raise KeyError(keys[0]) from error
    else:
        return __d


def iter_get(__iter: List[dict], /, key: str) -> List[object]:
    """Get value for key from each dictionary in an iterable object.

    Args:
        __iter: Iterable object containing dictionaries.
        key: Key for which to retrieve value.

    Raises:
        TypeError: when argument is not an iterable object.
        ValueError: when not all items are dictionaries.

    """
    raise_for_instance(__iter, list)

    if not allinstance(__iter, dict):
        raise ValueError("iterable object must contain dictionaries")

    results = [deep_get(item, key) for item in __iter]
    return results


def iter_set(__iter: List[dict], /, key: str, value: Any) -> List[dict]:
    """Set value of key on each dictionary in an iterable object.

    Args:
        __iter: Iterable object containing dictionaries.
        key: Key for which to set value.
        value: Value to set.

    Returns:
        List of updated dictionary objects.

    Raises:
        TypeError: when argument is not an iterable object.
        ValueError: when not all items are dictionaries.

    """
    raise_for_instance(__iter, list)

    if not allinstance(__iter, dict):
        raise ValueError("iterable object must contain dictionaries")

    results = [deep_set(item, key, value) for item in __iter]
    return results


def merge(
    *args: Optional[Dict[str, T]], overwrite: bool = True
) -> Optional[Dict[str, T]]:
    """Combines dictionary objects into a single dictionary.

    Args:
        *args: Dictionary objects to merge.
        overwrite (optional): Overwrite existing keys. Default ``True``.

    Returns:
        Merged dictionary.

    Raises:
        TypeError: when arguments are not all dictionaries.
        ValueError: when keys conflict and overwrite is ``False``.

    """
    if not allinstance(args, (dict, type(None))):
        raise TypeError("all arguments must be instances of 'dict'")

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
            overwrite (optional): Overwrite existing keys. Default ``False``.

        Raises:
            ValueError: when keys conflict and overwrite is ``False``.

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
                    location = ".".join(k for k in [*__path, key] if k)
                    message = f"Conflict at {location!s}"
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
    )  # type: dict
    return result if result else None


def omit(__d: dict, /, keys: Collection[str]) -> Dict[str, Any]:
    """Omit multiple key-value pairs from dictionary.

    Args:
        __d: Dictionary object.
        keys: Collection of keys.

    Returns:
        Dictionary without the selected key-value pairs.

    Raises:
        TypeError: when argument is not an instance of 'dict'.

    """
    raise_for_instance(__d, dict)

    # TODO: Add support for omitting key-value pairs from nested dictionaries.
    results = {key: __d[key] for key in __d if key not in keys}
    return results


def pick(__d: dict, /, keys: Collection[str]) -> Dict[str, Any]:
    """Pick multiple values from a dictionary.

    Args:
        __d: Dictionary object.
        keys: Collection of keys.

    Returns:
        Dictionary containing the selected key-value pairs.

    Raises:
        TypeError: when argument is not an instance of 'dict'.

    """
    raise_for_instance(__d, (dict, ChainMap))

    def _last(key: str) -> str:
        return key.split(".")[-1]

    results = {_last(key): deep_get(__d, key) for key in keys}
    return results


def remap_keys(
    __d: dict, /, key_map: Dict[str, str], remove: bool = False
) -> Dict[str, Any]:
    """Remap dictionary object to new keys.

    Args:
        __d: Dictionary object for which keys will be remapped.
        key_map: Dictionary mapping old keys to new ones.
        remove (optional): Whether to drop key-value pairs if key is not found
            in key map. Default ``False``.

    Returns:
        Remapped dictionary.

    Raises:
        TypeError: when argument is not an instance of 'dict'.

    """
    raise_for_instance(__d, dict)

    result = {
        key_map.get(key, key): value
        for key, value in __d.items()
        if key in key_map or remove is False
    }
    return result


def remove_nulls(
    __d: dict, /, null_values: Collection[Any] = None
) -> Dict[str, Any]:
    """Remove all null values from dictionary.

    Args:
        __d: Dictionary from which to remove null values.
        null_values (optional): Additional values to recognize as null.

    Returns:
        Dictionary without null values.

    Raises:
        TypeError: when argument is not an instance of 'dict'.

    """
    raise_for_instance(__d, dict)

    nulls = null_values or []
    result = {
        key: value
        for key, value in __d.items()
        if value is not None and value not in nulls
    }
    return result
