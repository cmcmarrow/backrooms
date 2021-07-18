"""
Copyright 2021 Charles McMarrow
"""

# built-in
import unittest

# backrooms
from backrooms.stack import StackFrame, StackBottom
from tests.full_test_runner import full_test


class TestRules(unittest.TestCase):
    def test_branch_clear(self):
        full_test("branch_clear.brs")

    def test_branch_is_type(self):
        full_test("branch_is_type.brs")

    def test_branch_something_zero(self):   # TODO write
        full_test("branch_something_zero.brs")

    def test_cite(self):
        stream = full_test("cite.brs",
                           inputs=("", "hello <>{}[]!", "cite", "~ha", f"{chr(0)}{chr(9)}bad")).get_output_stream()
        self.assertEqual(len(stream), 7)
        self.assertEqual(stream[0], "")
        self.assertEqual(stream[1], "hello <>{}[]!")
        self.assertEqual(stream[2], "cite")
        self.assertEqual(stream[3], "ha")
        self.assertEqual(stream[4], "bad")
        self.assertEqual(stream[5], "")
        self.assertEqual(stream[6], "")

    def test_duplicate(self):
        stream = full_test("duplicate.brs").get_output_stream()
        self.assertEqual(len(stream), 8)
        self.assertEqual(stream[0], "StackBottom")
        self.assertEqual(stream[1], "StackBottom")
        self.assertIs(stream[2], None)
        self.assertIs(stream[3], None)
        self.assertEqual(stream[4], "cats")
        self.assertEqual(stream[5], "cats")
        self.assertEqual(stream[6], 1)
        self.assertEqual(stream[7], "StackBottom")

    def test_echo(self):
        stream = full_test("echo.brs").get_output_stream()
        self.assertEqual(len(stream), 6)
        self.assertEqual(stream[0], "StackBottom")
        self.assertEqual(stream[1], "StackFrame")
        self.assertIs(stream[2], None)
        self.assertEqual(stream[3], "ECHO")
        self.assertEqual(stream[4], -56)
        self.assertEqual(stream[5], "StackBottom")

    def test_halt(self):
        full_test("halt.brs")

    def test_halt_2(self):
        full_test("halt_2.brs")

    def test_hope_one(self):
        full_test("hope_one.brs")

    def test_hope_two(self):
        full_test("hope_two.brs")

    def test_hope_three(self):
        full_test("hope_three.brs")

    def test_hope_four(self):
        full_test("hope_four.brs")

    def test_hope_five(self):
        full_test("hope_five.brs")

    def test_hope_six(self):
        full_test("hope_six.brs")

    def test_hope_seven(self):
        full_test("hope_seven.brs")

    def test_hope_eighth(self):
        full_test("hope_eighth.brs")

    def test_hope_nine(self):
        full_test("hope_nine.brs")

    def test_integer_cast(self):
        stream = full_test("integer_cast.brs").get_output_stream()
        self.assertEqual(len(stream), 11)
        self.assertIs(stream[0], None)
        self.assertIs(stream[1], None)
        self.assertIs(stream[2], None)
        self.assertEqual(stream[3], -34)
        self.assertEqual(stream[4], 5)
        self.assertEqual(stream[5], 325)
        self.assertEqual(stream[6], -345)
        self.assertIs(stream[7], None)
        self.assertIs(stream[8], None)
        self.assertIs(stream[9], None)
        self.assertEqual(stream[10], "StackBottom")

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

    def test_integer_byte(self):
        stream = full_test("integer_byte.brs").get_output_stream()
        self.assertEqual(len(stream), 8)
        self.assertEqual(stream[0], "StackBottom")
        self.assertEqual(stream[1], None)
        self.assertEqual(stream[2], None)
        self.assertEqual(stream[3], chr(0))
        self.assertEqual(stream[4], chr(255))
        self.assertEqual(stream[5], "\n")
        self.assertEqual(stream[6], "C")
        self.assertEqual(stream[7], "StackBottom")

    def test_integer_absolute(self):
        stream = full_test("integer_absolute.brs").get_output_stream()
        self.assertEqual(len(stream), 6)
        self.assertEqual(stream[0], "StackBottom")
        self.assertEqual(stream[1], 523)
        self.assertEqual(stream[2], 33)
        self.assertEqual(stream[3], 1)
        self.assertEqual(stream[4], 89)
        self.assertEqual(stream[5], "StackBottom")

    def test_pop(self):
        stream = full_test("pop.brs").get_output_stream()
        self.assertEqual(len(stream), 7)
        self.assertEqual(stream[0], "StackBottom")
        self.assertEqual(stream[1], "StackFrame")
        self.assertEqual(stream[2], "cats")
        self.assertEqual(stream[3], 45)
        self.assertEqual(stream[4], None)
        self.assertEqual(stream[5], "StackBottom")
        self.assertEqual(stream[6], "StackBottom")

    def test_pop_frame(self):
        stream = full_test("pop_frame.brs").get_output_stream()
        self.assertEqual(len(stream), 7)
        self.assertEqual(stream[0], "StackBottom")
        self.assertEqual(stream[1], "StackFrame")
        self.assertEqual(stream[2], "StackFrame")
        self.assertEqual(stream[3], 4)
        self.assertIs(stream[4], None)
        self.assertEqual(stream[5], "StackBottom")
        self.assertEqual(stream[6], "StackBottom")

    def test_register(self):
        stream = full_test("register.brs").get_output_stream()
        self.assertEqual(len(stream), 22)

        for i in range(10):
            self.assertIs(stream[i], None)

        self.assertEqual(stream[10], "StackBottom")
        self.assertEqual(stream[11], "StackBottom")

        for i in range(10):
            self.assertEqual(stream[i + 12], i * (-1 if i % 2 else 1))

    def test_shifter(self):
        full_test("shifter.brs")

    def test_switch(self):
        stream = full_test("switch.brs").get_output_stream()
        self.assertEqual(len(stream), 7)
        self.assertEqual(stream[0], 1)
        self.assertIs(stream[1], None)
        self.assertEqual(stream[2], "StackFrame")
        self.assertEqual(stream[3], 3)
        self.assertEqual(stream[4], "str")
        self.assertEqual(stream[5], "StackBottom")
        self.assertEqual(stream[6], "StackBottom")
