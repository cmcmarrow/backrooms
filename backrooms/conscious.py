"""
Copyright 2021 Charles McMarrow

This script holds a simple conscious "thread" data structure.
A conscious holds it own state.
    * work stack
    * function ret stack
    * 10 work registers
    * an error register
    * PC registers
"""


# built-in
from typing import Dict, Tuple, Union, Type

# backrooms
from . import stack


# Stacks
WORK_STACK = "WORK_STACK"
FUNCTION_STACK = "FUNCTION_RET_STACK"

# Normal Registers
R0 = "R0"
R1 = "R1"
R2 = "R2"
R3 = "R3"
R4 = "R4"
R5 = "R5"
R6 = "R6"
R7 = "R7"
R8 = "R8"
R9 = "R9"

# Program Counter Registers
PC_X = "PC_X"
PC_Y = "PC_Y"
PC_FLOOR = "PC_FLOOR"

# Program Counter Vector Registers
PC_V_X = "PC_V_X"
PC_V_Y = "PC_V_Y"
PC_V_FLOOR = "PC_V_FLOOR"

# Thread ID
ID = "ID"

# State
ALIVE = "ALIVE"
HALT = "HALT"


def _to_int(obj: Union[int, str, Type[stack.StackFrame], Type[stack.StackBottom], None]) -> int:
    if isinstance(obj, str):
        return len(obj)
    elif obj is None:
        return 0
    elif obj is stack.StackFrame:
        return 0
    elif obj is stack.StackBottom:
        return 0
    return obj


def _clear(conscious: 'Conscious') -> bool:
    return True


def _less_than_zero(conscious: 'Conscious') -> bool:
    return _to_int(conscious[WORK_STACK].peak()) < 0


def _greater_than_zero(conscious: 'Conscious') -> bool:
    return _to_int(conscious[WORK_STACK].peak()) > 0


def _zero(conscious: 'Conscious') -> bool:
    return _to_int(conscious[WORK_STACK].peak()) == 0


def _not_zero(conscious: 'Conscious') -> bool:
    return _to_int(conscious[WORK_STACK].peak()) != 0


def _is_integer(conscious: 'Conscious') -> bool:
    return isinstance(conscious[WORK_STACK].peak(), int)


def _is_string(conscious: 'Conscious') -> bool:
    return isinstance(conscious[WORK_STACK].peak(), str)


def _is_none(conscious: 'Conscious') -> bool:
    return conscious[WORK_STACK].peak() is None


def _is_stack_frame(conscious: 'Conscious') -> bool:
    return conscious[WORK_STACK].peak() is stack.StackFrame


def _is_stack_bottom(conscious: 'Conscious') -> bool:
    return conscious[WORK_STACK].peak() is stack.StackBottom


# Branch
BRANCH = "BRANCH"
BRANCH_CLEAR = _clear
BRANCH_LESS_THAN_ZERO = _less_than_zero
BRANCH_GREATER_THAN_ZERO = _greater_than_zero
BRANCH_ZERO = _zero
BRANCH_NOT_ZERO = _not_zero
BRANCH_IS_INTEGER = _is_integer
BRANCH_IS_STRING = _is_string
BRANCH_IS_NONE = _is_none
BRANCH_IS_STACK_FRAME = _is_stack_frame
BRANCH_IS_STACK_BOTTOM = _is_stack_bottom


class Conscious(Dict):
    def __init__(self, **kwargs):
        """
        info: Makes a conscious "Thread".
        :param kwargs: Dict[str, object]
        :return: Dict[str, object]
        """
        new_conscious = {WORK_STACK: stack.Stack(),
                         FUNCTION_STACK: stack.Stack(),
                         R0: None,
                         R1: None,
                         R2: None,
                         R3: None,
                         R4: None,
                         R5: None,
                         R6: None,
                         R7: None,
                         R8: None,
                         R9: None,
                         PC_X: 0,
                         PC_Y: 0,
                         PC_FLOOR: 0,
                         PC_V_X: 1,
                         PC_V_Y: 0,
                         PC_V_FLOOR: 0,
                         ID: None,
                         ALIVE: True,
                         HALT: False,
                         BRANCH: BRANCH_CLEAR}
        new_conscious.update(kwargs)
        super(Conscious, self).__init__(new_conscious)

    def step(self) -> None:
        """
        info: Shift the PC Registers based off the PC Vector Registers.
        :return:
        """
        self[PC_X] += self[PC_V_X]
        self[PC_Y] += self[PC_V_Y]
        self[PC_FLOOR] += self[PC_V_FLOOR]

    def next_step(self) -> Tuple[int, int, int]:
        """
        info: Get the next location for conscious.
        :return: Tuple[int, int, int]
        """
        return self[PC_X] + self[PC_V_X], self[PC_Y] + self[PC_V_Y], self[PC_FLOOR] + self[PC_V_FLOOR]

    def at(self) -> Tuple[int, int, int]:
        """
        info: Get the current location of conscious.
        :return: Tuple[int, int, int]
        """
        return self[PC_X], self[PC_Y], self[PC_FLOOR]
