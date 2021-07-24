"""
Copyright 2021 Charles McMarrow
"""

# built-in
import inspect
import sys
import unittest
from typing import Optional, Tuple

# backrooms
import backrooms
from tests import test_files


def full_test(file: str,
              inputs: Optional[Tuple[str, ...]] = None,
              lost_count: int = 10000,
              lost_rule_count: int = 10000,
              error_on_space: bool = True,
              br_builtins: bool = True) -> backrooms.portal.Portal:
    """
    info: Load file and run backrooms silently.
    :param file: str
    :param inputs: Optional[Tuple[str, ...]]
    :param lost_count: int
    :param lost_rule_count: int
    :param error_on_space: bool
    :param br_builtins: bool
    :return: Portal
    """

    if inputs is None:
        inputs = ()

    br = backrooms.backrooms.backrooms_api(test_files.get_path(file),
                                           inputs=inputs,
                                           sys_output=False,
                                           catch_output=True,
                                           lost_count=lost_count,
                                           lost_rule_count=lost_rule_count,
                                           error_on_space=error_on_space,
                                           br_builtins=br_builtins)
    br()
    return br
