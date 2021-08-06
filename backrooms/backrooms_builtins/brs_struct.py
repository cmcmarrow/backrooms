"""
Copyright 2021 Charles McMarrow
"""


# backrooms
from backrooms.translator import StringHandler

NAME = "struct"

SCRIPT = """
"""


def get_handler() -> StringHandler:
    """
    info: Gets script handler.
    :return: StringHandler
    """
    return StringHandler(NAME, SCRIPT)
