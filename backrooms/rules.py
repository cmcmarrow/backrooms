"""
Copyright 2021 Charles McMarrow
"""

# built-in
from typing import Generator, Tuple, List
import string

# backrooms
from .backrooms_error import BackroomsError
from . import conscious as c
from .rooms import Rooms
from .stack import StackFrame, StackBottom
from . import whisper


class RuleError(BackroomsError):
    pass


class Rule:
    def __init__(self, start_character: str):
        self._start_character = start_character

    def __call__(self,
                 portal: 'Portal',
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

    def get_start_character(self):
        return self._start_character


def _branch(conscious: c.Conscious) -> bool:
    """
    info: Decides if rule should branch.
    :param conscious: c.Conscious
    :return: bool
    """
    if conscious[c.BRANCH] == c.BRANCH_CLEAR:
        return True

    item = conscious[c.WORK_STACK].peak()
    if item is StackFrame or item is StackBottom:
        return False
    elif item is None:
        item = 0
    elif isinstance(item, str):
        item = int(bool(item))
    if conscious[c.BRANCH] == c.BRANCH_LESS_THAN_ZERO:
        return item < 0
    elif conscious[c.BRANCH] == c.BRANCH_GREATER_THAN_ZERO:
        return item > 0
    elif conscious[c.BRANCH] == c.BRANCH_ZERO:
        return item == 0
    elif conscious[c.BRANCH] == c.BRANCH_NOT_ZERO:
        return item != 0
    whisper.critical(f"Branch is in a bad state: {conscious[c.BRANCH]}!")
    return False


class VectorShift(Rule):
    def __init__(self,
                 start_character: str,
                 x: int,
                 y: int,
                 floor: int):
        self._x: int = x
        self._y: int = y
        self._floor: int = floor
        super(VectorShift, self).__init__(start_character)

    def __call__(self,
                 portal: 'Portal',
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
        if not _branch(conscious):
            conscious.step()
            return
        conscious[c.PC_V_X] = self._x
        conscious[c.PC_V_Y] = self._y
        conscious[c.PC_V_FLOOR] = self._floor
        conscious.step()
        yield
        if rooms.read(*conscious.at()) == self.get_start_character():
            rule_step_visuals.append(conscious.at())
            conscious.step()
            yield
            skip_count = 0
            while True:
                charter = rooms.read(*conscious.at())
                if charter in "^V<>/\\|":
                    if skip_count == 0:
                        break
                    skip_count += -1
                elif charter == "!":
                    skip_count += 1
                rule_step_visuals.append(conscious.at())
                conscious.step()
                yield


class UpShift(VectorShift):
    def __init__(self):
        super(UpShift, self).__init__("^", 0, 1, 0)


class DownShift(VectorShift):
    def __init__(self):
        super(DownShift, self).__init__("V", 0, -1, 0)


class LeftShift(VectorShift):
    def __init__(self):
        super(LeftShift, self).__init__("<", -1, 0, 0)


class RightShift(VectorShift):
    def __init__(self):
        super(RightShift, self).__init__(">", 1, 0, 0)


class AboveShift(VectorShift):
    def __init__(self):
        super(AboveShift, self).__init__("/", 1, 0, 1)


class LowerShift(VectorShift):
    def __init__(self):
        super(LowerShift, self).__init__("\\", 0, 0, -1)


class Halt(Rule):
    def __init__(self):
        super(Halt, self).__init__("~")

    def __call__(self,
                 portal: 'Portal',
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
            rule_step_visuals.append(conscious.at())
            conscious.step()
            yield
            if rooms.read(*conscious.at()) == "a":
                rule_step_visuals.append(conscious.at())
                conscious.step()
                conscious[c.ALIVE] = False
                conscious[c.HALT] = True
                yield


class Branch(Rule):
    def __init__(self, start_character: str, branch_state: str):
        """
        info: Will change the branch register.
        :param start_character: str
        :param branch_state: str
        """
        self._branch_state: str = branch_state
        super(Branch, self).__init__(start_character)

    def __call__(self,
                 portal: 'Portal',
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
        conscious[c.BRANCH] = self._branch_state
        conscious.step()
        yield


class Clear(Branch):
    def __init__(self):
        super(Clear, self).__init__("C", c.BRANCH_CLEAR)


class LessThanZero(Branch):
    def __init__(self):
        super(LessThanZero, self).__init__("L", c.BRANCH_LESS_THAN_ZERO)


class GreaterThanZero(Branch):
    def __init__(self):
        super(GreaterThanZero, self).__init__("G", c.BRANCH_GREATER_THAN_ZERO)


class Zero(Branch):
    def __init__(self):
        super(Zero, self).__init__("Z", c.BRANCH_ZERO)


class NotZero(Branch):
    def __init__(self):
        super(NotZero, self).__init__("N", c.BRANCH_NOT_ZERO)


class Hope(Rule):
    def __init__(self, digit: str):
        self._hope = int(digit)
        super(Hope, self).__init__(digit)

    def __call__(self,
                 portal: 'Portal',
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
        for _ in range(self._hope + 1):
            conscious.step()
        yield


class HopeOne(Hope):
    def __init__(self):
        super(HopeOne, self).__init__("1")


class HopeTwo(Hope):
    def __init__(self):
        super(HopeTwo, self).__init__("2")


class HopeThree(Hope):
    def __init__(self):
        super(HopeThree, self).__init__("3")


class HopeFour(Hope):
    def __init__(self):
        super(HopeFour, self).__init__("4")


class HopeFive(Hope):
    def __init__(self):
        super(HopeFive, self).__init__("5")


class HopeSix(Hope):
    def __init__(self):
        super(HopeSix, self).__init__("6")


class HopeSeven(Hope):
    def __init__(self):
        super(HopeSeven, self).__init__("7")


class HopeEight(Hope):
    def __init__(self):
        super(HopeEight, self).__init__("8")


class HopeNine(Hope):
    def __init__(self):
        super(HopeNine, self).__init__("9")


class Duplicate(Rule):
    def __init__(self):
        super(Duplicate, self).__init__("d")

    def __call__(self,
                 portal: 'Portal',
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
        stack = conscious[c.WORK_STACK]
        item = stack.peak()
        if item is StackBottom:
            item = None
        stack.push(item)
        conscious.step()
        yield


class Pop(Rule):
    def __init__(self):
        super(Pop, self).__init__("p")

    def __call__(self,
                 portal: 'Portal',
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


class Move(Rule):
    def __init__(self):
        super(Move, self).__init__("m")

    def __call__(self,
                 portal: 'Portal',
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
        conscious[conscious[c.WORKING_REGISTER]] = conscious[c.WORK_STACK].peak()
        conscious.step()
        yield


class Store(Rule):
    def __init__(self):
        super(Store, self).__init__("s")

    def __call__(self,
                 portal: 'Portal',
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
        conscious[c.WORK_STACK].push(conscious[conscious[c.WORKING_REGISTER]])
        conscious.step()
        yield


class Worker(Rule):
    def __init__(self):
        super(Worker, self).__init__("w")

    def __call__(self,
                 portal: 'Portal',
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
        register = rooms.read(*conscious.at())
        if register in string.digits:
            rule_step_visuals.append(conscious.at())
            conscious[c.WORKING_REGISTER] = f"R{register}"
            yield


class _Read(Rule):
    def __init__(self, start_character: str, flip: bool):
        self._flip = flip
        super(_Read, self).__init__(start_character)

    def __call__(self,
                 portal: 'Portal',
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
        at = conscious.at()
        conscious.step()
        yield
        read_type = rooms.read(*conscious.at())
        if read_type == "n":
            conscious[c.WORK_STACK].push(None)
            rule_step_visuals.append(conscious.at())
            conscious.step()
            yield
        elif read_type == "f":
            conscious[c.WORK_STACK].push(StackFrame)
            rule_step_visuals.append(conscious.at())
            conscious.step()
            yield
        elif read_type == "b":
            conscious[c.WORK_STACK].push(StackBottom)
            rule_step_visuals.append(conscious.at())
            conscious.step()
            yield
        elif read_type == "s":
            rule_step_visuals.append(conscious.at())
            conscious.step()
            yield
            exit_character = rooms.read(*conscious.at())
            read_string = ""
            conscious.step()
            yield
            while exit_character != rooms.read(*conscious.at()):
                read_string += rooms.read(*conscious.at())
                rule_step_visuals.append(conscious.at())
                conscious.step()
                yield
            rule_step_visuals.append(conscious.at())
            conscious.step()
            conscious[c.WORK_STACK].push(read_string)
            yield
        elif read_type in string.digits + "-":
            pass
        if self._flip:
            conscious[c.PC_X] = at[0]
            conscious[c.PC_Y] = at[1]
            conscious[c.PC_FLOOR] = at[2]

            conscious[c.PC_V_X] *= -1
            conscious[c.PC_V_Y] *= -1
            conscious[c.PC_V_FLOOR] *= -1
            conscious.step()


class Read(_Read):
    def __init__(self):
        super(Read, self).__init__("r", False)


class FRead(_Read):
    def __init__(self):
        super(FRead, self).__init__("a", True)


class _Write(Rule):
    def __init__(self):
        super(_Write, self).__init__("w")

    def __call__(self,
                 portal: 'Portal',
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


RULES = (UpShift,
         DownShift,
         LeftShift,
         RightShift,
         AboveShift,
         LowerShift,
         Halt,
         Clear,
         LessThanZero,
         GreaterThanZero,
         Zero,
         NotZero,
         HopeOne,
         HopeTwo,
         HopeThree,
         HopeFour,
         HopeFive,
         HopeSix,
         HopeSeven,
         HopeEight,
         HopeNine,
         Duplicate,
         Pop,
         Move,
         Store,
         Worker,
         Read,
         FRead)
