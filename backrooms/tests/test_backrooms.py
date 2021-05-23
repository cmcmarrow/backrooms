"""
Copyright 2021 Charles McMarrow
"""

import unittest
from backrooms.backrooms import*


class TestBackRoomsCord(unittest.TestCase):
    def test_init(self):
        self.assertIsInstance(BackRoomsCord(), BackRoomsCord)

    def test_init_x(self):
        self.assertIsInstance(BackRoomsCord(x=800), BackRoomsCord)

    def test_init_y(self):
        self.assertIsInstance(BackRoomsCord(y=45), BackRoomsCord)

    def test_init_x_y(self):
        self.assertIsInstance(BackRoomsCord(3, -4), BackRoomsCord)

    def test_bad_init_x(self):
        self.assertRaises(BackRoomsError, BackRoomsCord, x=None)

    def test_bad_init_y(self):
        self.assertRaises(BackRoomsError, BackRoomsCord, y=complex(3, 4))

    def test_bad_init_x_y(self):
        self.assertRaises(BackRoomsError, BackRoomsCord, x="23", y=4.0)

    def test_repr(self):
        self.assertIsInstance(repr(BackRoomsCord(3, -4)), str)

    def test_hash(self):
        self.assertIsInstance(hash(BackRoomsCord(30, -40)), int)

    def test_eq(self):
        self.assertEqual(BackRoomsCord(30, -40), BackRoomsCord(30, -40))

    def test_eq_2(self):
        self.assertEqual(BackRoomsCord(), BackRoomsCord())

    def test_nq(self):
        self.assertNotEqual(BackRoomsCord(30, -41), BackRoomsCord(30, -40))

    def test_nq_2(self):
        self.assertNotEqual(BackRoomsCord(30, -41), BackRoomsCord())

    def test_x(self):
        self.assertEqual(BackRoomsCord(44, -41).x, 44)

    def test_x_2(self):
        self.assertEqual(BackRoomsCord(404).x, 404)

    def test_y(self):
        self.assertEqual(BackRoomsCord(44, -41).y, -41)

    def test_y_2(self):
        self.assertEqual(BackRoomsCord(y=-404).y, -404)

    def test_shift(self):
        cord = BackRoomsCord(100, 90)
        new_cord = cord.shift(y=45)

        self.assertIsNot(cord, new_cord)

        self.assertEqual(new_cord.x, 100)
        self.assertEqual(new_cord.y, 135)

    def test_shift_2(self):
        cord = BackRoomsCord(100, -90)
        new_cord = cord.shift(20, 44)

        self.assertIsNot(cord, new_cord)

        self.assertEqual(new_cord.x, 120)
        self.assertEqual(new_cord.y, -46)

    def test_bad_shift(self):
        cord = BackRoomsCord(100, -90)
        self.assertRaises(BackRoomsError, cord.shift, 45, -4.66)


class TestHallway(unittest.TestCase):
    def test_init(self):
        self.assertIsInstance(Hallway(), Hallway)

    def test_init_2(self):
        self.assertIsInstance(Hallway("territory", BackRoomsCord(4)), Hallway)

    def test_bad_init_name(self):
        self.assertRaises(BackRoomsError, Hallway, " ")

    def test_bad_init_cord(self):
        self.assertRaises(BackRoomsError, Hallway, cord=45)

    def test_bad_init_cord_y(self):
        self.assertRaises(BackRoomsError, Hallway, cord=BackRoomsCord(45, 3))

    def test_repr(self):
        self.assertIsInstance(repr(Hallway("TerrITory", BackRoomsCord(44))), str)

    def test_hash(self):
        self.assertIsInstance(hash(Hallway("ITs", BackRoomsCord(-44))), int)

    def test_eq(self):
        self.assertFalse(Hallway() == Hallway(cord=BackRoomsCord(-100)))

    def test_eq_2(self):
        self.assertTrue(Hallway(cord=BackRoomsCord(110)) == Hallway(cord=BackRoomsCord(110)))

    def test_nq(self):
        self.assertTrue(Hallway() != Hallway(cord=BackRoomsCord(-100)))

    def test_nq_2(self):
        self.assertFalse(Hallway(cord=BackRoomsCord(110)) != Hallway(cord=BackRoomsCord(110)))

    def test_gt(self):
        self.assertTrue(Hallway() > Hallway(cord=BackRoomsCord(-100)))

    def test_gt_2(self):
        self.assertFalse(Hallway(cord=BackRoomsCord(110)) > Hallway(cord=BackRoomsCord(120)))

    def test_lt(self):
        self.assertFalse(Hallway() < Hallway(cord=BackRoomsCord(-100)))

    def test_lt_2(self):
        self.assertTrue(Hallway(cord=BackRoomsCord(110)) < Hallway(cord=BackRoomsCord(120)))

    def test_cord(self):
        self.assertEqual(Hallway("territory", BackRoomsCord(4)).cord, BackRoomsCord(4))

    def test_name(self):
        self.assertEqual(Hallway("territory", BackRoomsCord(4)).name, "territory")

    def test_name_none(self):
        self.assertIsNone(Hallway().name)

    def test_x(self):
        self.assertEqual(Hallway(None, BackRoomsCord(4)).x, 4)
