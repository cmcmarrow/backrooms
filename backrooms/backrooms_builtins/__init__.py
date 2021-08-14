"""
Copyright 2021 Charles McMarrow

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

This module holds Backrooms built-in scripts.
"""

# built-in
from typing import Tuple

# backrooms
from backrooms.translator import StringHandler
from . import brs_heap
from . import brs_heap_load
from . import brs_hard_vector
from . import brs_utils
from . import brs_variables
from . import brs_variables_load


def get_builtins() -> Tuple[StringHandler, ...]:
    """
    info: Gets Backrooms builtins scripts.
    :return: Tuple[StringHandler, ...]
    """
    return (brs_heap.get_handler(),
            brs_heap_load.get_handler(),
            brs_hard_vector.get_handler(),
            brs_utils.get_handler(),
            brs_variables.get_handler(),
            brs_variables_load.get_handler())
