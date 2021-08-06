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
        info: Simple Stack with StackFrames.
        """
        self._stack: List[object] = [StackBottom]

    def __bool__(self) -> bool:
        """
        info: check if Stack is empty.
        :return: bool
        """
        return not self.is_empty()

    def __repr__(self):
        """
        info: Shows top item on stack.
        :return: str
        """
        return f"<{self.__class__.__name__}: {self.peak()}>"

    def push(self, item: object) -> None:
        """
        info: Push item to Stack unless item is StackBottom.
        :param item: object
        :return: object
        """
        if item is not StackBottom:
            self._stack.append(item)

    def pop(self) -> object:
        """
        info: Pop item from Stack unless item is StackBottom.
        :return: object
        """
        if self._stack[-1] is StackBottom:
            return StackBottom
        return self._stack.pop()

    def peak(self) -> object:
        """
        info: Peak at item on top of Stack.
        :return: object
        """
        return self._stack[-1]

    def is_empty(self) -> bool:
        """
        info: Checks if Stack is empty.
        :return: bool
        """
        return self._stack[-1] is StackBottom

    def push_frame(self) -> None:
        """
        info: Push StackFrame to stack.
        :return: None
        """
        self.push(StackFrame)

    def pop_frame(self) -> None:
        """
        info: Pop till end of Stack or till a StackFrame is found.
        :return: None
        """
        while not self.is_empty():
            if self.pop() is StackFrame:
                return

    def clear(self) -> None:
        """
        info: Clear data off Stack.
        :return: None
        """
        self._stack.clear()
        self._stack.append(StackBottom)
