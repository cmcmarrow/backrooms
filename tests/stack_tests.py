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

        self.assertIsNone(stack.pop())
        self.assertEqual(stack.pop(), 1)
        self.assertEqual(stack.pop(), 1)

        self.assertIs(stack.pop(), StackBottom)

        stack.push(2)
        stack.push(StackBottom)
        stack.push(3)

        self.assertEqual(stack.pop(), 3)
        self.assertEqual(stack.pop(), 2)
        self.assertIs(stack.pop(), StackBottom)
        self.assertIs(stack.pop(), StackBottom)

    def test_peak(self):
        stack = Stack()
        self.assertIs(stack.peak(), StackBottom)
        for i in range(100):
            stack.push(i)
            self.assertEqual(stack.peak(), i)
        for i in range(99, -1, -1):
            self.assertEqual(stack.peak(), i)
            self.assertEqual(stack.pop(), i)
        self.assertIs(stack.peak(), StackBottom)

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

    def test_clear(self):
        stack = Stack()
        stack.clear()
        self.assertIs(stack.pop(), StackBottom)
        for i in range(100):
            stack.push(i)
            stack.push(i*2)
            stack.push(StackFrame)
        stack.clear()
        self.assertIs(stack.pop(), StackBottom)
