"""
Copyright 2021 Charles McMarrow
"""

# built-in
import unittest

# backrooms
from tests.full_test_runner import full_test


class TestHeaps(unittest.TestCase):
    def test_heap_array(self):
        portal = full_test("heap_array.brs", lost_count=450000)
        stream = portal.get_output_stream()
        rooms = portal.get_rooms()

        self.assertEqual(len(stream), 9)

        self.assertIsInstance(stream[0], str)
        id_1: str = stream.pop(0)
        self.assertIsInstance(stream[0], str)
        id_2: str = stream.pop(0)
        self.assertIsInstance(stream[0], str)
        id_3: str = stream.pop(0)

        self.assertEqual(stream[0], "cats")
        self.assertEqual(stream[1], "cats")
        self.assertEqual(stream[2], 45)
        self.assertEqual(stream[3], "StackFrame")
        self.assertIsNone(stream[4])
        self.assertEqual(stream[5], "StackBottom")

        floor = rooms.get_floor_level("heap")
        self.assertEqual(rooms.get_hallway_location(floor, id_1),
                         rooms.get_hallway_location(floor, "_START") - 1)
        self.assertEqual(rooms.get_hallway_location(floor, id_2),
                         rooms.get_hallway_location(floor, "_START") - 2)
        self.assertEqual(rooms.get_hallway_location(floor, id_3),
                         rooms.get_hallway_location(floor, "_START") - 1002)

        for i in range(1, 1000):
            self.assertIsInstance(rooms.get_hallway_location(floor, f"{id_2}_{i}"), int)

        for i in range(1, 9):
            self.assertIsInstance(rooms.get_hallway_location(floor, f"{id_3}_{i}"), int)

        self.assertIsNone(rooms.get_hallway_location(floor, f"{id_1}_1"))
        self.assertIsNone(rooms.get_hallway_location(floor, f"{id_2}_1000"))
        self.assertIsNone(rooms.get_hallway_location(floor, f"{id_3}_9"))

    def test_heap_basic(self):
        portal = full_test("heap_basic.brs")
        stream = portal.get_output_stream()
        rooms = portal.get_rooms()

        self.assertEqual(len(stream), 13)

        self.assertIsInstance(stream[0], str)
        id_1: str = stream.pop(0)
        self.assertIsInstance(stream[0], str)
        id_2: str = stream.pop(0)
        self.assertIsInstance(stream[0], str)
        id_3: str = stream.pop(0)
        self.assertIsInstance(stream[3], str)
        id_4: str = stream.pop(3)
        self.assertIsInstance(stream[3], str)
        id_5: str = stream.pop(3)

        self.assertEqual(stream[0], "cats")
        self.assertEqual(stream[1], 55)
        self.assertEqual(stream[2], "StackFrame")
        self.assertEqual(stream[3], "cats")
        self.assertIsNone(stream[4])
        self.assertEqual(stream[5], "StackFrame")
        self.assertEqual(stream[6], "*")
        self.assertEqual(stream[7], "StackBottom")

        self.assertEqual(id_2, id_4)

        floor = rooms.get_floor_level("heap")
        self.assertEqual(rooms.get_hallway_location(floor, id_1),
                         rooms.get_hallway_location(floor, "_START") - 1)
        self.assertEqual(rooms.get_hallway_location(floor, id_4),
                         rooms.get_hallway_location(floor, "_START") - 2)
        self.assertEqual(rooms.get_hallway_location(floor, id_3),
                         rooms.get_hallway_location(floor, "_START") - 3)
        self.assertEqual(rooms.get_hallway_location(floor, id_5),
                         rooms.get_hallway_location(floor, "_START") - 4)

    def test_heap_del(self):
        portal = full_test("heap_del.brs")
        stream = portal.get_output_stream()
        rooms = portal.get_rooms()

    def test_heap_del_2(self):
        portal = full_test("heap_del_2.brs")
        stream = portal.get_output_stream()
        rooms = portal.get_rooms()
