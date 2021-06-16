"""
Copyright 2021 Charles McMarrow
"""

# built-in
import inspect
import sys
import unittest

# backrooms
from . import rooms_tests
from . import translator_tests
from . import stack_tests
from . import conscious_tests
from . import test_files

# add all tests to namespace
for module_name, module in vars().copy().items():
    if inspect.ismodule(module) and module_name != "unittest":
        for module_var_name, module_var in vars(module).items():
            if inspect.isclass(module_var) and unittest.TestCase in module_var.__mro__:
                setattr(sys.modules[__name__], module_var_name, module_var)
            del module_var_name
            del module_var
    del module_name
    del module
