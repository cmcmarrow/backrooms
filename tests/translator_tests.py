"""
Copyright 2021 Charles McMarrow
"""

# built-in
import unittest

# backrooms
from backrooms.translator import Handler, translator, StringHandler, FileHandler, Handlers, TranslatorError

# test
from . import test_files


class TestHandler(unittest.TestCase):
    def test_is_open_and_close(self):
        handler = Handler("test")
        self.assertTrue(handler.is_open())
        self.assertTrue(handler.is_open())
        for _ in range(2):
            handler.close()
            self.assertFalse(handler.is_open())
            self.assertFalse(handler.is_open())


class TestFileHandler(unittest.TestCase):
    def test_file_handler(self):
        handler = FileHandler(test_files.get_path("test_file_handler.brs"))
        self.assertEqual(handler.get_name(), "test_file_handler")
        self.assertIsInstance(iter(handler), FileHandler)

        self.assertEqual(next(handler), "TEST")
        self.assertEqual(next(handler), "123")
        self.assertEqual(next(handler), "")
        self.assertEqual(next(handler), "tbs")
        self.assertEqual(next(handler), " f")

        self.assertRaises(StopIteration, next, handler)

    def test_file_handler_2(self):
        handler = FileHandler(test_files.get_path("test_file_handler"))
        self.assertEqual(handler.get_name(), "test_file_handler")
        self.assertIsInstance(iter(handler), FileHandler)

        self.assertEqual(next(handler), "TEST")
        self.assertEqual(next(handler), "123")
        self.assertEqual(next(handler), "")
        self.assertEqual(next(handler), "tbs")
        self.assertEqual(next(handler), " f2")

        self.assertRaises(StopIteration, next, handler)


_STRING_HANDLER_TEST_STRING = """TEST
123

\t tbs
 s"""


class TestStringHandler(unittest.TestCase):
    def test_string_handler(self):
        handler = StringHandler("test", _STRING_HANDLER_TEST_STRING)

        self.assertEqual(handler.get_name(), "test")
        self.assertIsInstance(iter(handler), StringHandler)

        self.assertEqual(next(handler), "TEST")
        self.assertEqual(next(handler), "123")
        self.assertEqual(next(handler), "")
        self.assertEqual(next(handler), "\t tbs")
        self.assertEqual(next(handler), " s")

        self.assertRaises(StopIteration, next, handler)


class TestHandlers(unittest.TestCase):
    def test_handlers_init(self):
        self.assertIsInstance(Handlers(StringHandler("Main", "")), Handlers)

    def test_handlers_init_2(self):
        self.assertIsInstance(Handlers(
                              StringHandler("Main", ""),
                              ((StringHandler("12", ""), StringHandler("123", "$")),
                               (StringHandler("123", "%"),))), Handlers)

    def test_handlers_init_error(self):
        self.assertRaises(TranslatorError,
                          Handlers,
                          StringHandler("Main", ""),
                          ((StringHandler("123", ""), StringHandler("123", "$")),))

    def test_handlers(self):
        handlers = Handlers(StringHandler("Main", "test"),
                            ((StringHandler("12", "12\n"), StringHandler("123", "66\n55")),
                            (StringHandler("1235", "%\n5\n334"),)))

        handlers.include("1235")
        handlers.include("12")
        handlers.include("123")

        self.assertIsInstance(iter(handlers), Handlers)

        self.assertTrue(bool(handlers))

        self.assertEqual(handlers.get_name(), "Main")
        self.assertIsNone(handlers.get_line_number())

        self.assertEqual(next(handlers), "test")
        self.assertEqual(handlers.get_name(), "Main")
        self.assertEqual(handlers.get_line_number(), 0)

        self.assertEqual(next(handlers), "%")
        self.assertEqual(handlers.get_name(), "1235")
        self.assertEqual(handlers.get_line_number(), 0)
        self.assertEqual(next(handlers), "5")
        self.assertEqual(handlers.get_name(), "1235")
        self.assertEqual(handlers.get_line_number(), 1)
        self.assertEqual(next(handlers), "334")
        self.assertEqual(handlers.get_name(), "1235")
        self.assertEqual(handlers.get_line_number(), 2)

        self.assertTrue(bool(handlers))

        self.assertEqual(next(handlers), "12")
        self.assertEqual(handlers.get_name(), "12")
        self.assertEqual(handlers.get_line_number(), 0)
        self.assertEqual(next(handlers), "")
        self.assertEqual(handlers.get_name(), "12")
        self.assertEqual(handlers.get_line_number(), 1)

        self.assertEqual(next(handlers), "66")
        self.assertEqual(handlers.get_name(), "123")
        self.assertEqual(handlers.get_line_number(), 0)

        self.assertTrue(bool(handlers))

        self.assertEqual(next(handlers), "55")
        self.assertEqual(handlers.get_name(), "123")
        self.assertEqual(handlers.get_line_number(), 1)

        self.assertTrue(bool(handlers))

        self.assertRaises(StopIteration, next, iter(handlers))
        self.assertFalse(bool(handlers))

    def test_handlers_empty_handler(self):
        handlers = Handlers(StringHandler("Main", ""),
                            ((StringHandler("12", ""), StringHandler("123", "$$\n55")),
                            (StringHandler("123", "%"),)))

        handlers.include("12")
        handlers.include("123")

        self.assertEqual(handlers.get_name(), "Main")
        self.assertIsNone(handlers.get_line_number())
        self.assertEqual(next(handlers), "")
        self.assertEqual(handlers.get_name(), "Main")
        self.assertEqual(handlers.get_line_number(), 0)
        self.assertEqual(next(handlers), "")
        self.assertEqual(handlers.get_name(), "12")
        self.assertEqual(handlers.get_line_number(), 0)
        self.assertEqual(next(handlers), "$$")
        self.assertEqual(next(handlers), "55")

    def test_missing_include(self):
        handlers = Handlers(StringHandler("Main", ""))

        self.assertRaises(TranslatorError, handlers.include, "math")


