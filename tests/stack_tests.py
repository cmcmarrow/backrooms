"""
Copyright 2021 Charles McMarrow
"""

# built-in
import unittest

# backrooms
from backrooms.stack import Stack, StackFrame, StackBottom


class TestStack(unittest.TestCase):
    def test_init(self):
        self.assertIsInstance(Stack(), Stack)

    def test_push_and_pop(self):
        stack = Stack()
        self.assertIs(stack.pop(), StackBottom)
        self.assertIs(stack.pop(), StackBottom)

        stack.push(1)
        stack.push(1)
        stack.push(None)

        self.assertEqual(stack.pop(), None)
        self.assertEqual(stack.pop(), 1)
        self.assertEqual(stack.pop(), 1)

        self.assertIs(stack.pop(), StackBottom)

        stack.push(2)
        stack.push(StackBottom)
        stack.push(3)

        stack.pop()
        stack.pop()

        self.assertIs(stack.pop(), StackBottom)
        self.assertIs(stack.pop(), StackBottom)

    def test_is_empty(self):
        stack = Stack()
        self.assertTrue(stack.is_empty())
        stack.push(2)
        self.assertFalse(stack.is_empty())
        stack.push(3)
        self.assertFalse(stack.is_empty())
        stack.pop()
        self.assertFalse(stack.is_empty())
        stack.pop()
        self.assertTrue(stack.is_empty())

    def test_push_and_pop_frame(self):
        stack = Stack()
        stack.push_frame()
        stack.pop_frame()
        stack.push_frame()
        self.assertIs(stack.pop(), StackFrame)

        stack.push(1)
        stack.push_frame()
        stack.push("cats")
        stack.push(None)
        stack.pop_frame()
        self.assertEqual(stack.pop(), 1)
