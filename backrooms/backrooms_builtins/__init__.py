"""
Copyright 2021 Charles McMarrow
"""

# built-in
from typing import Tuple

# backrooms
from backrooms.translator import StringHandler
from . import brs_heap
from . import brs_heap_load
from . import brs_si_vector
from . import brs_si_vector_load
from . import brs_struct
from . import brs_utils
from . import brs_variables
from . import brs_variables_load
from . import brs_vector


def get_builtins() -> Tuple[StringHandler, ...]:
    """
    info: Gets Backrooms builtins modules.
    :return: Tuple[StringHandler, ...]
    """
    return (brs_heap.get_handler(),
            brs_heap_load.get_handler(),
            brs_si_vector.get_handler(),
            brs_si_vector_load.get_handler(),
            brs_struct.get_handler(),
            brs_utils.get_handler(),
            brs_variables.get_handler(),
            brs_variables_load.get_handler(),
            brs_vector.get_handler())
