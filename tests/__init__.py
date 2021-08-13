"""
Copyright 2021 Charles McMarrow

Holds tests for Backrooms.
"""

# built-in
import inspect
import sys
import unittest

# backrooms
from . import backrooms_tests
from . import conscious_tests
from . import full_test_runner
from . import hard_vector_tests
from . import heap_tests
from . import portal_tests
from . import rooms_tests
from . import rules_tests
from . import stack_tests
from . import test_files
from . import translator_tests
from . import utils_tests
from . import variables_tests

# add all tests to namespace
for module_name, module in vars().copy().items():
    if inspect.ismodule(module) and module_name != "unittest":
        for module_var_name, module_var in vars(module).items():
            if inspect.isclass(module_var) and unittest.TestCase in module_var.__mro__:
                assert not hasattr(sys.modules[__name__], module_var_name)
                setattr(sys.modules[__name__], module_var_name, module_var)
            del module_var_name
            del module_var
    del module_name
    del module


def tests() -> None:
    """
    info: Run tests and write to stdio.
    :return: None
    """
    unittest.main(module=__name__,
                  exit=False)
