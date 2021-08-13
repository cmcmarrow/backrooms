"""
Copyright 2021 Charles McMarrow
"""


# backrooms
from backrooms.translator import StringHandler

NAME = "heap_load"

SCRIPT = """
%h_vector
!heap
"""


def get_handler() -> StringHandler:
    """
    info: Gets script handler.
    :return: StringHandler
    """
    return StringHandler(NAME, SCRIPT)
