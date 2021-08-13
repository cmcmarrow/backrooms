"""
Copyright 2021 Charles McMarrow
"""

# built-in
import unittest

# backrooms
from tests.full_test_runner import full_test


class TestHardVectors(unittest.TestCase):
    def test_insert_remove(self):
        stream = full_test("hard_vector_insert_remove.brs", lost_count=220000).get_output_stream()
        self.assertEqual(len(stream), 204)
        stream.reverse()
        items = []
        for item in range(102, 2, -1):
            items.append(item)
        items.insert(0, 666666)
        items.insert(6, "StackFrame")
        items.append("cats")

        for item in items:
            self.assertEqual(stream.pop(), item)

        for item in range(102, 2, -1):
            self.assertEqual(stream.pop(), item)

        self.assertEqual(stream.pop(), "StackBottom")
        self.assertFalse(len(stream))

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

    def test_find_insert(self):
        stream = full_test("hard_vector_find_insert.brs", lost_count=120000).get_output_stream()
        self.assertEqual(len(stream), 31)
        self.assertEqual(stream.pop(), "StackBottom")
        last_item = stream.pop()
        stream.reverse()
        for item in stream:
            self.assertLessEqual(last_item, item)
            last_item = item
