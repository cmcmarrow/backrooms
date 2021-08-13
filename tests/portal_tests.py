"""
Copyright 2021 Charles McMarrow
"""

# built-in
import unittest

# backrooms
from backrooms.conscious import WORK_STACK, ID
from backrooms.portal import Feeder, Portal, PortalError
from backrooms.rooms import Rooms
from backrooms.stack import StackBottom
from backrooms.translator import StringHandler, Handlers, translator


class FeederTests(unittest.TestCase):
    def test_init(self):
        self.assertIsInstance(Feeder(), Feeder)

    def test_feeder(self):
        feeder = Feeder()
        self.assertIsNone(feeder.get_input())
        self.assertIsNone(feeder.get_input())
        self.assertFalse(feeder.wants_input())
        self.assertFalse(feeder.wants_input())
        feeder.need_input()
        self.assertTrue(feeder.wants_input())
        self.assertTrue(feeder.wants_input())
        feeder.set_input("cats")
        self.assertFalse(feeder.wants_input())
        self.assertFalse(feeder.wants_input())
        self.assertEqual(feeder.get_input(), "cats")
        self.assertIsNone(feeder.get_input())
        feeder.set_input("cats")
        feeder.set_input("1234")
        feeder.set_input("666666")
        self.assertEqual(feeder.get_input(), "666666")
        self.assertIsNone(feeder.get_input())
        self.assertFalse(feeder.wants_input())
        feeder.need_input()
        self.assertTrue(feeder.wants_input())
        self.assertIsNone(feeder.get_input())
        self.assertTrue(feeder.wants_input())
        feeder.set_input("hello")
        self.assertFalse(feeder.wants_input())
        self.assertEqual(feeder.get_input(), "hello")
        self.assertIsNone(feeder.get_input())
        self.assertFalse(feeder.wants_input())


