"""
Copyright 2021 Charles McMarrow
"""

# built-in
import unittest

# backrooms
from tests import test_files
from backrooms import backrooms


class BackroomsAPITests(unittest.TestCase):
    def test_string(self):
        portal = backrooms.backrooms_api(test_files.get_path("hello.brs"),
                                         sys_output=False,
                                         catch_output=True,
                                         lost_count=1000,
                                         lost_rule_count=1000)
        portal()
        stream = portal.get_output_stream()
        self.assertEqual(len(stream), 1)
        self.assertEqual(stream[0], "hello")

    def test_string_handler(self):
        brs = """
        ~GATE
        /rs"hello"e~ha
        """
        portal = backrooms.backrooms_api(backrooms.StringHandler("hello", brs),
                                         sys_output=False,
                                         catch_output=True,
                                         lost_count=1000,
                                         lost_rule_count=1000)
        portal()
        stream = portal.get_output_stream()
        self.assertEqual(len(stream), 1)
        self.assertEqual(stream[0], "hello")

    def test_file_handler(self):
        portal = backrooms.backrooms_api(backrooms.FileHandler(test_files.get_path("hello.brs")),
                                         sys_output=False,
                                         catch_output=True,
                                         lost_count=1000,
                                         lost_rule_count=1000)
        portal()
        stream = portal.get_output_stream()
        self.assertEqual(len(stream), 1)
        self.assertEqual(stream[0], "hello")

    def test_handlers(self):
        handler = backrooms.FileHandler(test_files.get_path("hello.brs"))
        portal = backrooms.backrooms_api(backrooms.Handlers(handler),
                                         sys_output=False,
                                         catch_output=True,
                                         lost_count=1000,
                                         lost_rule_count=1000)
        portal()
        stream = portal.get_output_stream()
        self.assertEqual(len(stream), 1)
        self.assertEqual(stream[0], "hello")
