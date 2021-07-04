"""
Copyright 2021 Charles McMarrow
"""

# built-in
from typing import Generator, Tuple, List, Dict, Union, Optional, Callable
import string

# backrooms
import backrooms    # import backrooms to avoid circular imports
from .backrooms_error import BackroomsError
from . import conscious as c
from .rooms import Rooms
from .stack import StackFrame, StackBottom


class RuleError(BackroomsError):
    @classmethod
    def bad_start_character(cls,
                            start_character: str):
        return cls(f"{repr(start_character)} is not a valid start character!")

    @classmethod
    def start_character_collection(cls,
                                   start_character: str):
        return cls(f"{repr(start_character)} is used more then once in a work space!")

    @classmethod
    def bad_hope_start_character(cls, name: str):
        return cls(f"Hope start character most be a single digit not: {repr(name)}!")


def _to_int(obj: Union[int, str, StackFrame, StackBottom, None]) -> Optional[int]:
    if isinstance(obj, str):
        try:
            return int(obj)
        except ValueError:
            return
    elif obj is None:
        return
    elif obj is StackFrame:
        return
    elif obj is StackBottom:
        return
    return obj


def _to_string(obj: Union[int, str, StackFrame, StackBottom, None]) -> str:
    if isinstance(obj, int):
        return str(obj)
    elif obj is None:
        return "None"
    elif obj is StackFrame:
        return "StackFrame"
    elif obj is StackBottom:
        return "StackBottom"
    return obj


SHIFTER = "SHIFTER"


class WorkSpace(dict):
    def __init__(self):
        work_space = {SHIFTER: set()}
        super(WorkSpace, self).__init__(work_space)


class Rule:
    def __init__(self,
                 start_character: str,
                 work_space: WorkSpace):
        if len(start_character) != 1:
            raise RuleError.bad_hope_start_character(start_character)
        self._start_character: str = start_character
        self._work_space: WorkSpace = work_space

    def __call__(self,
                 portal: 'backrooms.portal.Portal',
                 rooms: Rooms,
                 conscious: c.Conscious,
                 rule_step_visuals: List[Tuple[int, int, int]]) -> Generator[None, None, None]:
        """
        info: Runs a rule.
        :param portal: Portal
        :param rooms: Rooms
        :param conscious: Conscious
        :param rule_step_visuals: List[Tuple[int, int, int]]
        :return: Generator[None, None, None]
        """
        raise NotImplementedError()

    def get_start_character(self) -> str:
        return self._start_character

    def get_work_space(self) -> WorkSpace:
        return self._work_space


class RuleModule(Rule):
    def __init__(self,
                 start_character: str,
                 work_space: WorkSpace,
                 rules: Tuple):
        super(RuleModule, self).__init__(start_character, work_space)
        rules_obj = [rule(work_space) for rule in rules]
        self._rules: Dict[str, Rule] = {}
        for rule in rules_obj:
            if rule.get_start_character() in self._rules:
                raise RuleError.start_character_collection(rule.get_start_character())
            self._rules[rule.get_start_character()] = rule

    def __call__(self,
                 portal: 'backrooms.portal.Portal',
                 rooms: Rooms,
                 conscious: c.Conscious,
                 rule_step_visuals: List[Tuple[int, int, int]]) -> Generator[None, None, None]:
        """
        info: Runs a rule.
        :param portal: Portal
        :param rooms: Rooms
        :param conscious: Conscious
        :param rule_step_visuals: List[Tuple[int, int, int]]
        :return: Generator[None, None, None]
        """
        conscious.step()
        rule_step_visuals.append(conscious.at())
        yield
        rule = rooms.read(*conscious.at())
        if rule in self._rules:
            for _ in self._rules[rule](portal, rooms, conscious, rule_step_visuals):
                yield