class PortalTests(unittest.TestCase):
    def test_is_done(self):
        main = """
        ~GATE
        /ri1e~ha
        """
        portal = Portal(translator(Handlers(StringHandler("main", main))),
                        inputs=(),
                        sys_output=False,
                        catch_output=True,
                        lost_count=1000,
                        lost_rule_count=1000,
                        error_on_space=True)
        self.assertFalse(portal.is_done())
        for rule in portal:
            self.assertFalse(portal.is_done())
            for _ in rule:
                self.assertFalse(portal.is_done())

        for _ in range(3):
            self.assertTrue(portal.is_done())

    def test_get_rooms(self):
        main = """
                ~GATE
                /ri1ew...~ha
                """
        portal = Portal(translator(Handlers(StringHandler("main", main))),
                        inputs=(),
                        sys_output=False,
                        catch_output=True,
                        lost_count=1000,
                        lost_rule_count=1000,
                        error_on_space=True)
        self.assertIsInstance(portal.get_rooms(), Rooms)
        self.assertEqual(portal.get_rooms().read(7, 0, 0), ".")
        portal()
        self.assertEqual(portal.get_rooms().read(7, 0, 0), "1")

    def test_get_consciouses_and_new_conscious(self):
        main = """
                ~GATE
                /ri1e.~ha
                """
        portal = Portal(translator(Handlers(StringHandler("main", main))),
                        inputs=(),
                        sys_output=False,
                        catch_output=True,
                        lost_count=1000,
                        lost_rule_count=1000,
                        error_on_space=True)
        portal_iter = iter(portal)
        self.assertEqual(len(portal.get_consciouses()), 1)
        self.assertEqual(portal.get_consciouses()[0][WORK_STACK].peak(), StackBottom)
        self.assertEqual(portal.get_consciouses()[0][ID], 0)
        for _ in next(portal_iter):
            pass
        self.assertEqual(portal.get_consciouses()[0][WORK_STACK].peak(), 1)
        for i in range(1, 4):
            new_conscious = portal.new_conscious()
            self.assertIs(portal.get_consciouses()[-1], new_conscious)
            self.assertEqual(new_conscious[ID], i)
        portal()
        self.assertEqual(portal.get_output_stream(), [1] * 4)

    def test_read_input_and_get_output_stream(self):
        main = """
               ~GATE
               /ri44eprs"cats"eprneprfepe~ha
               """
        portal = Portal(translator(Handlers(StringHandler("main", main))),
                        inputs=(),
                        sys_output=False,
                        catch_output=True,
                        lost_count=1000,
                        lost_rule_count=1000,
                        error_on_space=True)
        portal()
        self.assertEqual(portal.get_output_stream(), [44, "cats", None, "StackFrame", "StackBottom"])

    def test_write_out_and_get_output_stream(self):
        main = """
               ~GATE
               /ri1e~ha
               """
        portal = Portal(translator(Handlers(StringHandler("main", main))),
                        inputs=(),
                        sys_output=False,
                        catch_output=True,
                        lost_count=1000,
                        lost_rule_count=1000,
                        error_on_space=True)
        portal.write_output("hello")
        portal.write_output(1)
        portal.write_output("cats")
        self.assertEqual(portal.get_output_stream(), ["hello", 1, "cats"])
        self.assertEqual(portal.get_output_stream(), ["hello", 1, "cats"])
        portal.write_output(2)
        self.assertEqual(portal.get_output_stream(), ["hello", 1, "cats", 2])
        portal.get_output_stream().clear()
        portal.write_output("run")
        self.assertEqual(portal.get_output_stream(), ["run"])

    def test_get_step_visuals_and_step_count(self):
        main = """
                ~GATE
                /ri1e~ha
                """
        portal = Portal(translator(Handlers(StringHandler("main", main))),
                        inputs=(),
                        sys_output=False,
                        catch_output=True,
                        lost_count=1000,
                        lost_rule_count=1000,
                        error_on_space=True,
                        yields=True)
        portal_iter = iter(portal)

        rule_iter = next(portal_iter)
        self.assertEqual(portal.get_step_visuals(), [])
        self.assertEqual(next(rule_iter), 1)
        self.assertEqual(portal.get_step_visuals(), [(0, 0, 0)])
        self.assertEqual(next(rule_iter), 2)
        self.assertEqual(portal.get_step_visuals(), [(0, 0, 0), (1, 0, 0)])
        self.assertEqual(next(rule_iter), 3)
        self.assertEqual(portal.get_step_visuals(), [(0, 0, 0), (1, 0, 0), (2, 0, 0)])
        self.assertRaises(StopIteration, next, rule_iter)

        rule_iter = next(portal_iter)
        self.assertEqual(portal.get_step_visuals(), [])
        self.assertEqual(next(rule_iter), 1)
        self.assertEqual(portal.get_step_visuals(), [(3, 0, 0)])
        self.assertRaises(StopIteration, next, rule_iter)

        rule_iter = next(portal_iter)
        self.assertEqual(portal.get_step_visuals(), [])
        self.assertEqual(next(rule_iter), 1)
        self.assertEqual(portal.get_step_visuals(), [(4, 0, 0)])
        self.assertEqual(next(rule_iter), 2)
        self.assertEqual(portal.get_step_visuals(), [(4, 0, 0), (5, 0, 0)])
        self.assertEqual(next(rule_iter), 3)
        self.assertEqual(portal.get_step_visuals(), [(4, 0, 0), (5, 0, 0), (6, 0, 0)])
        self.assertRaises(StopIteration, next, rule_iter)

    def test_feeder(self):
        main = """
                        ~GATE
                        /cepcepe~ha
                        """
        portal = Portal(translator(Handlers(StringHandler("main", main))),
                        feeder=True,
                        sys_output=False,
                        catch_output=True,
                        lost_count=1000,
                        lost_rule_count=1000,
                        error_on_space=True)
        self.assertIsInstance(portal.get_feeder(), Feeder)
        feeder = portal.get_feeder()
        portal_iter = iter(portal)

        cite = next(portal_iter)
        self.assertFalse(feeder.wants_input())
        next(cite)
        self.assertTrue(feeder.wants_input())
        feeder.set_input("cats")
        self.assertFalse(feeder.wants_input())
        self.assertRaises(StopIteration, next, cite)
        for _ in range(2):
            rule = next(portal_iter)
            for _ in rule:
                pass
        cite = next(portal_iter)
        self.assertFalse(feeder.wants_input())
        for _ in range(25):
            next(cite)
            self.assertTrue(feeder.wants_input())
        feeder.set_input("&*(@^#")
        self.assertFalse(feeder.wants_input())
        self.assertRaises(StopIteration, next, cite)
        for _ in range(4):
            rule = next(portal_iter)
            for _ in rule:
                pass
        self.assertRaises(StopIteration, next, portal_iter)
        stream = portal.get_output_stream()
        self.assertEqual(len(stream), 3)
        self.assertEqual(stream[0], "cats")
        self.assertEqual(stream[1], "&*(@^#")
        self.assertEqual(stream[2], "StackBottom")

    def test_lost_feeder(self):
        main = """
                        ~GATE
                        /c~ha
                        """
        portal = Portal(translator(Handlers(StringHandler("main", main))),
                        feeder=True,
                        sys_output=False,
                        catch_output=True,
                        lost_count=1000,
                        lost_rule_count=1000,
                        error_on_space=True)
        self.assertRaises(PortalError, portal)
        self.assertIsInstance(portal.get_feeder(), Feeder)
        feeder = portal.get_feeder()
        self.assertTrue(feeder.wants_input())

    def test_lost_count(self):
        main = """
                                ~GATE
                                />V
                                /^<
                                """
        portal = Portal(translator(Handlers(StringHandler("main", main))),
                        inputs=(),
                        sys_output=False,
                        catch_output=True,
                        lost_count=100,
                        lost_rule_count=1000,
                        error_on_space=True)
        count = 0
        try:
            for rule in portal:
                count += 1
                for _ in rule:
                    pass
        except PortalError:
            pass
        self.assertEqual(count, 100)

    def test_lost_count_2(self):
        main = """
                                ~GATE
                                />.....V
                                /^.....<
                                """
        portal = Portal(translator(Handlers(StringHandler("main", main))),
                        inputs=(),
                        sys_output=False,
                        catch_output=True,
                        lost_count=750,
                        lost_rule_count=1000,
                        error_on_space=True)
        count = 0
        try:
            for rule in portal:
                count += 1
                for _ in rule:
                    pass
        except PortalError:
            pass
        self.assertEqual(count, 750)

    def test_lost_rule_count(self):
        main = """
                                ~GATE
                                /ppppppppprs"lol
                                """
        portal = Portal(translator(Handlers(StringHandler("main", main))),
                        inputs=(),
                        sys_output=False,
                        catch_output=True,
                        lost_count=1000,
                        lost_rule_count=100,
                        error_on_space=True)
        count = 0
        try:
            for rule in portal:
                count = 0
                for _ in rule:
                    count += 1
        except PortalError:
            pass
        self.assertEqual(count, 99)

    def test_lost_rule_count_2(self):
        main = """
                                ~GATE
                                /V>...............rs+
                                />^
                                """
        portal = Portal(translator(Handlers(StringHandler("main", main))),
                        inputs=(),
                        sys_output=False,
                        catch_output=True,
                        lost_count=1000,
                        lost_rule_count=750,
                        error_on_space=True)
        count = 0
        try:
            for rule in portal:
                count = 0
                for _ in rule:
                    count += 1
        except PortalError:
            pass
        self.assertEqual(count, 749)

    def test_missing_gate(self):
        main = """
                ~GATE2
                /~ha
                """
        self.assertRaises(PortalError,
                          Portal,
                          translator(Handlers(StringHandler("main", main))),
                          inputs=(),
                          sys_output=False,
                          catch_output=True,
                          lost_count=1000,
                          lost_rule_count=1000,
                          error_on_space=True)

    def test_multiple_inputs_methods(self):
        main = """
               ~GATE
               /~ha
               """
        self.assertRaises(PortalError,
                          Portal,
                          translator(Handlers(StringHandler("main", main))),
                          inputs=(),
                          feeder=True,
                          sys_output=False,
                          catch_output=True,
                          lost_count=1000,
                          lost_rule_count=1000,
                          error_on_space=True)
