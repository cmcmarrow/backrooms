"""
Copyright 2021 Charles McMarrow
"""


# backrooms
from backrooms.translator import StringHandler

VARIABLES_NAME = "vars"

VARIABLES = """
~GET
~SET
"""


def get_handler() -> StringHandler:
    return StringHandler(VARIABLES_NAME, VARIABLES)