class Halt(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(Halt, self).__init__("~", work_space)

    def __call__(self,
                 portal: 'backrooms.portal.Portal',
                 rooms: Rooms,
                 conscious: c.Conscious,
                 rule_step_visuals: List[Tuple[int, int, int]]) -> Generator[None, None, None]:
        """
        info: Runs a rule.
        :param portal: Portal
        :param rooms: Rooms
        :param conscious: Conscious
        :param rule_step_visuals: List[Tuple[int, int, int]]
        :return: Generator[None, None, None]
        """
        conscious.step()
        yield
        if rooms.read(*conscious.at()) == "h":
            conscious.step()
            rule_step_visuals.append(conscious.at())
            yield
            if rooms.read(*conscious.at()) == "a":
                conscious.step()
                conscious[c.HALT] = True


class Output(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(Output, self).__init__("e", work_space)

    def __call__(self,
                 portal: 'backrooms.portal.Portal',
                 rooms: Rooms,
                 conscious: c.Conscious,
                 rule_step_visuals: List[Tuple[int, int, int]]) -> Generator[None, None, None]:
        """
        info: Runs a rule.
        :param portal: Portal
        :param rooms: Rooms
        :param conscious: Conscious
        :param rule_step_visuals: List[Tuple[int, int, int]]
        :return: Generator[None, None, None]
        """
        conscious.step()
        output = conscious[c.WORK_STACK].peak()
        if output is StackFrame:
            output = "StackFrame"
        elif output is StackBottom:
            output = "StackBottom"
        portal.write_output(output)
        yield


class Input(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(Input, self).__init__("c", work_space)

    def __call__(self,
                 portal: 'backrooms.portal.Portal',
                 rooms: Rooms,
                 conscious: c.Conscious,
                 rule_step_visuals: List[Tuple[int, int, int]]) -> Generator[None, None, None]:
        """
        info: Runs a rule.
        :param portal: Portal
        :param rooms: Rooms
        :param conscious: Conscious
        :param rule_step_visuals: List[Tuple[int, int, int]]
        :return: Generator[None, None, None]
        """
        conscious.step()
        conscious[c.WORK_STACK].push(portal.read_input())
        yield


class Hope(Rule):
    def __init__(self,
                 start_character: str,
                 work_space: WorkSpace):
        if start_character not in string.digits:
            raise RuleError.bad_hope_start_character(start_character)

        super(Hope, self).__init__(start_character, work_space)
        self._jump_count = int(start_character)

    def __call__(self,
                 portal: 'backrooms.portal.Portal',
                 rooms: Rooms,
                 conscious: c.Conscious,
                 rule_step_visuals: List[Tuple[int, int, int]]) -> Generator[None, None, None]:
        """
        info: Runs a rule.
        :param portal: Portal
        :param rooms: Rooms
        :param conscious: Conscious
        :param rule_step_visuals: List[Tuple[int, int, int]]
        :return: Generator[None, None, None]
        """
        conscious.step()
        yield
        for _ in range(self._jump_count):
            conscious.step()


class One(Hope):
    def __init__(self,
                 work_space: WorkSpace):
        super(One, self).__init__("1", work_space)


class Two(Hope):
    def __init__(self,
                 work_space: WorkSpace):
        super(Two, self).__init__("2", work_space)


class Three(Hope):
    def __init__(self,
                 work_space: WorkSpace):
        super(Three, self).__init__("3", work_space)


class Four(Hope):
    def __init__(self,
                 work_space: WorkSpace):
        super(Four, self).__init__("4", work_space)


class Five(Hope):
    def __init__(self,
                 work_space: WorkSpace):
        super(Five, self).__init__("5", work_space)


class Six(Hope):
    def __init__(self,
                 work_space: WorkSpace):
        super(Six, self).__init__("6", work_space)


class Seven(Hope):
    def __init__(self,
                 work_space: WorkSpace):
        super(Seven, self).__init__("7", work_space)


class Eighth(Hope):
    def __init__(self,
                 work_space: WorkSpace):
        super(Eighth, self).__init__("8", work_space)


class Nine(Hope):
    def __init__(self,
                 work_space: WorkSpace):
        super(Nine, self).__init__("9", work_space)


class Shifter(Rule):
    def __init__(self,
                 vector_x: int,
                 vector_y: int,
                 vector_floor_level: int,
                 start_character: str,
                 work_space: WorkSpace):
        super(Shifter, self).__init__(start_character, work_space)
        self.get_work_space()[SHIFTER].add(self.get_start_character())
        self._vector_x: int = vector_x
        self._vector_y: int = vector_y
        self._vector_floor_level: int = vector_floor_level

    def __call__(self,
                 portal: 'backrooms.portal.Portal',
                 rooms: Rooms,
                 conscious: c.Conscious,
                 rule_step_visuals: List[Tuple[int, int, int]]) -> Generator[None, None, None]:
        """
        info: Runs a rule.
        :param portal: Portal
        :param rooms: Rooms
        :param conscious: Conscious
        :param rule_step_visuals: List[Tuple[int, int, int]]
        :return: Generator[None, None, None]
        """
        if conscious[c.BRANCH](conscious):
            conscious[c.PC_V_X] = self._vector_x
            conscious[c.PC_V_Y] = self._vector_y
            conscious[c.PC_V_FLOOR] = self._vector_floor_level
            conscious.step()
            yield
            if rooms.read(*conscious.at()) == self.get_start_character():
                rule_step_visuals.append(conscious.at())
                conscious.step()
                yield
                skip_count = 0
                while True:
                    rule_step_visuals.append(conscious.at())
                    if rooms.read(*conscious.at()) == "!":
                        skip_count += 1
                    elif rooms.read(*conscious.at()) in self.get_work_space()[SHIFTER]:
                        if not skip_count:
                            break
                        skip_count += -1
                    conscious.step()
                    yield
        else:
            conscious.step()
            yield


class Right(Shifter):
    def __init__(self,
                 work_space: WorkSpace):
        super(Right, self).__init__(1, 0, 0, ">", work_space)


class Left(Shifter):
    def __init__(self,
                 work_space: WorkSpace):
        super(Left, self).__init__(-1, 0, 0, "<", work_space)


class Up(Shifter):
    def __init__(self,
                 work_space: WorkSpace):
        super(Up, self).__init__(0, 1, 0, "^", work_space)


class Down(Shifter):
    def __init__(self,
                 work_space: WorkSpace):
        super(Down, self).__init__(0, -1, 0, "v", work_space)


class DownUpper(Shifter):
    def __init__(self,
                 work_space: WorkSpace):
        super(DownUpper, self).__init__(0, -1, 0, "V", work_space)


class Upper(Shifter):
    def __init__(self,
                 work_space: WorkSpace):
        super(Upper, self).__init__(0, 0, 1, "{", work_space)


class Lower(Shifter):
    def __init__(self,
                 work_space: WorkSpace):
        super(Lower, self).__init__(0, 0, -1, "}", work_space)


class Branch(Rule):
    def __init__(self,
                 branch_function: Callable,
                 start_character: str,
                 work_space: WorkSpace):
        super(Branch, self).__init__(start_character, work_space)
        self._branch_function = branch_function

    def __call__(self,
                 portal: 'backrooms.portal.Portal',
                 rooms: Rooms,
                 conscious: c.Conscious,
                 rule_step_visuals: List[Tuple[int, int, int]]) -> Generator[None, None, None]:
        """
        info: Runs a rule.
        :param portal: Portal
        :param rooms: Rooms
        :param conscious: Conscious
        :param rule_step_visuals: List[Tuple[int, int, int]]
        :return: Generator[None, None, None]
        """
        conscious[c.BRANCH] = self._branch_function
        conscious.step()
        yield


class Clear(Branch):
    def __init__(self,
                 work_space: WorkSpace):
        super(Clear, self).__init__(c.BRANCH_CLEAR, "C", work_space)


class LessThanZero(Branch):
    def __init__(self,
                 work_space: WorkSpace):
        super(LessThanZero, self).__init__(c.BRANCH_LESS_THAN_ZERO, "L", work_space)


class GreaterThanZero(Branch):
    def __init__(self,
                 work_space: WorkSpace):
        super(GreaterThanZero, self).__init__(c.BRANCH_GREATER_THAN_ZERO, "G", work_space)


class Zero(Branch):
    def __init__(self,
                 work_space: WorkSpace):
        super(Zero, self).__init__(c.BRANCH_ZERO, "Z", work_space)


class NotZero(Branch):
    def __init__(self,
                 work_space: WorkSpace):
        super(NotZero, self).__init__(c.BRANCH_NOT_ZERO, "N", work_space)


class IsInteger(Branch):
    def __init__(self,
                 work_space: WorkSpace):
        super(IsInteger, self).__init__(c.BRANCH_IS_INTEGER, "I", work_space)


class IsString(Branch):
    def __init__(self,
                 work_space: WorkSpace):
        super(IsString, self).__init__(c.BRANCH_IS_STRING, "S", work_space)


class IsNone(Branch):
    def __init__(self,
                 work_space: WorkSpace):
        super(IsNone, self).__init__(c.BRANCH_IS_NONE, "O", work_space)


class IsStackFrame(Branch):
    def __init__(self,
                 work_space: WorkSpace):
        super(IsStackFrame, self).__init__(c.BRANCH_IS_STACK_FRAME, "F", work_space)


class IsStackBottom(Branch):
    def __init__(self,
                 work_space: WorkSpace):
        super(IsStackBottom, self).__init__(c.BRANCH_IS_STACK_BOTTOM, "B", work_space)


class Pop(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(Pop, self).__init__("p", work_space)

    def __call__(self,
                 portal: 'backrooms.portal.Portal',
                 rooms: Rooms,
                 conscious: c.Conscious,
                 rule_step_visuals: List[Tuple[int, int, int]]) -> Generator[None, None, None]:
        """
        info: Runs a rule.
        :param portal: Portal
        :param rooms: Rooms
        :param conscious: Conscious
        :param rule_step_visuals: List[Tuple[int, int, int]]
        :return: Generator[None, None, None]
        """
        conscious[c.WORK_STACK].pop()
        conscious.step()
        yield


class Duplicate(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(Duplicate, self).__init__("d", work_space)

    def __call__(self,
                 portal: 'backrooms.portal.Portal',
                 rooms: Rooms,
                 conscious: c.Conscious,
                 rule_step_visuals: List[Tuple[int, int, int]]) -> Generator[None, None, None]:
        """
        info: Runs a rule.
        :param portal: Portal
        :param rooms: Rooms
        :param conscious: Conscious
        :param rule_step_visuals: List[Tuple[int, int, int]]
        :return: Generator[None, None, None]
        """
        work_space = conscious[c.WORK_STACK]
        work_space.push(work_space.peak())
        conscious.step()
        yield


class Worker(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(Worker, self).__init__("q", work_space)

    def __call__(self,
                 portal: 'backrooms.portal.Portal',
                 rooms: Rooms,
                 conscious: c.Conscious,
                 rule_step_visuals: List[Tuple[int, int, int]]) -> Generator[None, None, None]:
        """
        info: Runs a rule.
        :param portal: Portal
        :param rooms: Rooms
        :param conscious: Conscious
        :param rule_step_visuals: List[Tuple[int, int, int]]
        :return: Generator[None, None, None]
        """
        conscious.step()
        yield
        if rooms.read(*conscious.at()).isdigit():
            conscious[c.WORKING_REGISTER] = "R" + rooms.read(*conscious.at())
            rule_step_visuals.append(conscious.at())
            conscious.step()
            yield


class Keep(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(Keep, self).__init__("k", work_space)

    def __call__(self,
                 portal: 'backrooms.portal.Portal',
                 rooms: Rooms,
                 conscious: c.Conscious,
                 rule_step_visuals: List[Tuple[int, int, int]]) -> Generator[None, None, None]:
        """
        info: Runs a rule.
        :param portal: Portal
        :param rooms: Rooms
        :param conscious: Conscious
        :param rule_step_visuals: List[Tuple[int, int, int]]
        :return: Generator[None, None, None]
        """
        conscious.step()
        conscious[conscious[c.WORKING_REGISTER]] = conscious[c.WORK_STACK].peak()
        yield


class Store(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(Store, self).__init__("s", work_space)

    def __call__(self,
                 portal: 'backrooms.portal.Portal',
                 rooms: Rooms,
                 conscious: c.Conscious,
                 rule_step_visuals: List[Tuple[int, int, int]]) -> Generator[None, None, None]:
        """
        info: Runs a rule.
        :param portal: Portal
        :param rooms: Rooms
        :param conscious: Conscious
        :param rule_step_visuals: List[Tuple[int, int, int]]
        :return: Generator[None, None, None]
        """
        conscious.step()
        conscious[c.WORK_STACK].push(conscious[conscious[c.WORKING_REGISTER]])
        yield


def _read(rooms: Rooms,
          conscious: c.Conscious,
          rule_step_visuals: List[Tuple[int, int, int]]) -> Generator[None, None, None]:
    type_item = rooms.read(*conscious.at())
    if type_item == "i":
        rule_step_visuals.append(conscious.at())
        conscious.step()
        yield
        if rooms.read(*conscious.at()) in string.digits + "+-":
            new_integer = rooms.read(*conscious.at())
            rule_step_visuals.append(conscious.at())
            conscious.step()
            yield
            while rooms.read(*conscious.at()).isdigit():
                new_integer += rooms.read(*conscious.at())
                rule_step_visuals.append(conscious.at())
                conscious.step()
                yield
            try:
                conscious[c.WORK_STACK].push(int(new_integer))
            except ValueError:
                pass
    elif type_item == "s":
        rule_step_visuals.append(conscious.at())
        conscious.step()
        yield
        start_character = rooms.read(*conscious.at())
        new_string = ""
        rule_step_visuals.append(conscious.at())
        conscious.step()
        yield
        while rooms.read(*conscious.at()) != start_character:
            new_string += rooms.read(*conscious.at())
            rule_step_visuals.append(conscious.at())
            conscious.step()
            yield
        conscious[c.WORK_STACK].push(new_string)
        rule_step_visuals.append(conscious.at())
        conscious.step()
    elif type_item == "n":
        rule_step_visuals.append(conscious.at())
        conscious.step()
        conscious[c.WORK_STACK].push(None)
    elif type_item == "f":
        rule_step_visuals.append(conscious.at())
        conscious.step()
        conscious[c.WORK_STACK].push(StackFrame)


class Read(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(Read, self).__init__("r", work_space)

    def __call__(self,
                 portal: 'backrooms.portal.Portal',
                 rooms: Rooms,
                 conscious: c.Conscious,
                 rule_step_visuals: List[Tuple[int, int, int]]) -> Generator[None, None, None]:
        """
        info: Runs a rule.
        :param portal: Portal
        :param rooms: Rooms
        :param conscious: Conscious
        :param rule_step_visuals: List[Tuple[int, int, int]]
        :return: Generator[None, None, None]
        """
        conscious.step()
        yield
        for _ in _read(rooms, conscious, rule_step_visuals):
            yield


def _write(rooms: Rooms,
           conscious: c.Conscious,
           rule_step_visuals: List[Tuple[int, int, int]]) -> str:
    item = conscious[c.WORK_STACK].pop()
    if item is None:
        return "n"
    elif item is StackBottom:
        return "n"
    elif item is StackFrame:
        return "f"
    elif isinstance(item, int):
        return "i" + str(item)
    rule_step_visuals.append(conscious.at())
    start_character = rooms.read(*conscious.at())
    conscious.step()
    return f"s{start_character}{item}{start_character}"


class Write(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(Write, self).__init__("w", work_space)

    def __call__(self,
                 portal: 'backrooms.portal.Portal',
                 rooms: Rooms,
                 conscious: c.Conscious,
                 rule_step_visuals: List[Tuple[int, int, int]]) -> Generator[None, None, None]:
        """
        info: Runs a rule.
        :param portal: Portal
        :param rooms: Rooms
        :param conscious: Conscious
        :param rule_step_visuals: List[Tuple[int, int, int]]
        :return: Generator[None, None, None]
        """
        conscious.step()
        yield
        raw_data = "r" + _write(rooms, conscious, rule_step_visuals)
        yield
        for character in raw_data:
            rooms.write(*conscious.at(), character=character)
            rule_step_visuals.append(conscious.at())
            conscious.step()
            yield


class StringLength(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(StringLength, self).__init__("l", work_space)

    def __call__(self,
                 portal: 'backrooms.portal.Portal',
                 rooms: Rooms,
                 conscious: c.Conscious,
                 rule_step_visuals: List[Tuple[int, int, int]]) -> Generator[None, None, None]:
        """
        info: Runs a rule.
        :param portal: Portal
        :param rooms: Rooms
        :param conscious: Conscious
        :param rule_step_visuals: List[Tuple[int, int, int]]
        :return: Generator[None, None, None]
        """
        item = conscious[c.WORK_STACK].pop()
        if isinstance(item, str):
            conscious[c.WORK_STACK].push(len(item))
        else:
            conscious[c.WORK_STACK].push(None)
        conscious.step()
        yield


class StringCast(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(StringCast, self).__init__("c", work_space)

    def __call__(self,
                 portal: 'backrooms.portal.Portal',
                 rooms: Rooms,
                 conscious: c.Conscious,
                 rule_step_visuals: List[Tuple[int, int, int]]) -> Generator[None, None, None]:
        """
        info: Runs a rule.
        :param portal: Portal
        :param rooms: Rooms
        :param conscious: Conscious
        :param rule_step_visuals: List[Tuple[int, int, int]]
        :return: Generator[None, None, None]
        """
        item = conscious[c.WORK_STACK].pop()
        conscious[c.WORK_STACK].push(_to_string(item))
        conscious.step()
        yield


class StringAt(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(StringAt, self).__init__("a", work_space)

    def __call__(self,
                 portal: 'backrooms.portal.Portal',
                 rooms: Rooms,
                 conscious: c.Conscious,
                 rule_step_visuals: List[Tuple[int, int, int]]) -> Generator[None, None, None]:
        """
        info: Runs a rule.
        :param portal: Portal
        :param rooms: Rooms
        :param conscious: Conscious
        :param rule_step_visuals: List[Tuple[int, int, int]]
        :return: Generator[None, None, None]
        """
        at = conscious[c.WORK_STACK].pop()
        item = conscious[c.WORK_STACK].pop()
        if isinstance(item, str) and isinstance(at, int):
            try:
                conscious[c.WORK_STACK].push(item[at])
            except IndexError:
                conscious[c.WORK_STACK].push(None)
        else:
            conscious[c.WORK_STACK].push(None)
        conscious.step()
        yield


class StringByte(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(StringByte, self).__init__("b", work_space)

    def __call__(self,
                 portal: 'backrooms.portal.Portal',
                 rooms: Rooms,
                 conscious: c.Conscious,
                 rule_step_visuals: List[Tuple[int, int, int]]) -> Generator[None, None, None]:
        """
        info: Runs a rule.
        :param portal: Portal
        :param rooms: Rooms
        :param conscious: Conscious
        :param rule_step_visuals: List[Tuple[int, int, int]]
        :return: Generator[None, None, None]
        """
        item = conscious[c.WORK_STACK].pop()
        if isinstance(item, str) and len(item) == 1:
            conscious[c.WORK_STACK].push(ord(item))
        else:
            conscious[c.WORK_STACK].push(None)
        conscious.step()
        yield


class StringSplit(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(StringSplit, self).__init__("s", work_space)

    def __call__(self,
                 portal: 'backrooms.portal.Portal',
                 rooms: Rooms,
                 conscious: c.Conscious,
                 rule_step_visuals: List[Tuple[int, int, int]]) -> Generator[None, None, None]:
        """
        info: Runs a rule.
        :param portal: Portal
        :param rooms: Rooms
        :param conscious: Conscious
        :param rule_step_visuals: List[Tuple[int, int, int]]
        :return: Generator[None, None, None]
        """
        at = conscious[c.WORK_STACK].pop()
        item = conscious[c.WORK_STACK].pop()
        if isinstance(item, str) and isinstance(at, int):
            back = item[at:]
            front = item[:at]
            conscious[c.WORK_STACK].push(front)
            conscious[c.WORK_STACK].push(back)
        else:
            conscious[c.WORK_STACK].push(None)
        conscious.step()
        yield


class StringJoin(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(StringJoin, self).__init__("j", work_space)

    def __call__(self,
                 portal: 'backrooms.portal.Portal',
                 rooms: Rooms,
                 conscious: c.Conscious,
                 rule_step_visuals: List[Tuple[int, int, int]]) -> Generator[None, None, None]:
        """
        info: Runs a rule.
        :param portal: Portal
        :param rooms: Rooms
        :param conscious: Conscious
        :param rule_step_visuals: List[Tuple[int, int, int]]
        :return: Generator[None, None, None]
        """
        back = conscious[c.WORK_STACK].pop()
        front = conscious[c.WORK_STACK].pop()
        if isinstance(front, str) and isinstance(back, str):
            conscious[c.WORK_STACK].push(front + back)
        else:
            conscious[c.WORK_STACK].push(None)
        conscious.step()
        yield


class StringEqual(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(StringEqual, self).__init__("e", work_space)

    def __call__(self,
                 portal: 'backrooms.portal.Portal',
                 rooms: Rooms,
                 conscious: c.Conscious,
                 rule_step_visuals: List[Tuple[int, int, int]]) -> Generator[None, None, None]:
        """
        info: Runs a rule.
        :param portal: Portal
        :param rooms: Rooms
        :param conscious: Conscious
        :param rule_step_visuals: List[Tuple[int, int, int]]
        :return: Generator[None, None, None]
        """
        string_2 = conscious[c.WORK_STACK].pop()
        string_1 = conscious[c.WORK_STACK].pop()
        if isinstance(string_1, str) and isinstance(string_2, str):
            conscious[c.WORK_STACK].push(int(string_1 == string_2))
        else:
            conscious[c.WORK_STACK].push(None)
        conscious.step()
        yield


class StringIn(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(StringIn, self).__init__("i", work_space)

    def __call__(self,
                 portal: 'backrooms.portal.Portal',
                 rooms: Rooms,
                 conscious: c.Conscious,
                 rule_step_visuals: List[Tuple[int, int, int]]) -> Generator[None, None, None]:
        """
        info: Runs a rule.
        :param portal: Portal
        :param rooms: Rooms
        :param conscious: Conscious
        :param rule_step_visuals: List[Tuple[int, int, int]]
        :return: Generator[None, None, None]
        """
        string_2 = conscious[c.WORK_STACK].pop()
        string_1 = conscious[c.WORK_STACK].pop()
        if isinstance(string_1, str) and isinstance(string_2, str):
            conscious[c.WORK_STACK].push(int(string_1 in string_2))
        else:
            conscious[c.WORK_STACK].push(None)
        conscious.step()
        yield


class StringUpper(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(StringUpper, self).__init__("u", work_space)

    def __call__(self,
                 portal: 'backrooms.portal.Portal',
                 rooms: Rooms,
                 conscious: c.Conscious,
                 rule_step_visuals: List[Tuple[int, int, int]]) -> Generator[None, None, None]:
        """
        info: Runs a rule.
        :param portal: Portal
        :param rooms: Rooms
        :param conscious: Conscious
        :param rule_step_visuals: List[Tuple[int, int, int]]
        :return: Generator[None, None, None]
        """
        item = conscious[c.WORK_STACK].pop()
        if isinstance(item, str):
            conscious[c.WORK_STACK].push(item.upper())
        else:
            conscious[c.WORK_STACK].push(None)
        conscious.step()
        yield


class StringLower(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(StringLower, self).__init__("o", work_space)

    def __call__(self,
                 portal: 'backrooms.portal.Portal',
                 rooms: Rooms,
                 conscious: c.Conscious,
                 rule_step_visuals: List[Tuple[int, int, int]]) -> Generator[None, None, None]:
        """
        info: Runs a rule.
        :param portal: Portal
        :param rooms: Rooms
        :param conscious: Conscious
        :param rule_step_visuals: List[Tuple[int, int, int]]
        :return: Generator[None, None, None]
        """
        item = conscious[c.WORK_STACK].pop()
        if isinstance(item, str):
            conscious[c.WORK_STACK].push(item.lower())
        else:
            conscious[c.WORK_STACK].push(None)
        conscious.step()
        yield


class StringModule(RuleModule):
    def __init__(self,
                 work_space: WorkSpace):
        super(StringModule, self).__init__("b",
                                           work_space,
                                           (StringLength,
                                            StringCast,
                                            StringAt,
                                            StringByte,
                                            StringSplit,
                                            StringJoin,
                                            StringEqual,
                                            StringIn,
                                            StringUpper,
                                            StringLower))


class IntegerCast(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(IntegerCast, self).__init__("c", work_space)

    def __call__(self,
                 portal: 'backrooms.portal.Portal',
                 rooms: Rooms,
                 conscious: c.Conscious,
                 rule_step_visuals: List[Tuple[int, int, int]]) -> Generator[None, None, None]:
        """
        info: Runs a rule.
        :param portal: Portal
        :param rooms: Rooms
        :param conscious: Conscious
        :param rule_step_visuals: List[Tuple[int, int, int]]
        :return: Generator[None, None, None]
        """
        item = conscious[c.WORK_STACK].pop()
        conscious[c.WORK_STACK].push(_to_int(item))
        conscious.step()
        yield


class IntegerOperation(Rule):
    def __init__(self,
                 operation: Callable,
                 start_character: str,
                 work_space: WorkSpace):
        super(IntegerOperation, self).__init__(start_character, work_space)
        self._operation: Callable = operation

    def __call__(self,
                 portal: 'backrooms.portal.Portal',
                 rooms: Rooms,
                 conscious: c.Conscious,
                 rule_step_visuals: List[Tuple[int, int, int]]) -> Generator[None, None, None]:
        """
        info: Runs a rule.
        :param portal: Portal
        :param rooms: Rooms
        :param conscious: Conscious
        :param rule_step_visuals: List[Tuple[int, int, int]]
        :return: Generator[None, None, None]
        """
        back = conscious[c.WORK_STACK].pop()
        front = conscious[c.WORK_STACK].pop()
        if isinstance(front, int) and isinstance(back, int):
            try:
                conscious[c.WORK_STACK].push(self._operation(front, back))
            except ZeroDivisionError:
                conscious[c.WORK_STACK].push(None)
        else:
            conscious[c.WORK_STACK].push(None)
        conscious.step()
        yield


class IntegerAdd(IntegerOperation):
    def __init__(self,
                 work_space: WorkSpace):
        super(IntegerAdd, self).__init__(int.__add__, "a", work_space)


class IntegerSubtract(IntegerOperation):
    def __init__(self,
                 work_space: WorkSpace):
        super(IntegerSubtract, self).__init__(int.__sub__, "s", work_space)


class IntegerMultiply(IntegerOperation):
    def __init__(self,
                 work_space: WorkSpace):
        super(IntegerMultiply, self).__init__(int.__mul__, "m", work_space)


class IntegerDivide(IntegerOperation):
    def __init__(self,
                 work_space: WorkSpace):
        super(IntegerDivide, self).__init__(int.__floordiv__, "d", work_space)


class IntegerModular(IntegerOperation):
    def __init__(self,
                 work_space: WorkSpace):
        super(IntegerModular, self).__init__(int.__mod__, "o", work_space)


class IntegerPower(IntegerOperation):
    def __init__(self,
                 work_space: WorkSpace):
        super(IntegerPower, self).__init__(int.__floordiv__, "p", work_space)


class IntegerByte(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(IntegerByte, self).__init__("b", work_space)

    def __call__(self,
                 portal: 'backrooms.portal.Portal',
                 rooms: Rooms,
                 conscious: c.Conscious,
                 rule_step_visuals: List[Tuple[int, int, int]]) -> Generator[None, None, None]:
        """
        info: Runs a rule.
        :param portal: Portal
        :param rooms: Rooms
        :param conscious: Conscious
        :param rule_step_visuals: List[Tuple[int, int, int]]
        :return: Generator[None, None, None]
        """
        item = conscious[c.WORK_STACK].pop()
        if isinstance(item, int) and 0 <= item < 256:
            conscious[c.WORK_STACK].push(chr(item))
        else:
            conscious[c.WORK_STACK].push(None)
        conscious.step()
        yield


class IntegerModule(RuleModule):
    def __init__(self,
                 work_space: WorkSpace):
        super(IntegerModule, self).__init__("i",
                                            work_space,
                                            (IntegerCast,
                                             IntegerAdd,
                                             IntegerSubtract,
                                             IntegerMultiply,
                                             IntegerDivide,
                                             IntegerModular,
                                             IntegerPower,
                                             IntegerByte))


class X(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(X, self).__init__("x", work_space)

    def __call__(self,
                 portal: 'backrooms.portal.Portal',
                 rooms: Rooms,
                 conscious: c.Conscious,
                 rule_step_visuals: List[Tuple[int, int, int]]) -> Generator[None, None, None]:
        """
        info: Runs a rule.
        :param portal: Portal
        :param rooms: Rooms
        :param conscious: Conscious
        :param rule_step_visuals: List[Tuple[int, int, int]]
        :return: Generator[None, None, None]
        """
        conscious[c.WORK_STACK].push(conscious[c.PC_X])
        conscious.step()
        yield


class Y(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(Y, self).__init__("y", work_space)

    def __call__(self,
                 portal: 'backrooms.portal.Portal',
                 rooms: Rooms,
                 conscious: c.Conscious,
                 rule_step_visuals: List[Tuple[int, int, int]]) -> Generator[None, None, None]:
        """
        info: Runs a rule.
        :param portal: Portal
        :param rooms: Rooms
        :param conscious: Conscious
        :param rule_step_visuals: List[Tuple[int, int, int]]
        :return: Generator[None, None, None]
        """
        conscious[c.WORK_STACK].push(conscious[c.PC_Y])
        conscious.step()
        yield


class Floor(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(Floor, self).__init__("f", work_space)

    def __call__(self,
                 portal: 'backrooms.portal.Portal',
                 rooms: Rooms,
                 conscious: c.Conscious,
                 rule_step_visuals: List[Tuple[int, int, int]]) -> Generator[None, None, None]:
        """
        info: Runs a rule.
        :param portal: Portal
        :param rooms: Rooms
        :param conscious: Conscious
        :param rule_step_visuals: List[Tuple[int, int, int]]
        :return: Generator[None, None, None]
        """
        conscious[c.WORK_STACK].push(conscious[c.PC_FLOOR])
        conscious.step()
        yield


class ThreadThread(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(ThreadThread, self).__init__("t", work_space)

    def __call__(self,
                 portal: 'backrooms.portal.Portal',
                 rooms: Rooms,
                 conscious: c.Conscious,
                 rule_step_visuals: List[Tuple[int, int, int]]) -> Generator[None, None, None]:
        """
        info: Runs a rule.
        :param portal: Portal
        :param rooms: Rooms
        :param conscious: Conscious
        :param rule_step_visuals: List[Tuple[int, int, int]]
        :return: Generator[None, None, None]
        """
        conscious.step()
        new_conscious = portal.new_conscious()
        new_conscious[c.PC_X] = conscious[c.PC_X]
        new_conscious[c.PC_Y] = conscious[c.PC_Y]
        new_conscious[c.PC_FLOOR] = conscious[c.PC_FLOOR]
        new_conscious[c.PC_V_X] = conscious[c.PC_V_X]
        new_conscious[c.PC_V_Y] = conscious[c.PC_V_Y]
        new_conscious[c.PC_V_FLOOR] = conscious[c.PC_V_FLOOR]
        yield


class ThreadJoin(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(ThreadJoin, self).__init__("j", work_space)

    def __call__(self,
                 portal: 'backrooms.portal.Portal',
                 rooms: Rooms,
                 conscious: c.Conscious,
                 rule_step_visuals: List[Tuple[int, int, int]]) -> Generator[None, None, None]:
        """
        info: Runs a rule.
        :param portal: Portal
        :param rooms: Rooms
        :param conscious: Conscious
        :param rule_step_visuals: List[Tuple[int, int, int]]
        :return: Generator[None, None, None]
        """
        if conscious[c.ID] != 0:
            conscious[c.ALIVE] = False
        else:
            conscious.step()
        yield


class ThreadID(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(ThreadID, self).__init__("i", work_space)

    def __call__(self,
                 portal: 'backrooms.portal.Portal',
                 rooms: Rooms,
                 conscious: c.Conscious,
                 rule_step_visuals: List[Tuple[int, int, int]]) -> Generator[None, None, None]:
        """
        info: Runs a rule.
        :param portal: Portal
        :param rooms: Rooms
        :param conscious: Conscious
        :param rule_step_visuals: List[Tuple[int, int, int]]
        :return: Generator[None, None, None]
        """
        conscious[c.WORK_STACK].push(conscious[c.ID])
        conscious.step()
        yield


class ThreadModule(RuleModule):
    def __init__(self,
                 work_space: WorkSpace):
        super(ThreadModule, self).__init__("t",
                                           work_space,
                                           (ThreadThread,
                                            ThreadJoin,
                                            ThreadID))


class HallwayCall(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(HallwayCall, self).__init__("c", work_space)

    def __call__(self,
                 portal: 'backrooms.portal.Portal',
                 rooms: Rooms,
                 conscious: c.Conscious,
                 rule_step_visuals: List[Tuple[int, int, int]]) -> Generator[None, None, None]:
        """
        info: Runs a rule.
        :param portal: Portal
        :param rooms: Rooms
        :param conscious: Conscious
        :param rule_step_visuals: List[Tuple[int, int, int]]
        :return: Generator[None, None, None]
        """
        hallway = conscious[c.WORK_STACK].pop()
        if isinstance(hallway, str):
            hallway = rooms.get_hallway_location(conscious[c.PC_FLOOR], hallway)
        elif isinstance(hallway, int) and rooms.find_hallway_location(hallway, conscious[c.PC_FLOOR]) != hallway:
            hallway = None
        if isinstance(hallway, (int, str)):
            conscious[c.FUNCTION_STACK].push(conscious[c.PC_X])
            conscious[c.FUNCTION_STACK].push(conscious[c.PC_Y])
            conscious[c.FUNCTION_STACK].push(conscious[c.PC_FLOOR])
            conscious[c.FUNCTION_STACK].push(conscious[c.PC_V_X])
            conscious[c.FUNCTION_STACK].push(conscious[c.PC_V_Y])
            conscious[c.FUNCTION_STACK].push(conscious[c.PC_V_FLOOR])
            conscious[c.PC_X] = 0
            conscious[c.PC_Y] = hallway
        else:
            conscious.step()
        yield


class HallwayLevelCall(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(HallwayLevelCall, self).__init__("l", work_space)

    def __call__(self,
                 portal: 'backrooms.portal.Portal',
                 rooms: Rooms,
                 conscious: c.Conscious,
                 rule_step_visuals: List[Tuple[int, int, int]]) -> Generator[None, None, None]:
        """
        info: Runs a rule.
        :param portal: Portal
        :param rooms: Rooms
        :param conscious: Conscious
        :param rule_step_visuals: List[Tuple[int, int, int]]
        :return: Generator[None, None, None]
        """
        hallway = conscious[c.WORK_STACK].pop()
        floor = conscious[c.WORK_STACK].pop()
        if isinstance(floor, str):
            floor = rooms.get_floor_level(floor)
        if isinstance(floor, int):
            if isinstance(hallway, str):
                hallway = rooms.get_hallway_location(floor, hallway)
            elif isinstance(hallway, int) and rooms.find_hallway_location(hallway, floor) != hallway:
                hallway = None
            if isinstance(hallway, (int, str)):
                conscious[c.FUNCTION_STACK].push(conscious[c.PC_X])
                conscious[c.FUNCTION_STACK].push(conscious[c.PC_Y])
                conscious[c.FUNCTION_STACK].push(conscious[c.PC_FLOOR])
                conscious[c.FUNCTION_STACK].push(conscious[c.PC_V_X])
                conscious[c.FUNCTION_STACK].push(conscious[c.PC_V_Y])
                conscious[c.FUNCTION_STACK].push(conscious[c.PC_V_FLOOR])
                conscious[c.PC_X] = 0
                conscious[c.PC_Y] = hallway
                conscious[c.PC_FLOOR] = floor
            else:
                conscious.step()
        else:
            conscious.step()
        yield


class HallwayReturn(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(HallwayReturn, self).__init__("r", work_space)

    def __call__(self,
                 portal: 'backrooms.portal.Portal',
                 rooms: Rooms,
                 conscious: c.Conscious,
                 rule_step_visuals: List[Tuple[int, int, int]]) -> Generator[None, None, None]:
        """
        info: Runs a rule.
        :param portal: Portal
        :param rooms: Rooms
        :param conscious: Conscious
        :param rule_step_visuals: List[Tuple[int, int, int]]
        :return: Generator[None, None, None]
        """
        v_floor = conscious[c.FUNCTION_STACK].pop()
        v_y = conscious[c.FUNCTION_STACK].pop()
        v_x = conscious[c.FUNCTION_STACK].pop()
        floor = conscious[c.FUNCTION_STACK].pop()
        y = conscious[c.FUNCTION_STACK].pop()
        x = conscious[c.FUNCTION_STACK].pop()
        if isinstance(v_x, int) and isinstance(v_y, int) and isinstance(v_floor, int):
            if isinstance(x, int) and isinstance(y, int) and isinstance(floor, int):
                conscious[c.PC_X] = x
                conscious[c.PC_Y] = y
                conscious[c.PC_FLOOR] = floor
                conscious[c.PC_V_X] = v_x
                conscious[c.PC_V_Y] = v_y
                conscious[c.PC_V_FLOOR] = v_floor
        conscious.step()
        yield


class HallwayGetName(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(HallwayGetName, self).__init__("n", work_space)

    def __call__(self,
                 portal: 'backrooms.portal.Portal',
                 rooms: Rooms,
                 conscious: c.Conscious,
                 rule_step_visuals: List[Tuple[int, int, int]]) -> Generator[None, None, None]:
        """
        info: Runs a rule.
        :param portal: Portal
        :param rooms: Rooms
        :param conscious: Conscious
        :param rule_step_visuals: List[Tuple[int, int, int]]
        :return: Generator[None, None, None]
        """
        floor = conscious[c.WORK_STACK].pop()
        hallway = conscious[c.WORK_STACK].pop()
        if isinstance(hallway, int) and isinstance(floor, int):
            hallway = rooms.find_hallway_location(hallway, floor)
            if hallway is not None:
                conscious[c.WORK_STACK].push(rooms.get_hallway_name(hallway, floor))
            else:
                conscious[c.WORK_STACK].push(None)
        conscious.step()
        yield


class HallwayGetLocation(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(HallwayGetLocation, self).__init__("g", work_space)

    def __call__(self,
                 portal: 'backrooms.portal.Portal',
                 rooms: Rooms,
                 conscious: c.Conscious,
                 rule_step_visuals: List[Tuple[int, int, int]]) -> Generator[None, None, None]:
        """
        info: Runs a rule.
        :param portal: Portal
        :param rooms: Rooms
        :param conscious: Conscious
        :param rule_step_visuals: List[Tuple[int, int, int]]
        :return: Generator[None, None, None]
        """
        floor = conscious[c.WORK_STACK].pop()
        hallway = conscious[c.WORK_STACK].pop()
        if isinstance(hallway, str) and isinstance(floor, int):
            conscious[c.WORK_STACK].push(rooms.get_hallway_location(floor, hallway))
        elif isinstance(hallway, int) and isinstance(floor, int):
            conscious[c.WORK_STACK].push(rooms.find_hallway_location(hallway, floor))
        conscious.step()
        yield


class HallwaySet(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(HallwaySet, self).__init__("s", work_space)

    def __call__(self,
                 portal: 'backrooms.portal.Portal',
                 rooms: Rooms,
                 conscious: c.Conscious,
                 rule_step_visuals: List[Tuple[int, int, int]]) -> Generator[None, None, None]:
        """
        info: Runs a rule.
        :param portal: Portal
        :param rooms: Rooms
        :param conscious: Conscious
        :param rule_step_visuals: List[Tuple[int, int, int]]
        :return: Generator[None, None, None]
        """
        floor = conscious[c.WORK_STACK].pop()
        hallway = conscious[c.WORK_STACK].pop()
        hallway_name = conscious[c.WORK_STACK].pop()
        if isinstance(floor, int) and isinstance(hallway, int)\
                and (isinstance(hallway_name, str) or hallway_name is None):
            rooms.set_hallway_name(hallway, floor, hallway_name)    # error handling
        conscious.step()
        yield


class HallwayRemove(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(HallwayRemove, self).__init__("d", work_space)

    def __call__(self,
                 portal: 'backrooms.portal.Portal',
                 rooms: Rooms,
                 conscious: c.Conscious,
                 rule_step_visuals: List[Tuple[int, int, int]]) -> Generator[None, None, None]:
        """
        info: Runs a rule.
        :param portal: Portal
        :param rooms: Rooms
        :param conscious: Conscious
        :param rule_step_visuals: List[Tuple[int, int, int]]
        :return: Generator[None, None, None]
        """
        hallway = conscious[c.WORK_STACK].pop()
        floor = conscious[c.WORK_STACK].pop()
        if isinstance(hallway, int) and isinstance(floor, int):
            rooms.remove_hallway(hallway, floor)
        conscious.step()
        yield


class HallwayModule(RuleModule):
    def __init__(self,
                 work_space: WorkSpace):
        super(HallwayModule, self).__init__("h",
                                            work_space,
                                            (HallwayCall,
                                             HallwayLevelCall,
                                             HallwayReturn,
                                             HallwayGetLocation,
                                             HallwayGetName,
                                             HallwaySet,
                                             HallwayRemove))


class HallwayGetFloorName(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(HallwayGetFloorName, self).__init__("n", work_space)

    def __call__(self,
                 portal: 'backrooms.portal.Portal',
                 rooms: Rooms,
                 conscious: c.Conscious,
                 rule_step_visuals: List[Tuple[int, int, int]]) -> Generator[None, None, None]:
        """
        info: Runs a rule.
        :param portal: Portal
        :param rooms: Rooms
        :param conscious: Conscious
        :param rule_step_visuals: List[Tuple[int, int, int]]
        :return: Generator[None, None, None]
        """
        floor = conscious[c.WORK_STACK].pop()
        if isinstance(floor, int):
            conscious[c.WORK_STACK].push(rooms.get_floor_name(floor))
        conscious.step()
        yield


class HallwayGetFloorLevel(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(HallwayGetFloorLevel, self).__init__("l", work_space)

    def __call__(self,
                 portal: 'backrooms.portal.Portal',
                 rooms: Rooms,
                 conscious: c.Conscious,
                 rule_step_visuals: List[Tuple[int, int, int]]) -> Generator[None, None, None]:
        """
        info: Runs a rule.
        :param portal: Portal
        :param rooms: Rooms
        :param conscious: Conscious
        :param rule_step_visuals: List[Tuple[int, int, int]]
        :return: Generator[None, None, None]
        """
        floor_name = conscious[c.WORK_STACK].pop()
        if isinstance(floor_name, str):
            conscious[c.WORK_STACK].push(rooms.get_floor_level(floor_name))
        conscious.step()
        yield


class HallwaySetFloorLevel(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(HallwaySetFloorLevel, self).__init__("s", work_space)

    def __call__(self,
                 portal: 'backrooms.portal.Portal',
                 rooms: Rooms,
                 conscious: c.Conscious,
                 rule_step_visuals: List[Tuple[int, int, int]]) -> Generator[None, None, None]:
        """
        info: Runs a rule.
        :param portal: Portal
        :param rooms: Rooms
        :param conscious: Conscious
        :param rule_step_visuals: List[Tuple[int, int, int]]
        :return: Generator[None, None, None]
        """
        floor_name = conscious[c.WORK_STACK].pop()
        floor_level = conscious[c.WORK_STACK].pop()
        if isinstance(floor_level, int) and (isinstance(floor_name, str) or floor_name is None):
            rooms.set_floor_name(floor_level, floor_name)
        conscious.step()
        yield


class LevelModule(RuleModule):
    def __init__(self,
                 work_space: WorkSpace):
        super(LevelModule, self).__init__("l",
                                          work_space,
                                          (HallwayGetFloorName,
                                           HallwayGetFloorLevel,
                                           HallwaySetFloorLevel))


class ReadFlip(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(ReadFlip, self).__init__("r", work_space)

    def __call__(self,
                 portal: 'backrooms.portal.Portal',
                 rooms: Rooms,
                 conscious: c.Conscious,
                 rule_step_visuals: List[Tuple[int, int, int]]) -> Generator[None, None, None]:
        """
        info: Runs a rule.
        :param portal: Portal
        :param rooms: Rooms
        :param conscious: Conscious
        :param rule_step_visuals: List[Tuple[int, int, int]]
        :return: Generator[None, None, None]
        """
        x = conscious[c.PC_X]
        y = conscious[c.PC_Y]
        floor = conscious[c.PC_FLOOR]
        v_x = conscious[c.PC_V_X] * -1
        v_y = conscious[c.PC_V_Y] * -1
        v_floor = conscious[c.PC_V_FLOOR] * -1
        conscious.step()
        yield
        for _ in _read(rooms, conscious, rule_step_visuals):
            yield
        conscious[c.PC_X] = x
        conscious[c.PC_Y] = y
        conscious[c.PC_FLOOR] = floor
        conscious[c.PC_V_X] = v_x
        conscious[c.PC_V_Y] = v_y
        conscious[c.PC_V_FLOOR] = v_floor
        conscious.step()
        conscious.step()
        yield


class WriteFlip(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(WriteFlip, self).__init__("w", work_space)

    def __call__(self,
                 portal: 'backrooms.portal.Portal',
                 rooms: Rooms,
                 conscious: c.Conscious,
                 rule_step_visuals: List[Tuple[int, int, int]]) -> Generator[None, None, None]:
        """
        info: Runs a rule.
        :param portal: Portal
        :param rooms: Rooms
        :param conscious: Conscious
        :param rule_step_visuals: List[Tuple[int, int, int]]
        :return: Generator[None, None, None]
        """
        x = conscious[c.PC_X]
        y = conscious[c.PC_Y]
        floor = conscious[c.PC_FLOOR]
        v_x = conscious[c.PC_V_X] * -1
        v_y = conscious[c.PC_V_Y] * -1
        v_floor = conscious[c.PC_V_FLOOR] * -1
        conscious.step()
        yield
        for character in ">1vur" + _write(rooms, conscious, rule_step_visuals):
            rooms.write(*conscious.at(), character=character)
            rule_step_visuals.append(conscious.at())
            conscious.step()
            yield
        conscious[c.PC_X] = x
        conscious[c.PC_Y] = y
        conscious[c.PC_FLOOR] = floor
        conscious[c.PC_V_X] = v_x
        conscious[c.PC_V_Y] = v_y
        conscious[c.PC_V_FLOOR] = v_floor
        conscious.step()
        conscious.step()
        yield


class DynamicDump(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(DynamicDump, self).__init__("d", work_space)

    def __call__(self,
                 portal: 'backrooms.portal.Portal',
                 rooms: Rooms,
                 conscious: c.Conscious,
                 rule_step_visuals: List[Tuple[int, int, int]]) -> Generator[None, None, None]:
        """
        info: Runs a rule.
        :param portal: Portal
        :param rooms: Rooms
        :param conscious: Conscious
        :param rule_step_visuals: List[Tuple[int, int, int]]
        :return: Generator[None, None, None]
        """
        v_floor = conscious[c.WORK_STACK].pop()
        v_y = conscious[c.WORK_STACK].pop()
        v_x = conscious[c.WORK_STACK].pop()
        floor = conscious[c.WORK_STACK].pop()
        y = conscious[c.WORK_STACK].pop()
        x = conscious[c.WORK_STACK].pop()
        item = conscious[c.WORK_STACK].pop()
        if isinstance(item, int):
            item = str(item)
        elif item is None or item is StackBottom:
            item = "n"
        elif item is StackFrame:
            item = "f"
        if isinstance(x, int) and isinstance(y, int) and isinstance(floor, int):
            if isinstance(v_x, int) and isinstance(v_y, int) and isinstance(v_floor, int):
                for character in item:
                    rooms.write(x, y, floor, character)
                    x += v_x
                    y += v_y
                    floor += v_floor
                    yield
        conscious.step()
        yield


class UncommonModule(RuleModule):
    def __init__(self,
                 work_space: WorkSpace):
        super(UncommonModule, self).__init__("u",
                                             work_space,
                                             (ReadFlip,
                                              WriteFlip,
                                              DynamicDump))


RULES = (Halt,
         Output,
         Input,
         One,
         Two,
         Three,
         Four,
         Five,
         Six,
         Seven,
         Eighth,
         Nine,
         Right,
         Left,
         Up,
         Down,
         DownUpper,
         Upper,
         Lower,
         Clear,
         LessThanZero,
         GreaterThanZero,
         Zero,
         NotZero,
         IsInteger,
         IsString,
         IsNone,
         IsStackFrame,
         IsStackBottom,
         Pop,
         Duplicate,
         Worker,
         Keep,
         Store,
         Read,
         Write,
         StringModule,
         IntegerModule,
         X,
         Y,
         Floor,
         ThreadModule,
         HallwayModule,
         LevelModule,
         UncommonModule)
