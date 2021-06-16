"""
Copyright 2021 Charles McMarrow
"""

# built-in
from typing import Generator

# backrooms
from .backrooms_error import BackroomsError
from . import conscious as c


class RuleError(BackroomsError):
    pass


# TODO
class Rule:
    def __init__(self):
        pass

    def __call__(self, portal: 'Portal', conscious: c.Conscious) -> Generator[None]:
        raise NotImplementedError()

    def get_start_character(self):
        raise NotImplementedError()


RULES = ()
