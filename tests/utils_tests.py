"""
Copyright 2021 Charles McMarrow
"""

# built-in
import unittest

# backrooms
from tests.full_test_runner import full_test


class TestUtils(unittest.TestCase):
    def test_base_heap(self):
        portal = full_test("utils_base_heap.brs")
        stream = portal.get_output_stream()
        rooms = portal.get_rooms()
        self.assertEqual(len(stream), 5)
        self.assertIsNone(stream[0])
        self.assertEqual(stream[1], 66)
        self.assertEqual(stream[2], "cats")
        self.assertEqual(stream[3], "StackFrame")
        self.assertEqual(stream[4], "StackBottom")
        self.assertEqual(rooms.get_hallway_location(0, "1"), 11)
        self.assertEqual(rooms.get_hallway_location(0, "2"), 12)
        self.assertIsNone(rooms.get_hallway_location(0, "3"))
        self.assertIsNone(rooms.get_hallway_location(0, "4"))

        for spot, c in enumerate(f">ri66ri11hr" + " " * 100):
            self.assertEqual(rooms.read(spot, 12, 0), c)

        for i in range(-100, 101):
            self.assertEqual(rooms.read(i, 13, 0), " ")
            self.assertEqual(rooms.read(i, 14, 0), " ")

    def test_type_read(self):
        stream = full_test("utils_type_read.brs").get_output_stream()
        self.assertEqual(len(stream), 8)
        self.assertEqual(stream[0], "rn")
        self.assertEqual(stream[1], "rn")
        self.assertEqual(stream[2], "rf")
        self.assertEqual(stream[3], "ri-2345")
        self.assertEqual(stream[4], "ri0")
        self.assertEqual(stream[5], f"rs{chr(0)}cats{chr(0)}")
        self.assertEqual(stream[6], f"rs{chr(0)}{chr(0)}")
        self.assertEqual(stream[7], "StackBottom")

    def test_wsize(self):
        stream = full_test("utils_wsize.brs", lost_count=50000).get_output_stream()
        self.assertEqual(len(stream), 1001)
        for size, wsize in enumerate(stream[:-1]):
            self.assertEqual(f"1{'2'*size}ri{len(wsize)}hr", wsize)
            self.assertEqual(len(f"1{'2' * size}ri{len(wsize)}hr"), len(wsize))
        self.assertEqual(stream[1000], "StackBottom")
