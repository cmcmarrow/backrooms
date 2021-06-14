"""
Copyright 2021 Charles McMarrow

This script holds a simple stack data structure.
"""

# built-in
from typing import List


class StackBottom:
    pass


class StackFrame:
    pass


class Stack:
    def __init__(self):
        """
        info: Simple stack with some stack frames
        """
        self._stack: List[object] = [StackBottom]

    def __bool__(self):
        return not self.is_empty()

    def push(self, item: object) -> None:
        """
        info: Push item to stack unless item is stack bottom.
        :param item: object
        :return: object
        """
        if item is not StackBottom:
            self._stack.append(item)

    def pop(self) -> object:
        """
        info: Pop item from stack unless item is stack bottom.
        :return: object
        """
        if self._stack[-1] is StackBottom:
            return StackBottom
        return self._stack.pop()

    def is_empty(self) -> bool:
        """
        info: Checks if stack is empty.
        :return: bool
        """
        return self._stack[-1] is StackBottom

    def push_frame(self) -> None:
        """
        info: Push stack frame to stack.
        :return: None
        """
        self.push(StackFrame)

    def pop_frame(self) -> None:
        """
        info: Pop till end of stack or till a frame is found.
        :return: None
        """
        while not self.is_empty():
            if self.pop() is StackFrame:
                return
