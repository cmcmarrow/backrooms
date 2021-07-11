"""
Copyright 2021 Charles McMarrow
"""

# built-in
from typing import Tuple

# backrooms
from backrooms.translator import StringHandler
from . import variables
from . import heap


def get_builtins() -> Tuple[StringHandler, ...]:
    """
    info: Gets Backrooms builtins modules.
    :return: Tuple[StringHandler, ...]
    """
    return (variables.get_handler(),
            heap.get_handler())
