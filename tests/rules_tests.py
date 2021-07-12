"""
Copyright 2021 Charles McMarrow
"""

# built-in
import unittest

# backrooms
from backrooms.stack import StackFrame, StackBottom
from tests.full_test_runner import full_test


class TestRules(unittest.TestCase):
    def test_integer_add(self):
        stream = full_test("integer_add.brs").get_output_stream()
        self.assertEqual(len(stream), 7)
        self.assertEqual(stream[0], 0)
        self.assertEqual(stream[1], 11)
        self.assertEqual(stream[2], 6)
        self.assertEqual(stream[3], -2343)
        self.assertEqual(stream[4], "StackBottom")
        self.assertEqual(stream[5], "StackBottom")
        self.assertEqual(stream[6], "StackBottom")

    def test_integer_subtract(self):
        stream = full_test("integer_subtract.brs").get_output_stream()
        self.assertEqual(len(stream), 7)
        self.assertEqual(stream[0], 0)
        self.assertEqual(stream[1], -1)
        self.assertEqual(stream[2], 4)
        self.assertEqual(stream[3], 2347)
        self.assertEqual(stream[4], "StackBottom")
        self.assertEqual(stream[5], "StackBottom")
        self.assertEqual(stream[6], "StackBottom")

    def test_integer_multiply(self):
        stream = full_test("integer_multiply.brs").get_output_stream()
        self.assertEqual(len(stream), 7)
        self.assertEqual(stream[0], 0)
        self.assertEqual(stream[1], 30)
        self.assertEqual(stream[2], -150)
        self.assertEqual(stream[3], -4690)
        self.assertEqual(stream[4], "StackBottom")
        self.assertEqual(stream[5], "StackBottom")
        self.assertEqual(stream[6], "StackBottom")

    def test_integer_divide(self):
        stream = full_test("integer_divide.brs").get_output_stream()
        self.assertEqual(len(stream), 7)
        self.assertIs(stream[0], None)
        self.assertEqual(stream[1], 5)
        self.assertEqual(stream[2], -1)
        self.assertEqual(stream[3], 40)
        self.assertEqual(stream[4], "StackBottom")
        self.assertEqual(stream[5], "StackBottom")
        self.assertEqual(stream[6], "StackBottom")

    def test_integer_modular(self):
        stream = full_test("integer_modular.brs").get_output_stream()
        self.assertEqual(len(stream), 7)
        self.assertIs(stream[0], None)
        self.assertEqual(stream[1], 3)
        self.assertEqual(stream[2], -2)
        self.assertEqual(stream[3], 0)
        self.assertEqual(stream[4], "StackBottom")
        self.assertEqual(stream[5], "StackBottom")
        self.assertEqual(stream[6], "StackBottom")

    def test_integer_power(self):
        stream = full_test("integer_power.brs").get_output_stream()
        self.assertEqual(len(stream), 7)
        self.assertEqual(stream[0], 1)
        self.assertEqual(stream[1], 15625)
        self.assertEqual(stream[2], 0)
        self.assertEqual(stream[3], 4096)
        self.assertEqual(stream[4], "StackBottom")
        self.assertEqual(stream[5], "StackBottom")
        self.assertEqual(stream[6], "StackBottom")
