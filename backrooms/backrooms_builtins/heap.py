"""
Copyright 2021 Charles McMarrow
"""


# backrooms
from backrooms.translator import StringHandler

HEAP_NAME = "heap"

HEAP = """
# -> Pointer [str]
~NEW
# Pointer [str] ->                                                       
~FREE
# Pointer [str] -> Item[object]
~GET
# Item [object] Pointer [str] ->
~SET
"""


def get_handler() -> StringHandler:
    return StringHandler(HEAP_NAME, HEAP)
