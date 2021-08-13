"""
Copyright 2021 Charles McMarrow
"""

# built-in
import unittest

# backrooms
from tests.full_test_runner import full_test


class TestVariables(unittest.TestCase):
    def test_variables(self):
        portal = full_test("variables.brs")
        stream = portal.get_output_stream()
        rooms = portal.get_rooms()

        self.assertEqual(len(stream), 12)
        self.assertEqual(stream[0], 45)
        self.assertEqual(stream[1], "StackFrame")
        self.assertEqual(stream[2], "B")
        self.assertEqual(stream[3], -8374)
        self.assertEqual(stream[4], 45)
        self.assertIsNone(stream[5])
        self.assertEqual(stream[6], "uuuu")
        self.assertEqual(stream[7], "asdf")
        self.assertIsNone(stream[8])
        self.assertIsNone(stream[9])
        self.assertEqual(stream[10], "1234")
        self.assertEqual(stream[11], "StackBottom")

        floor = rooms.get_floor_level("vars")
        self.assertEqual(rooms.get_hallway_location(floor, "cats"),
                         rooms.get_hallway_location(floor, "_START") - 1)
        self.assertEqual(rooms.get_hallway_location(floor, "G"),
                         rooms.get_hallway_location(floor, "_START") - 3)
        self.assertEqual(rooms.get_hallway_location(floor, "666666"),
                         rooms.get_hallway_location(floor, "_START") - 4)
        self.assertEqual(rooms.get_hallway_location(floor, "FF"),
                         rooms.get_hallway_location(floor, "_START") - 5)
        self.assertIsNone(rooms.get_hallway_location(floor, "A"))
        self.assertIsNone(rooms.get_hallway_location(floor, "F"))

    def test_variables_del(self):
        portal = full_test("variables_del.brs", lost_count=15000)
        stream = portal.get_output_stream()
        rooms = portal.get_rooms()

        self.assertEqual(len(stream), 3)
        self.assertEqual(stream[0], 450)
        self.assertEqual(stream[1], 78)
        self.assertEqual(stream[2], "StackBottom")

        floor = rooms.get_floor_level("vars")
        self.assertEqual(rooms.get_hallway_location(floor, "cats"),
                         rooms.get_hallway_location(floor, "_START") - 1)
        self.assertEqual(rooms.get_hallway_location(floor, "1"),
                         rooms.get_hallway_location(floor, "_START") - 2)
        self.assertIsNone(rooms.get_hallway_location(floor, "F"))
        self.assertIsNone(rooms.get_hallway_location(floor, "A"))
        self.assertIsNone(rooms.get_hallway_location(floor, "666666"))

    def test_variables_del_2(self):
        portal = full_test("variables_del_2.brs", lost_count=20000)
        stream = portal.get_output_stream()
        rooms = portal.get_rooms()

        self.assertEqual(len(stream), 4)
        self.assertEqual(stream[0], "StackFrame")
        self.assertEqual(stream[1], 78)
        self.assertEqual(stream[2], 79)
        self.assertEqual(stream[3], "StackBottom")

        floor = rooms.get_floor_level("vars")

        self.assertEqual(rooms.get_hallway_location(floor, "1"),
                         rooms.get_hallway_location(floor, "_START") - 1)
        self.assertEqual(rooms.get_hallway_location(floor, "F"),
                         rooms.get_hallway_location(floor, "_START") - 2)
        self.assertEqual(rooms.get_hallway_location(floor, "2"),
                         rooms.get_hallway_location(floor, "_START") - 3)

        self.assertIsNone(rooms.get_hallway_location(floor, "cats"))
        self.assertIsNone(rooms.get_hallway_location(floor, "A"))
        self.assertIsNone(rooms.get_hallway_location(floor, "666666"))
