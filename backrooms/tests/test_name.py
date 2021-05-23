"""
Copyright 2021 Charles McMarrow
"""

import unittest
from backrooms.name import *


class TestNameChars(unittest.TestCase):
    def test_name_chars(self):
        self.assertIsInstance(NAME_CHARS, set)
        for c in NAME_CHARS:
            self.assertIsInstance(c, str)
            self.assertEqual(len(c), 1)


class TestIsName(unittest.TestCase):
    def test_is_name(self):
        self.assertTrue(is_name("RUN"))

    def test_is_name_2(self):
        self.assertTrue(is_name("fr0m_"))

    def test_bad_is_name(self):
        self.assertFalse(is_name("<<<THEM>>>"))

    def test_bad_is_name_empty(self):
        self.assertFalse(is_name(""))
