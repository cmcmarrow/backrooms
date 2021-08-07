"""
Copyright 2021 Charles McMarrow
"""

# built-in
import unittest

# backrooms
from tests.full_test_runner import full_test


class TestHardVector(unittest.TestCase):
    def test_rwap(self):
        stream = full_test("hard_vector_rwap.brs", lost_count=140000).get_output_stream()
        self.assertEqual(len(stream), 253)
        stream.reverse()
        self.assertEqual(100, stream.pop())
        for item in range(102, 2, -1):
            self.assertEqual(item, stream.pop())
        for item in range(3, 103):
            if item == 69:
                self.assertEqual(666666, stream.pop())
            elif item == 98:
                self.assertEqual("cats", stream.pop())
            else:
                self.assertEqual(item, stream.pop())
        self.assertEqual(0, stream.pop())
        for _ in range(50):
            self.assertIsNone(stream.pop())
        self.assertEqual("StackBottom", stream.pop())
        self.assertFalse(len(stream))
