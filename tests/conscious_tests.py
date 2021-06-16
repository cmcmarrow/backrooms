"""
Copyright 2021 Charles McMarrow
"""

# built-in
import unittest

# backrooms
from backrooms import conscious


class ConsciousTest(unittest.TestCase):
    def test_default(self):
        this_conscious = conscious.Conscious()
        self.assertIsInstance(this_conscious, dict)
        self.assertIsNone(this_conscious[conscious.R0])
        self.assertIsNone(this_conscious[conscious.RE])
        self.assertEqual(this_conscious[conscious.PC_X], 0)
        self.assertEqual(this_conscious[conscious.PC_Y], 0)
        self.assertEqual(this_conscious[conscious.PC_FLOOR], 0)
        self.assertIsNone(this_conscious[conscious.RE])
        self.assertEqual(this_conscious[conscious.PC_V_X], 1)
        self.assertEqual(this_conscious[conscious.PC_V_Y], 0)
        self.assertEqual(this_conscious[conscious.PC_V_FLOOR], 0)
        self.assertIsNone(this_conscious[conscious.ID])

    def test_id_kwarg(self):
        this_conscious = conscious.Conscious(ID=48)
        self.assertEqual(this_conscious[conscious.ID], 48)

    def test_step_and_at(self):
        this_conscious = conscious.Conscious()
        self.assertEqual(this_conscious.at(), (0, 0, 0))
        this_conscious.step()
        self.assertEqual(this_conscious.at(), (1, 0, 0))
        this_conscious.step()
        self.assertEqual(this_conscious.at(), (2, 0, 0))
        this_conscious[conscious.PC_V_X] = -1
        this_conscious[conscious.PC_V_Y] = 2
        this_conscious[conscious.PC_V_FLOOR] = 1
        this_conscious.step()
        self.assertEqual(this_conscious.at(), (1, 2, 1))
        this_conscious.step()
        self.assertEqual(this_conscious.at(), (0, 4, 2))
