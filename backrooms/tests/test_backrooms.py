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


class TestBackrooms(unittest.TestCase):
    def test_init(self):
        self.assertIsInstance(Backrooms(), Backrooms)

    def test_init_2(self):
        self.assertIsInstance(Backrooms("Name",
                                        {BackRoomsCord(4): "A"},
                                        [Hallway(cord=BackRoomsCord(4)),
                                         Hallway(cord=BackRoomsCord(-4)),
                                         Hallway(cord=BackRoomsCord(0))]), Backrooms)

    def test_bad_init_name(self):
        self.assertRaises(BackRoomsError,
                          Backrooms,
                          " ",
                          {BackRoomsCord(4): "A"},
                          [Hallway(cord=BackRoomsCord(4)),
                           Hallway(cord=BackRoomsCord(-4)),
                           Hallway(cord=BackRoomsCord(0))])

    def test_bad_init_raw_backrooms(self):
        self.assertRaises(BackRoomsError,
                          Backrooms,
                          "Name",
                          [BackRoomsCord(4), "A"],
                          [Hallway(cord=BackRoomsCord(4)),
                           Hallway(cord=BackRoomsCord(-4)),
                           Hallway(cord=BackRoomsCord(0))])

    def test_bad_init_cord(self):
        self.assertRaises(BackRoomsError,
                          Backrooms,
                          "Name",
                          {"A", "A"},
                          [Hallway(cord=BackRoomsCord(4)),
                           Hallway(cord=BackRoomsCord(-4)),
                           Hallway(cord=BackRoomsCord(0))])

    def test_bad_init_entity(self):
        self.assertRaises(BackRoomsError,
                          Backrooms,
                          "Name",
                          {BackRoomsCord(4), "AA"},
                          [Hallway(cord=BackRoomsCord(4)),
                           Hallway(cord=BackRoomsCord(-4)),
                           Hallway(cord=BackRoomsCord(0))])

    def test_bad_init_entity_2(self):
        self.assertRaises(BackRoomsError,
                          Backrooms,
                          "Name",
                          {BackRoomsCord(4), ""},
                          [Hallway(cord=BackRoomsCord(4)),
                           Hallway(cord=BackRoomsCord(-4)),
                           Hallway(cord=BackRoomsCord(0))])

    def test_bad_init_entity_3(self):
        self.assertRaises(BackRoomsError,
                          Backrooms,
                          "Name",
                          {BackRoomsCord(4), None},
                          [Hallway(cord=BackRoomsCord(4)),
                           Hallway(cord=BackRoomsCord(-4)),
                           Hallway(cord=BackRoomsCord(0))])

    def test_bad_init_hallways(self):
        self.assertRaises(BackRoomsError,
                          Backrooms,
                          "Name",
                          {BackRoomsCord(4), "A"},
                          {Hallway(cord=BackRoomsCord(4)),
                           Hallway(cord=BackRoomsCord(-4)),
                           Hallway(cord=BackRoomsCord(0))})

    def test_bad_init_hallways_2(self):
        self.assertRaises(BackRoomsError,
                          Backrooms,
                          "Name",
                          {BackRoomsCord(4), "A"},
                          [Hallway(cord=BackRoomsCord(4)),
                           Hallway(cord=BackRoomsCord(4)),
                           Hallway(cord=BackRoomsCord(0))])

    def test_bad_init_hallway(self):
        self.assertRaises(BackRoomsError,
                          Backrooms,
                          "Name",
                          {BackRoomsCord(4), "A"},
                          [None,
                           Hallway(cord=BackRoomsCord(-4)),
                           Hallway(cord=BackRoomsCord(0))])

    def test_name(self):
        self.assertEqual(Backrooms("Name").name, "Name")

    def test_name_blank(self):
        self.assertIsNone(Backrooms().name)

    def test_hallways(self):
        self.assertIsInstance(Backrooms().hallways, tuple)

    def test_hallways_order(self):
        backrooms = Backrooms("Name",
                              {BackRoomsCord(4): "A"},
                              [Hallway(cord=BackRoomsCord(4)),
                               Hallway(cord=BackRoomsCord(-4)),
                               Hallway(cord=BackRoomsCord(23)),
                               Hallway(cord=BackRoomsCord(-2300)),
                               Hallway(cord=BackRoomsCord(230))])

        hallways = backrooms.hallways
        last = None
        for hallway in hallways:
            if last is not None:
                self.assertLess(hallway.x, last)
            last = hallway.x

    def test_read_write(self):
        cord_1 = BackRoomsCord(4, 5)
        cord_2 = BackRoomsCord(-40000000000000000000000000000000,
                               5000000000000000000000000000000000)
        cord_3 = BackRoomsCord(444,
                               -101)
        backrooms = Backrooms("Name",
                              {cord_1: "A"},
                              [Hallway(cord=BackRoomsCord(4)),
                               Hallway(cord=BackRoomsCord(-4))])

        self.assertEqual(backrooms.read(cord_1), "A")
        backrooms.write(cord_1, "@")
        self.assertEqual(backrooms.read(cord_1), "@")

        self.assertEqual(backrooms.read(cord_2), " ")
        backrooms.write(cord_2, "V")
        self.assertEqual(backrooms.read(cord_2), "V")

        backrooms.write(cord_3, "L")
        self.assertEqual(backrooms.read(cord_3), "L")

    def test_bad_read(self):
        backrooms = Backrooms("Name",
                              {BackRoomsCord(4): "A"},
                              [Hallway(cord=BackRoomsCord(4)),
                               Hallway(cord=BackRoomsCord(-4))])

        self.assertRaises(BackRoomsError, backrooms.read, 78)

    def test_bad_write_cord(self):
        backrooms = Backrooms("Name",
                              {BackRoomsCord(4): "A"},
                              [Hallway(cord=BackRoomsCord(4)),
                               Hallway(cord=BackRoomsCord(-4))])

        self.assertRaises(BackRoomsError, backrooms.write, 78, "A")

    def test_bad_write_entity(self):
        backrooms = Backrooms("Name",
                              {BackRoomsCord(4): "A"},
                              [Hallway(cord=BackRoomsCord(4)),
                               Hallway(cord=BackRoomsCord(-4))])

        self.assertRaises(BackRoomsError, backrooms.write, BackRoomsCord(4), 78)

    def test_bad_write_entity_2(self):
        backrooms = Backrooms("Name",
                              {BackRoomsCord(4): "A"},
                              [Hallway(cord=BackRoomsCord(4)),
                               Hallway(cord=BackRoomsCord(-4))])

        self.assertRaises(BackRoomsError, backrooms.write, BackRoomsCord(4), "")

    def test_bad_write_entity_3(self):
        backrooms = Backrooms("Name",
                              {BackRoomsCord(4): "A"},
                              [Hallway(cord=BackRoomsCord(4)),
                               Hallway(cord=BackRoomsCord(-4))])

        self.assertRaises(BackRoomsError, backrooms.write, BackRoomsCord(4), "AA")

    def test_is_vacant(self):
        cord_1 = BackRoomsCord(4, 5)
        backrooms = Backrooms("Name",
                              {cord_1: "A"},
                              [Hallway(cord=BackRoomsCord(4)),
                               Hallway(cord=BackRoomsCord(-4))])

        self.assertFalse(backrooms.is_vacant(cord_1))
        self.assertTrue(backrooms.is_vacant(BackRoomsCord(400, 691)))

    def test_is_vacant_write(self):
        cord_1 = BackRoomsCord(40, 59)
        backrooms = Backrooms("Name",
                              {BackRoomsCord(42): "A"},
                              [Hallway(cord=BackRoomsCord(4)),
                               Hallway(cord=BackRoomsCord(-4))])

        self.assertTrue(backrooms.is_vacant(cord_1))
        self.assertTrue(backrooms.is_vacant(cord_1))
        backrooms.write(cord_1, " ")
        self.assertFalse(backrooms.is_vacant(cord_1))

    def test_get_hallway(self):
        func = Hallway("FUNC", cord=BackRoomsCord(23))
        backrooms = Backrooms("Name",
                              {BackRoomsCord(4): "A"},
                              [Hallway("MAIN", BackRoomsCord(4)),
                               Hallway(cord=BackRoomsCord(-4)),
                               func,
                               Hallway(cord=BackRoomsCord(-2300)),
                               Hallway(cord=BackRoomsCord(230))])

        self.assertIs(backrooms.get_hallway("FUNC"), func)

    def test_get_hallway_none(self):
        backrooms = Backrooms("Name",
                              {BackRoomsCord(4): "A"},
                              [Hallway("MAIN", BackRoomsCord(4)),
                               Hallway(cord=BackRoomsCord(-4)),
                               Hallway("FUNC", cord=BackRoomsCord(23)),
                               Hallway(cord=BackRoomsCord(-2300)),
                               Hallway(cord=BackRoomsCord(230))])

        self.assertIsNone(backrooms.get_hallway("FUNc"))

    def test_bad_hallway(self):
        backrooms = Backrooms("Name",
                              {BackRoomsCord(4): "A"},
                              [Hallway("MAIN", BackRoomsCord(4)),
                               Hallway(cord=BackRoomsCord(-4)),
                               Hallway("FUNC", cord=BackRoomsCord(23)),
                               Hallway(cord=BackRoomsCord(-2300)),
                               Hallway(cord=BackRoomsCord(230))])

        self.assertRaises(BackRoomsError, backrooms.get_hallway, None)

    def test_get_higher_hallway(self):
        higher = Hallway(cord=BackRoomsCord(-4))
        func = Hallway("FUNC", cord=BackRoomsCord(-8))
        backrooms = Backrooms("Name",
                              {BackRoomsCord(4): "A"},
                              [Hallway("MAIN", BackRoomsCord(4)),
                               Hallway(cord=BackRoomsCord(-2300)),
                               func,
                               higher,
                               Hallway(cord=BackRoomsCord(230))])
        self.assertIs(backrooms.get_higher_hallway(func), higher)

    def test_get_higher_hallway_top(self):
        func = Hallway("FUNC", cord=BackRoomsCord(99999))
        backrooms = Backrooms("Name",
                              {BackRoomsCord(4): "A"},
                              [Hallway("MAIN", BackRoomsCord(4)),
                               Hallway(cord=BackRoomsCord(-2300)),
                               func,
                               Hallway(cord=BackRoomsCord(230))])
        self.assertIsNone(backrooms.get_higher_hallway(func))

    def test_bad_get_higher_hallway(self):
        backrooms = Backrooms("Name",
                              {BackRoomsCord(4): "A"},
                              [Hallway("MAIN", BackRoomsCord(4)),
                               Hallway(cord=BackRoomsCord(-2300)),
                               Hallway(cord=BackRoomsCord(230))])
        self.assertRaises(BackRoomsError, backrooms.get_higher_hallway, None)

    def test_bad_get_higher_hallway_unidentified(self):
        backrooms = Backrooms("Name",
                              {BackRoomsCord(4): "A"},
                              [Hallway("MAIN", BackRoomsCord(4)),
                               Hallway(cord=BackRoomsCord(-2300)),
                               Hallway(cord=BackRoomsCord(230))])
        self.assertRaises(BackRoomsError, backrooms.get_higher_hallway, Hallway("mAIN", BackRoomsCord(4)))

    def test_get_lower_hallway(self):
        lower = Hallway(cord=BackRoomsCord(-9))
        func = Hallway("FUNC", cord=BackRoomsCord(-8))
        backrooms = Backrooms("Name",
                              {BackRoomsCord(4): "A"},
                              [Hallway("MAIN", BackRoomsCord(4)),
                               func,
                               Hallway(cord=BackRoomsCord(-2300)),
                               lower,
                               Hallway(cord=BackRoomsCord(230))])
        self.assertIs(backrooms.get_lower_hallway(func), lower)

    def test_get_lower_hallway_bottom(self):
        func = Hallway("FUNC", cord=BackRoomsCord(-99999))
        backrooms = Backrooms("Name",
                              {BackRoomsCord(4): "A"},
                              [Hallway("MAIN", BackRoomsCord(4)),
                               Hallway(cord=BackRoomsCord(-2300)),
                               func,
                               Hallway(cord=BackRoomsCord(230))])
        self.assertIsNone(backrooms.get_lower_hallway(func))

    def test_bad_get_lower_hallway(self):
        backrooms = Backrooms("Name",
                              {BackRoomsCord(4): "A"},
                              [Hallway("MAIN", BackRoomsCord(4)),
                               Hallway(cord=BackRoomsCord(-2300)),
                               Hallway(cord=BackRoomsCord(230))])
        self.assertRaises(BackRoomsError, backrooms.get_lower_hallway, None)

    def test_bad_get_lower_hallway_unidentified(self):
        backrooms = Backrooms("Name",
                              {BackRoomsCord(4): "A"},
                              [Hallway("MAIN", BackRoomsCord(4)),
                               Hallway(cord=BackRoomsCord(-2300)),
                               Hallway(cord=BackRoomsCord(230))])
        self.assertRaises(BackRoomsError, backrooms.get_lower_hallway, Hallway("mAIN", BackRoomsCord(4)))

    def test_parallel(self):
        cord_1 = BackRoomsCord(40, 59)
        backrooms = Backrooms("Name",
                              {cord_1: "A"},
                              [Hallway("MAIN", BackRoomsCord(4)),
                               Hallway(cord=BackRoomsCord(-2300)),
                               Hallway(cord=BackRoomsCord(230))])

        new_backrooms = backrooms.parallel("Name2")
        self.assertEqual(new_backrooms.name, "Name2")
        self.assertEqual(new_backrooms.read(cord_1), "A")
        self.assertEqual(len(new_backrooms.hallways), 3)

    def test_parallel_none(self):
        cord_1 = BackRoomsCord(40, 59)
        backrooms = Backrooms("Name",
                              {cord_1: "A"},
                              [Hallway("MAIN", BackRoomsCord(4)),
                               Hallway(cord=BackRoomsCord(-2300)),
                               Hallway(cord=BackRoomsCord(230))])

        new_backrooms = backrooms.parallel()
        self.assertIsNone(new_backrooms.name)
