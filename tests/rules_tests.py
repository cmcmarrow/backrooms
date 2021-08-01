"""
Copyright 2021 Charles McMarrow
"""

# built-in
import unittest

# backrooms
from tests.full_test_runner import full_test


class TestRules(unittest.TestCase):
    def test_branch(self):
        full_test("branch.brs")

    def test_branch_is_type(self):
        full_test("branch_is_type.brs")

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

    def test_clear_stack(self):
        stream = full_test("clear_stack.brs").get_output_stream()
        self.assertEqual(len(stream), 4)
        self.assertEqual(stream[0], 41)
        self.assertEqual(stream[1], "StackBottom")
        self.assertEqual(stream[2], 5)
        self.assertEqual(stream[3], "StackBottom")

    def test_coordinates(self):
        stream = full_test("coordinates.brs").get_output_stream()
        self.assertEqual(len(stream), 12)
        self.assertEqual(stream[0], 0)
        self.assertEqual(stream[1], 0)
        self.assertEqual(stream[2], 0)
        self.assertEqual(stream[3], 9)
        self.assertEqual(stream[4], -2)
        self.assertEqual(stream[5], 0)
        self.assertEqual(stream[6], 16)
        self.assertEqual(stream[7], -4)
        self.assertEqual(stream[8], 0)
        self.assertEqual(stream[9], 2)
        self.assertEqual(stream[10], 40)
        self.assertEqual(stream[11], -1)

    def test_core_dump(self):
        stream = full_test("core_dump.brs").get_output_stream()
        self.assertEqual(len(stream), 0)
        stream = full_test("core_dump.brs", core_dump=True).get_output_stream()
        self.assertNotEqual(len(stream), 0)
        stream = "".join(stream)
        self.assertIn("Stacks\nWorking\tFunction\n", stream)
        self.assertIn("46", stream)
        self.assertIn("'R1': None", stream)
        self.assertIn("StackFrame", stream)
        self.assertIn("StackBottom", stream)

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

    def test_hallway_calls(self):
        stream = full_test("hallway_calls.brs").get_output_stream()
        self.assertEqual(len(stream), 10)
        self.assertEqual(stream[0], "cats")
        self.assertEqual(stream[1], "cats_echo")
        self.assertEqual(stream[2], "MAIN")
        self.assertEqual(stream[3], "cats")
        self.assertEqual(stream[4], "cats_echo")
        self.assertEqual(stream[5], "MAIN")
        self.assertEqual(stream[6], "cats_echo")
        self.assertEqual(stream[7], "MAIN")
        self.assertEqual(stream[8], "lol")
        self.assertEqual(stream[9], "StackBottom")

    def test_hallway_get_set(self):
        stream = full_test("hallway_get_set.brs").get_output_stream()      # TODO!!! write test

    def test_hallway_next_pass(self):
        stream = full_test("hallway_next_pass.brs").get_output_stream()
        self.assertEqual(len(stream), 15)
        self.assertEqual(stream[0], -2)
        self.assertEqual(stream[1], 10)
        self.assertEqual(stream[2], 1)
        self.assertIs(stream[3], None)
        self.assertIs(stream[4], None)
        self.assertEqual(stream[5], 1)
        self.assertIs(stream[6], None)
        self.assertEqual(stream[7], -2)
        self.assertEqual(stream[8], -2)
        self.assertIs(stream[9], None)
        self.assertIs(stream[10], None)
        self.assertEqual(stream[11], -2)
        self.assertEqual(stream[12], -3)
        self.assertEqual(stream[13], 0)
        self.assertEqual(stream[14], "StackBottom")

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
        self.assertEqual(len(stream), 8)
        self.assertEqual(stream[0], 0)
        self.assertEqual(stream[1], 11)
        self.assertEqual(stream[2], 6)
        self.assertEqual(stream[3], -2343)
        self.assertEqual(stream[4], 5)
        self.assertEqual(stream[5], 9)
        self.assertEqual(stream[6], 0)
        self.assertEqual(stream[7], "StackBottom")

    def test_integer_subtract(self):
        stream = full_test("integer_subtract.brs").get_output_stream()
        self.assertEqual(len(stream), 8)
        self.assertEqual(stream[0], 0)
        self.assertEqual(stream[1], -1)
        self.assertEqual(stream[2], 4)
        self.assertEqual(stream[3], 2347)
        self.assertEqual(stream[4], -1)
        self.assertEqual(stream[5], 1)
        self.assertEqual(stream[6], 0)
        self.assertEqual(stream[7], "StackBottom")

    def test_integer_multiply(self):
        stream = full_test("integer_multiply.brs").get_output_stream()
        self.assertEqual(len(stream), 8)
        self.assertEqual(stream[0], 0)
        self.assertEqual(stream[1], 30)
        self.assertEqual(stream[2], -150)
        self.assertEqual(stream[3], -4690)
        self.assertEqual(stream[4], 6)
        self.assertEqual(stream[5], 20)
        self.assertEqual(stream[6], 0)
        self.assertEqual(stream[7], "StackBottom")

    def test_integer_divide(self):
        stream = full_test("integer_divide.brs").get_output_stream()
        self.assertEqual(len(stream), 8)
        self.assertIs(stream[0], None)
        self.assertEqual(stream[1], 5)
        self.assertEqual(stream[2], -1)
        self.assertEqual(stream[3], 40)
        self.assertEqual(stream[4], 0)
        self.assertEqual(stream[5], 1)
        self.assertIs(stream[6], None)
        self.assertEqual(stream[7], "StackBottom")

    def test_integer_modular(self):
        stream = full_test("integer_modular.brs").get_output_stream()
        self.assertEqual(len(stream), 8)
        self.assertIs(stream[0], None)
        self.assertEqual(stream[1], 3)
        self.assertEqual(stream[2], -2)
        self.assertEqual(stream[3], 0)
        self.assertEqual(stream[4], 2)
        self.assertEqual(stream[5], 1)
        self.assertIs(stream[6], None)
        self.assertEqual(stream[7], "StackBottom")

    def test_integer_power(self):
        stream = full_test("integer_power.brs").get_output_stream()
        self.assertEqual(len(stream), 8)
        self.assertEqual(stream[0], 1)
        self.assertEqual(stream[1], 15625)
        self.assertEqual(stream[2], 0)
        self.assertEqual(stream[3], 4096)
        self.assertEqual(stream[4], 8)
        self.assertEqual(stream[5], 625)
        self.assertEqual(stream[6], 1)
        self.assertEqual(stream[7], "StackBottom")

    def test_integer_byte(self):
        stream = full_test("integer_byte.brs").get_output_stream()
        self.assertEqual(len(stream), 8)
        self.assertEqual(stream[0], chr(0))
        self.assertIs(stream[1], None)
        self.assertIs(stream[2], None)
        self.assertEqual(stream[3], chr(0))
        self.assertEqual(stream[4], chr(255))
        self.assertEqual(stream[5], "\n")
        self.assertEqual(stream[6], "C")
        self.assertEqual(stream[7], "StackBottom")

    def test_integer_absolute(self):
        stream = full_test("integer_absolute.brs").get_output_stream()
        self.assertEqual(len(stream), 6)
        self.assertEqual(stream[0], 0)
        self.assertEqual(stream[1], 523)
        self.assertEqual(stream[2], 33)
        self.assertEqual(stream[3], 1)
        self.assertEqual(stream[4], 89)
        self.assertEqual(stream[5], "StackBottom")

    def test_level(self):
        stream = full_test("level.brs").get_output_stream()
        self.assertEqual(len(stream), 19)
        self.assertEqual(stream[0], "level")
        self.assertEqual(stream[1], 0)
        self.assertEqual(stream[2], "cats")
        self.assertEqual(stream[3], 0)
        self.assertIs(stream[4], None)
        self.assertEqual(stream[5], "CATS2")
        self.assertEqual(stream[6], -1)
        self.assertIs(stream[7], None)
        self.assertEqual(stream[8], 0)
        self.assertEqual(stream[9], "cats")
        self.assertEqual(stream[10], "45362")
        self.assertEqual(stream[11], -3)
        self.assertEqual(stream[12], "45362")
        self.assertEqual(stream[13], -3)
        self.assertEqual(stream[14], "askjdFSF4325")
        self.assertEqual(stream[15], 1)
        self.assertEqual(stream[16], "cats")
        self.assertEqual(stream[17], 1)
        self.assertEqual(stream[18], "StackBottom")

    def test_pop(self):
        stream = full_test("pop.brs").get_output_stream()
        self.assertEqual(len(stream), 7)
        self.assertEqual(stream[0], "StackBottom")
        self.assertEqual(stream[1], "StackFrame")
        self.assertEqual(stream[2], "cats")
        self.assertEqual(stream[3], 45)
        self.assertIs(stream[4], None)
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

    def test_read(self):
        stream = full_test("read.brs").get_output_stream()
        self.assertEqual(len(stream), 12)
        self.assertIs(stream[0], None)
        self.assertEqual(stream[1], "StackFrame")
        self.assertEqual(stream[2], 100)
        self.assertEqual(stream[3], -100)
        self.assertEqual(stream[4], 100)
        self.assertEqual(stream[5], "StackBottom")
        self.assertEqual(stream[6], "StackBottom")
        self.assertEqual(stream[7], "StackBottom")
        self.assertEqual(stream[8], "cats")
        self.assertEqual(stream[9], "run")
        self.assertEqual(stream[10], "")
        self.assertEqual(stream[11], "lilith")

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

    def test_string_length(self):
        stream = full_test("string_length.brs").get_output_stream()
        self.assertEqual(len(stream), 5)
        self.assertEqual(stream[0], 11)
        self.assertEqual(stream[1], 4)
        self.assertEqual(stream[2], 0)
        self.assertEqual(stream[3], 17)
        self.assertEqual(stream[4], "StackBottom")

    def test_string_cast(self):
        stream = full_test("string_cast.brs").get_output_stream()
        self.assertEqual(len(stream), 6)
        self.assertEqual(stream[0], "StackBottom!")
        self.assertEqual(stream[1], "StackFrame!")
        self.assertEqual(stream[2], "None")
        self.assertEqual(stream[3], "-45")
        self.assertEqual(stream[4], "cats")
        self.assertEqual(stream[5], "StackBottom")

    def test_string_at(self):
        stream = full_test("string_at.brs").get_output_stream()
        self.assertEqual(len(stream), 14)
        self.assertEqual(stream[0], "c")
        self.assertEqual(stream[1], "a")
        self.assertEqual(stream[2], "t")
        self.assertEqual(stream[3], "s")
        self.assertIs(stream[4], None)
        self.assertIs(stream[5], None)
        self.assertEqual(stream[6], "s")
        self.assertEqual(stream[7], "t")
        self.assertEqual(stream[8], "a")
        self.assertEqual(stream[9], "c")
        self.assertIs(stream[10], None)
        self.assertIs(stream[11], None)
        self.assertEqual(stream[12], "#")
        self.assertEqual(stream[13], "StackBottom")

    def test_string_byte(self):
        stream = full_test("string_byte.brs").get_output_stream()
        self.assertEqual(len(stream), 7)
        self.assertIs(stream[0], None)
        self.assertEqual(stream[1], 97)
        self.assertEqual(stream[2], 64)
        self.assertEqual(stream[3], 62)
        self.assertEqual(stream[4], 10)
        self.assertEqual(stream[5], 0)
        self.assertEqual(stream[6], "StackBottom")

    def test_string_split(self):
        stream = full_test("string_split.brs").get_output_stream()
        self.assertEqual(len(stream), 9)
        self.assertEqual(stream[0], "12345")
        self.assertEqual(stream[1], "67890")
        self.assertEqual(stream[2], "asdfg")
        self.assertEqual(stream[3], "hjkl")
        self.assertEqual(stream[4], "1234567890")
        self.assertEqual(stream[5], "")
        self.assertEqual(stream[6], "")
        self.assertEqual(stream[7], "asdfghjkl")
        self.assertEqual(stream[8], "StackBottom")

    def test_string_join(self):
        stream = full_test("string_join.brs").get_output_stream()
        self.assertEqual(len(stream), 4)
        self.assertEqual(stream[0], "cats12345")
        self.assertEqual(stream[1], "")
        self.assertEqual(stream[2], "!@#$[]")
        self.assertEqual(stream[3], "StackBottom")

    def test_string_equal(self):
        stream = full_test("string_equal.brs").get_output_stream()
        self.assertEqual(len(stream), 5)
        self.assertEqual(stream[0], 1)
        self.assertEqual(stream[1], 1)
        self.assertEqual(stream[2], 0)
        self.assertEqual(stream[3], 0)
        self.assertEqual(stream[4], "StackBottom")

    def test_string_in(self):
        stream = full_test("string_in.brs").get_output_stream()
        self.assertEqual(len(stream), 5)
        self.assertEqual(stream[0], 1)
        self.assertEqual(stream[1], 0)
        self.assertEqual(stream[2], 1)
        self.assertEqual(stream[3], 0)
        self.assertEqual(stream[4], "StackBottom")

    def test_string_upper(self):
        stream = full_test("string_upper.brs").get_output_stream()
        self.assertEqual(len(stream), 3)
        self.assertEqual(stream[0], "CATS")
        self.assertEqual(stream[1], "1234!@#$QWERQWER")
        self.assertEqual(stream[2], "StackBottom")

    def test_string_lower(self):
        stream = full_test("string_lower.brs").get_output_stream()
        self.assertEqual(len(stream), 3)
        self.assertEqual(stream[0], "cats")
        self.assertEqual(stream[1], "1234!@#$qwerqwer")
        self.assertEqual(stream[2], "StackBottom")

    def test_thread(self):
        stream = full_test("thread.brs").get_output_stream()
        self.assertEqual(len(stream), 70)
        self.assertEqual(stream[0], 0)
        self.assertEqual(stream[1], -1)
        self.assertEqual(stream[2], 0)
        self.assertEqual(stream[3], "not main thread")
        ids = (1, 17, 9, 18, 5, 19, 10, 20, 3, 21, 11, 22, 6, 23, 12, 24,
               2, 25, 13, 26, 7, 27, 14, 28, 4, 29, 15, 30, 8, 31, 16, 32)
        for spot, i in enumerate(ids):
            self.assertEqual(stream[spot * 2 + 4], i)
            self.assertEqual(stream[spot * 2 + 5], " ")
        self.assertEqual(stream[68], "done")
        self.assertEqual(stream[69], "done")

    def test_thread_2(self):
        stream = full_test("thread_2.brs").get_output_stream()
        self.assertEqual(len(stream), 1)
        self.assertEqual(stream[0], "StackBottom")

    def test_thread_3(self):
        stream = full_test("thread_3.brs").get_output_stream()
        self.assertEqual(len(stream), 1)
        self.assertEqual(stream[0], 1)

    def test_uncommon_double_duplicate(self):
        stream = full_test("uncommon_double_duplicate.brs").get_output_stream()
        self.assertEqual(len(stream), 11)
        self.assertEqual(stream[0], "StackFrame")
        self.assertIs(stream[1], None)
        self.assertEqual(stream[2], "StackFrame")
        self.assertIs(stream[3], None)
        self.assertEqual(stream[4], 5)
        self.assertEqual(stream[5], "cats")
        self.assertEqual(stream[6], 5)
        self.assertEqual(stream[7], "cats")
        self.assertEqual(stream[8], 4)
        self.assertEqual(stream[9], 1)
        self.assertEqual(stream[10], "StackBottom")

    def test_uncommon_dynamic_dump(self):
        stream = full_test("uncommon_dynamic_dump.brs").get_output_stream()
        self.assertEqual(len(stream), 4)
        self.assertEqual(stream[0], "lol")
        self.assertEqual(stream[1], -45)
        self.assertEqual(stream[2], "StackFrame")
        self.assertEqual(stream[3], "StackBottom")

    def test_uncommon_simple_dump(self):
        stream = full_test("uncommon_simple_dump.brs").get_output_stream()
        self.assertEqual(len(stream), 3)
        self.assertEqual(stream[0], 32)
        self.assertEqual(stream[1], "cats")
        self.assertEqual(stream[2], "StackBottom")

    def test_uncommon_read_flip(self):
        stream = full_test("uncommon_read_flip.brs").get_output_stream()
        self.assertEqual(len(stream), 5)
        self.assertIs(stream[0], None)
        self.assertEqual(stream[1], "StackFrame")
        self.assertEqual(stream[2], "cats")
        self.assertEqual(stream[3], -4325)
        self.assertEqual(stream[4], "StackBottom")

    def test_uncommon_write_flip(self):
        stream = full_test("uncommon_write_flip.brs").get_output_stream()
        self.assertEqual(len(stream), 6)
        self.assertIs(stream[0], None)
        self.assertEqual(stream[1], "StackFrame")
        self.assertIs(stream[2], None)
        self.assertEqual(stream[3], -4123)
        self.assertEqual(stream[4], "cats2")
        self.assertEqual(stream[5], "StackBottom")

    def test_uncommon_hot_patch(self):
        stream = full_test("uncommon_hot_patch.brs").get_output_stream()
        self.assertEqual(len(stream), 3)
        self.assertEqual(stream[0], "hot patch")
        self.assertEqual(stream[1], -9)
        self.assertEqual(stream[2], "StackBottom")

    def test_write(self):
        stream = full_test("write.brs").get_output_stream()
        self.assertEqual(len(stream), 6)
        self.assertEqual(stream[0], -38764)
        self.assertEqual(stream[1], "StackFrame")
        self.assertIs(stream[2], None)
        self.assertEqual(stream[3], "cats")
        self.assertIs(stream[4], None)
        self.assertEqual(stream[5], "StackBottom")

    def test_mirrors(self):
        stream = full_test("mirrors.brs").get_output_stream()
        self.assertEqual(len(stream), 3)
        self.assertEqual(stream[0], "StackFrame")
        self.assertEqual(stream[1], 44)
        self.assertIs(stream[2], "StackBottom")
