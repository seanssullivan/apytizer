# -*- coding: utf-8 -*-

# Standard Library Imports
from typing import Dict


def merge(*args: Dict) -> Dict:
    """
    Combines dictionaries.

    Args:
        *args: Dictionaries to merge.

    Returns:
        Merged dictionary.

    """
    result = {k: v for dictionary in args if dictionary for k, v in dictionary.items()}
    return result if result else None
