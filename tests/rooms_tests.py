"""
Copyright 2021 Charles McMarrow
"""

# built-in
import unittest

# backrooms
from backrooms.rooms import Rooms, RoomsError, is_character, is_name


class IsCharacterTest(unittest.TestCase):
    def test_is_character(self):
        for character in range(256):
            self.assertTrue(is_character(chr(character)))

    def test_is_character_bad(self):
        for character in range(256, 500):
            self.assertFalse(is_character(chr(character)))


class IsNameTest(unittest.TestCase):
    def test_is_name_1(self):
        self.assertTrue(is_name("cats"))

    def test_is_name_2(self):
        self.assertTrue(is_name("c"))

    def test_is_name_3(self):
        self.assertTrue(is_name("2345_242"))

    def test_is_name_bad_1(self):
        self.assertFalse(is_name(""))

    def test_is_name_bad_2(self):
        self.assertFalse(is_name("2435_24^DD"))

    def test_is_name_bad_3(self):
        self.assertFalse(is_name("!"))


class RoomsTests(unittest.TestCase):
    def test_init(self):
        self.assertIsInstance(Rooms(), Rooms)

    def test_read_and_write(self):
        rooms = Rooms()
        self.assertEqual(rooms.read(0, 0, 0), " ")
        self.assertEqual(rooms.read(345, 2345235, -10000), " ")

        rooms.write_line(0, 0, 0, chr(0))
        rooms.write_line(1, 0, 0, chr(255))

        self.assertEqual(rooms.read(0, 0, 0), chr(0))
        self.assertEqual(rooms.read(1, 0, 0), chr(255))

    def test_read_and_write_2(self):
        rooms = Rooms()

        rooms.write_line(345, 2345235, -10001, "1")
        rooms.write_line(345, 2345235, -10002, "2")
        rooms.write_line(345, 2345235, -10003, "3")
        rooms.write_line(345, 2345235, -10004, "4")

        self.assertEqual(rooms.read(345, 2345235, -10001), "1")
        self.assertEqual(rooms.read(345, 2345235, -10002), "2")
        self.assertEqual(rooms.read(345, 2345235, -10003), "3")
        self.assertEqual(rooms.read(345, 2345235, -10004), "4")

    def test_read_and_write_all_ascii(self):
        rooms = Rooms()
        for character in range(256):
            rooms.write(55, -66, 79, chr(character))
            self.assertEqual(rooms.read(55, -66, 79), chr(character))

    def test_read_and_write_line(self):
        rooms = Rooms()
        rooms.write_line(1, 2, 3, "cats", 1, 0, 0)

        self.assertEqual(rooms.read(1, 2, 3), "c")
        self.assertEqual(rooms.read(2, 2, 3), "a")
        self.assertEqual(rooms.read(3, 2, 3), "t")
        self.assertEqual(rooms.read(4, 2, 3), "s")

    def test_read_and_write_line_2(self):
        rooms = Rooms()
        rooms.write_line(-5, -5, -5, "12345", 2, -1, 1)

        self.assertEqual(rooms.read(-5, -5, -5), "1")
        self.assertEqual(rooms.read(-3, -6, -4), "2")
        self.assertEqual(rooms.read(-1, -7, -3), "3")
        self.assertEqual(rooms.read(1, -8, -2), "4")
        self.assertEqual(rooms.read(3, -9, -1), "5")

    def test_bad_write_not_ascii(self):
        rooms = Rooms()
        rooms.write_line(44, 45, 46, "@")
        for character in range(256, 500):
            self.assertRaises(RoomsError, rooms.write, 44, 45, 46, chr(character))
        self.assertEqual(rooms.read(44, 45, 46), "@")

    def test_bad_write_not_character(self):
        rooms = Rooms()
        rooms.write(440, 450, 460, "$")
        self.assertRaises(RoomsError, rooms.write, 440, 450, 460, "@@")
        self.assertEqual(rooms.read(440, 450, 460), "$")

    def test_set_floor_names(self):
        rooms = Rooms()

        self.assertIsNone(rooms.get_floor_level("cats"))
        self.assertIsNone(rooms.get_floor_name(3))

        rooms.set_floor_name(3, "cats")
        self.assertEqual(rooms.get_floor_level("cats"), 3)
        self.assertEqual(rooms.get_floor_name(3), "cats")

        rooms.set_floor_name(4, "cats")
        self.assertIsNone(rooms.get_floor_name(3))
        self.assertEqual(rooms.get_floor_level("cats"), 4)
        self.assertEqual(rooms.get_floor_name(4), "cats")

        rooms.set_floor_name(3)
        self.assertIsNone(rooms.get_floor_name(3))
        self.assertEqual(rooms.get_floor_level("cats"), 4)
        self.assertEqual(rooms.get_floor_name(4), "cats")

        rooms.set_floor_name(4)
        self.assertIsNone(rooms.get_floor_level("cats"))
        self.assertIsNone(rooms.get_floor_name(3))
        self.assertIsNone(rooms.get_floor_name(4))

    def test_set_floor_bad_name(self):
        rooms = Rooms()
        self.assertRaises(RoomsError, rooms.set_floor_name, -44, "24354@345")

    def test_set_hallway_name_and_find_hallway_location(self):
        rooms = Rooms()
        rooms.set_hallway_name(45, 1, "cats")
        rooms.set_hallway_name(500, 1, "cats2")
        rooms.set_hallway_name(0, 1, "cats")
        rooms.set_hallway_name(-45, 1, "12345")
        rooms.set_hallway_name(-70, 1)
        rooms.set_hallway_name(-700, 1)

        self.assertIsNone(rooms.find_hallway_location(234523452, 1))
        self.assertIsNone(rooms.find_hallway_location(501, 1))
        self.assertEqual(rooms.find_hallway_location(500, 1), 500)
        self.assertEqual(rooms.find_hallway_location(10, 1), 500)
        self.assertEqual(rooms.find_hallway_location(0, 1), 0)
        self.assertEqual(rooms.find_hallway_location(-1, 1), 0)
        self.assertEqual(rooms.find_hallway_location(-44, 1), 0)
        self.assertEqual(rooms.find_hallway_location(-45, 1), -45)
        self.assertEqual(rooms.find_hallway_location(-50, 1), -45)
        self.assertEqual(rooms.find_hallway_location(-70, 1), -70)
        self.assertEqual(rooms.find_hallway_location(-80, 1), -70)
        self.assertEqual(rooms.find_hallway_location(-700, 1), -700)
        self.assertEqual(rooms.find_hallway_location(-700283405723045, 1), -700)

    def test_find_hallway_location_no_hallways(self):
        rooms = Rooms()
        self.assertIsNone(rooms.find_hallway_location(0, -10))

    def test_find_hallway_location_single_hallway(self):
        rooms = Rooms()
        rooms.set_hallway_name(45, 10, "cats")
        self.assertIsNone(rooms.find_hallway_location(46, 10))
        self.assertEqual(rooms.find_hallway_location(45, 10), 45)
        self.assertEqual(rooms.find_hallway_location(44, 10), 45)

    def test_remove_floor(self):
        rooms = Rooms()

        rooms.write(0, -2340, 1, "$")
        rooms.write(0, 0, 1, "1")

        for x in range(256):
            for y in range(30):
                rooms.write(x, y, 0, chr(x))

        rooms.set_hallway_name(0, 0, "cats")
        rooms.set_hallway_name(5, 0)

        rooms.remove_floor(0)

        for x in range(256):
            for y in range(30):
                self.assertEqual(rooms.read(x, y, 0), " ")

        self.assertIsNone(rooms.find_hallway_location(0, 0))
        self.assertIsNone(rooms.get_hallway_name(0, 0))
        self.assertIsNone(rooms.find_hallway_location(5, 0))
        self.assertIsNone(rooms.get_hallway_name(5, 0))

    def test_remove_floor_empty(self):
        rooms = Rooms()
        rooms.remove_floor(0)
        for x in range(256):
            self.assertEqual(rooms.read(x, 0, 0), " ")
        self.assertIsNone(rooms.find_hallway_location(0, 0))

    def test_get_hallway_name_and_location(self):
        rooms = Rooms()
        self.assertIsNone(rooms.get_hallway_name(0, 0))
        self.assertIsNone(rooms.get_hallway_location(0, "cats"))

        rooms.set_hallway_name(0, 0, "cats")
        rooms.set_hallway_name(10, 0, "12345")
        rooms.set_hallway_name(100, 0, "cats")

        self.assertIsNone(rooms.get_hallway_name(0, 0))

        self.assertEqual(rooms.get_hallway_name(10, 0), "12345")
        self.assertEqual(rooms.get_hallway_location(0, "12345"), 10)

        self.assertEqual(rooms.get_hallway_name(100, 0), "cats")
        self.assertEqual(rooms.get_hallway_location(0, "cats"), 100)

    def test_get_next_and_past_hallway_location(self):
        rooms = Rooms()

        rooms.set_hallway_name(101, 0, "cats")
        rooms.set_hallway_name(11, 0, "12345")
        rooms.set_hallway_name(1, 0, "6")

        self.assertIsNone(rooms.get_next_hallway_location(101, 0))
        self.assertEqual(rooms.get_past_hallway_location(101, 0), 11)
        self.assertEqual(rooms.get_next_hallway_location(11, 0), 101)
        self.assertEqual(rooms.get_past_hallway_location(11, 0), 1)
        self.assertEqual(rooms.get_next_hallway_location(1, 0), 11)
        self.assertIsNone(rooms.get_past_hallway_location(1, 0))

        rooms.remove_hallway(11, 0)
        rooms.set_hallway_name(-100, 0)

        self.assertIsNone(rooms.get_next_hallway_location(101, 0))
        self.assertEqual(rooms.get_past_hallway_location(101, 0), 1)
        self.assertEqual(rooms.get_next_hallway_location(1, 0), 101)
        self.assertEqual(rooms.get_past_hallway_location(1, 0), -100)
        self.assertEqual(rooms.get_next_hallway_location(-100, 0), 1)
        self.assertIsNone(rooms.get_past_hallway_location(-100, 0))

        self.assertIsNone(rooms.get_next_hallway_location(11, 0), 1)
        self.assertEqual(rooms.get_past_hallway_location(11, 0), 1)

    def test_get_next_and_past_hallway_empty(self):
        rooms = Rooms()

        self.assertIsNone(rooms.get_next_hallway_location(10, 0))
        self.assertIsNone(rooms.get_past_hallway_location(-10, 0))

    def test_duplicate_floor(self):
        rooms = Rooms()

        rooms.write(0, -2340, 1, "$")
        rooms.write(0, 0, 1, "1")

        for x in range(256):
            for y in range(30):
                rooms.write(x, y, 0, chr(x))

        rooms.set_hallway_name(0, 0, "cats")
        rooms.set_hallway_name(5, 0)
        rooms.set_hallway_name(45, 1, "1234")

        rooms.duplicate_floor(0, 1)

        self.assertEqual(rooms.read(0, -2340, 1), " ")

        for x in range(256):
            for y in range(30):
                self.assertEqual(rooms.read(x, y, 0), rooms.read(x, y, 1))

        self.assertEqual(rooms.find_hallway_location(0, 1), 0)
        self.assertEqual(rooms.get_hallway_name(0, 1), "cats")
        self.assertEqual(rooms.find_hallway_location(5, 1), 5)
        self.assertIsNone(rooms.get_hallway_name(5, 1))
        self.assertIsNone(rooms.find_hallway_location(45, 1))

    def test_duplicate_floor_empty(self):
        rooms = Rooms()
        rooms.duplicate_floor(4, 50)

        for x in range(256):
            for y in range(30):
                self.assertEqual(rooms.read(x, y, 4), rooms.read(x, y, 50))

        self.assertIsNone(rooms.find_hallway_location(-1234, 50))