class TranslatorTest(unittest.TestCase):
    def test_row(self):
        rooms = translator(Handlers(StringHandler("Main", "/test\n/1234")))
        for spot, character in enumerate("test"):
            self.assertEqual(rooms.read(spot, 0, 0), character)

        for spot, character in enumerate("1234"):
            self.assertEqual(rooms.read(spot, -1, 0), character)

    def test_row_error(self):
        self.assertRaises(TranslatorError,
                          translator,
                          Handlers(StringHandler("Main", "/cats" + chr(500))))

    def test_comment(self):
        rooms = translator(Handlers(StringHandler("Main", "#Comment\n# test")))
        self.assertEqual(rooms.read(0, 0, 0), " ")

    def test_hallway(self):
        rooms = translator(Handlers(StringHandler("Main",
                                                  """
                                                  ~Gate
                                                  ~Gate2
                                                  /
                                                  ~Gate3
                                                  /
                                                  /
                                                  ~Gate4""")))
        self.assertEqual(rooms.get_hallway_name(0, 0), "Gate2")
        self.assertEqual(rooms.get_hallway_name(-1, 0), "Gate3")
        self.assertEqual(rooms.get_hallway_name(-3, 0), "Gate4")

    def test_hallway_none(self):
        rooms = translator(Handlers(StringHandler("Main",
                                                  """
                                                  /
                                                  ~
                                                  /
                                                  /
                                                  ~@
                                                  /
                                                  /
                                                  ~  @   """)))
        self.assertEqual(rooms.find_hallway_location(-1, 0), -1)
        self.assertEqual(rooms.find_hallway_location(-3, 0), -3)
        self.assertEqual(rooms.find_hallway_location(-5, 0), -5)

    def test_hallway_error(self):
        handlers = Handlers(StringHandler("Main",
                                          "~@@"))
        self.assertRaises(TranslatorError, translator, handlers)

    def test_hallway_error_2(self):
        handlers = Handlers(StringHandler("Main",
                                          "~^&*(^("))
        self.assertRaises(TranslatorError, translator, handlers)

    def test_hallway_error_3(self):
        handlers = Handlers(StringHandler("Main",
                                          "~Gate   @"))
        self.assertRaises(TranslatorError, translator, handlers)

    def test_hallway_error_4(self):
        handlers = Handlers(StringHandler("Main",
                                          "~Gate  asdf cats"))
        self.assertRaises(TranslatorError, translator, handlers)

    def test_floor(self):
        rooms = translator(Handlers(StringHandler("Main",
                                                  """
                                                  +Floor
                                                  +Floor2
                                                  /a
                                                  +Floor3
                                                  /b
                                                  /c
                                                  +Floor4
                                                  /d""")))

        self.assertEqual(rooms.get_floor_name(0), "Main")
        self.assertEqual(rooms.read(0, 0, 0), " ")
        self.assertEqual(rooms.get_floor_name(1), "Floor")
        self.assertEqual(rooms.get_floor_name(2), "Floor2")
        self.assertEqual(rooms.read(0, 0, 2), "a")
        self.assertEqual(rooms.get_floor_name(3), "Floor3")
        self.assertEqual(rooms.read(0, 0, 3), "b")
        self.assertEqual(rooms.read(0, -1, 3), "c")
        self.assertEqual(rooms.get_floor_name(4), "Floor4")
        self.assertEqual(rooms.read(0, 0, 4), "d")

    def test_floor_none(self):
        rooms = translator(Handlers(StringHandler("Main",
                                                  """
                                                  /a
                                                  +
                                                  /b
                                                  /c
                                                  +@
                                                  /d
                                                  /e
                                                  + @   
                                                  /f""")))

        self.assertEqual(rooms.get_floor_name(0), "Main")
        self.assertIsNone(rooms.get_floor_name(1))
        self.assertIsNone(rooms.get_floor_name(2))
        self.assertIsNone(rooms.get_floor_name(3))

    def test_floor_error(self):
        handlers = Handlers(StringHandler("Main",
                                          "+@@"))
        self.assertRaises(TranslatorError, translator, handlers)

    def test_floor_error_2(self):
        handlers = Handlers(StringHandler("Main",
                                          "+^&*(^("))
        self.assertRaises(TranslatorError, translator, handlers)

    def test_floor_error_3(self):
        handlers = Handlers(StringHandler("Main",
                                          "+FunCats   @"))
        self.assertRaises(TranslatorError, translator, handlers)

    def test_floor_error_4(self):
        handlers = Handlers(StringHandler("Main",
                                          "+Floor  asdf cats"))
        self.assertRaises(TranslatorError, translator, handlers)

    def test_include(self):
        handler = StringHandler("Main",
                                "%S2")
        handler_2 = StringHandler("S2",
                                  "/3")
        rooms = translator(Handlers(handler, ((handler_2,),)))

        self.assertEqual(rooms.get_floor_name(1), "S2")
        self.assertEqual(rooms.read(0, 0, 1), "3")

    def test_include_error(self):
        handlers = Handlers(StringHandler("Main",
                                          "%@"))
        self.assertRaises(TranslatorError, translator, handlers)

    def test_include_error_2(self):
        handlers = Handlers(StringHandler("Main",
                                          "%^&*(^("))
        self.assertRaises(TranslatorError, translator, handlers)

    def test_include_error_3(self):
        handler_2 = StringHandler("S2",
                                  "/3")

        handlers = Handlers(StringHandler("Main",
                                          "%S2   @"),
                            ((handler_2,),))
        self.assertRaises(TranslatorError, translator, handlers)

    def test_include_error_4(self):
        handler_2 = StringHandler("S2",
                                  "/3")
        handlers = Handlers(StringHandler("Main",
                                          "%S2  asdf cats"),
                            ((handler_2,),))
        self.assertRaises(TranslatorError, translator, handlers)

    def test_include_error_5(self):
        handlers = Handlers(StringHandler("Main",
                                          "%      "))
        self.assertRaises(TranslatorError, translator, handlers)

    def test_parallel(self):
        rooms = translator(Handlers(StringHandler("Main",
                                                  """
                                                  ~GATE
                                                  /1
                                                  /c
                                                  =
                                                  """)))
        self.assertEqual(rooms.get_hallway_name(0, 1), "GATE")
        self.assertEqual(rooms.read(0, 0, 1), "1")
        self.assertEqual(rooms.read(0, -1, 1), "c")

    def test_parallel_2(self):
        rooms = translator(Handlers(StringHandler("Main",
                                                  """
                                                  ~GATE
                                                  /1
                                                  /c
                                                  +
                                                  +
                                                  +
                                                  =Main
                                                  """)))
        self.assertEqual(rooms.get_hallway_name(0, 4), "GATE")
        self.assertEqual(rooms.read(0, 0, 4), "1")
        self.assertEqual(rooms.read(0, -1, 4), "c")

    def test_parallel_3(self):
        rooms = translator(Handlers(StringHandler("Main",
                                                  """
                                                  ~GATE
                                                  /1
                                                  /c
                                                  +
                                                  +
                                                  +
                                                  =Main sqrt
                                                  """)))
        self.assertEqual(rooms.get_hallway_name(0, 4), "GATE")
        self.assertEqual(rooms.read(0, 0, 4), "1")
        self.assertEqual(rooms.read(0, -1, 4), "c")
        self.assertEqual(rooms.get_floor_name(4), "sqrt")

    def test_parallel_4(self):
        rooms = translator(Handlers(StringHandler("Main",
                                                  """
                                                  +
                                                  ~GATE
                                                  /1
                                                  /c
                                                  +
                                                  +
                                                  +
                                                  =@@1 -4
                                                  """)))
        self.assertEqual(rooms.get_hallway_name(0, -4), "GATE")
        self.assertEqual(rooms.read(0, 0, -4), "1")
        self.assertEqual(rooms.read(0, -1, -4), "c")

    def test_parallel_5(self):
        rooms = translator(Handlers(StringHandler("Main",
                                                  """
                                                  ~GATE
                                                  /1
                                                  /c
                                                  =@@@@
                                                  """)))
        self.assertEqual(rooms.get_hallway_name(0, 1), "GATE")
        self.assertEqual(rooms.read(0, 0, 1), "1")
        self.assertEqual(rooms.read(0, -1, 1), "c")

    def test_parallel_error(self):
        self.assertRaises(TranslatorError,
                          translator,
                          Handlers(StringHandler("Main",
                                                 """
                                                 +C
                                                 ~GATE
                                                 /1
                                                 /c
                                                 +
                                                 +
                                                 +
                                                 =C@-1111 -4
                                                 """)))

    def test_parallel_error_2(self):
        self.assertRaises(TranslatorError,
                          translator,
                          Handlers(StringHandler("Main",
                                                 """
                                                 +C
                                                 ~GATE
                                                 /1
                                                 /c
                                                 +
                                                 +
                                                 +
                                                 =@@@@@
                                                 """)))

    def test_parallel_error_3(self):
        self.assertRaises(TranslatorError,
                          translator,
                          Handlers(StringHandler("Main",
                                                 """
                                                 +C
                                                 ~GATE
                                                 /1
                                                 /c
                                                 +
                                                 +
                                                 +
                                                 =@@@ Cats
                                                 """)))

    def test_parallel_error_4(self):
        self.assertRaises(TranslatorError,
                          translator,
                          Handlers(StringHandler("Main",
                                                 """
                                                 +C
                                                 ~GATE
                                                 /1
                                                 /c
                                                 +
                                                 +
                                                 +
                                                 =@@4.44@
                                                 """)))

    def test_shift_x_y_floor(self):
        rooms = translator(Handlers(StringHandler("Main",
                                                  """
                                                  XS 23
                                                  YS-24
                                                  FS -5
                                                  /t""")))
        self.assertTrue(rooms.read(23, -24, -5), "t")

    def test_x_y_floor(self):
        rooms = translator(Handlers(StringHandler("Main",
                                                  """
                                                  X 23
                                                  Y-24
                                                  F -5
                                                  /T""")))
        self.assertTrue(rooms.read(23, -24, -5), "T")

    def test_shift_x_y_floor_and_x_y_floor(self):
        rooms = translator(Handlers(StringHandler("Main",
                                                  """
                                                  \tXS 23
                                                  YS-24
                                                  FS -5
                                                  X2
                                                  Y4
                                                  Y3
                                                  F-5
                                                  XS -3
                                                  YS6
                                                  FS -5
                                                  /t
                                                  +floor2
                                                  /2""")))
        self.assertTrue(rooms.read(-1, 9, -10), "t")
        self.assertTrue(rooms.read(0, 0, -9), "2")

    def test_shift_x_error(self):
        handlers = Handlers(StringHandler("Main",
                                          "XS@"))
        self.assertRaises(TranslatorError, translator, handlers)

    def test_shift_y_error(self):
        handlers = Handlers(StringHandler("Main",
                                          "YS88 -80"))
        self.assertRaises(TranslatorError, translator, handlers)

    def test_shift_f_error(self):
        handlers = Handlers(StringHandler("Main",
                                          "FSasdf"))
        self.assertRaises(TranslatorError, translator, handlers)

    def test_x_error(self):
        handlers = Handlers(StringHandler("Main",
                                          "X@"))
        self.assertRaises(TranslatorError, translator, handlers)

    def test_y_error(self):
        handlers = Handlers(StringHandler("Main",
                                          "Y88 -80"))
        self.assertRaises(TranslatorError, translator, handlers)

    def test_f_error(self):
        handlers = Handlers(StringHandler("Main",
                                          "Fasdf"))
        self.assertRaises(TranslatorError, translator, handlers)

    def test_bad_line(self):
        handlers = Handlers(StringHandler("Main",
                                          "@"))
        self.assertRaises(TranslatorError, translator, handlers)

    def test_bad_line_2(self):
        handlers = Handlers(StringHandler("Main",
                                          "      2384095 *(*&)"))
        self.assertRaises(TranslatorError, translator, handlers)
