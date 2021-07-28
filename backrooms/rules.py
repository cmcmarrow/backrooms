"""
Copyright 2021 Charles McMarrow
"""

# built-in
from typing import Generator, Tuple, List, Dict, Union, Optional, Callable
from copy import deepcopy
import string

# backrooms
import backrooms    # import backrooms to avoid circular imports
from .backrooms_error import BackroomsError
from . import conscious as c
from .conscious import _to_int
from .rooms import Rooms, RoomsError
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


def _cast_to_int(obj: Union[int, str, StackFrame, StackBottom, None]) -> Optional[int]:
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


def _cast_string(obj: Union[int, str, StackFrame, StackBottom, None]) -> str:
    if isinstance(obj, int):
        return str(obj)
    elif obj is None:
        return "None"
    elif obj is StackFrame:
        return "StackFrame"
    elif obj is StackBottom:
        return "StackBottom"
    return obj


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


SHIFTER = "SHIFTER"
KEY_HOLDER = "KEY_HOLDER"
LOCK_COUNT = "LOCK_COUNT"


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


class BackMirror(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(BackMirror, self).__init__("\\", work_space)

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
        if conscious[c.PC_V_FLOOR] == 0:
            if conscious[c.PC_V_Y] == 0:
                if conscious[c.PC_V_X] == 1:
                    conscious[c.PC_V_X] = 0
                    conscious[c.PC_V_Y] = -1
                elif conscious[c.PC_V_X] == -1:
                    conscious[c.PC_V_X] = 0
                    conscious[c.PC_V_Y] = 1
            elif conscious[c.PC_V_X] == 0:
                if conscious[c.PC_V_Y] == 1:
                    conscious[c.PC_V_X] = -1
                    conscious[c.PC_V_Y] = 0
                elif conscious[c.PC_V_Y] == -1:
                    conscious[c.PC_V_X] = 1
                    conscious[c.PC_V_Y] = 0
        conscious.step()
        yield


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


class BranchLessThanZero(Branch):
    def __init__(self,
                 work_space: WorkSpace):
        super(BranchLessThanZero, self).__init__(c.BRANCH_LESS_THAN_ZERO, "L", work_space)


class BranchGreaterThanZero(Branch):
    def __init__(self,
                 work_space: WorkSpace):
        super(BranchGreaterThanZero, self).__init__(c.BRANCH_GREATER_THAN_ZERO, "G", work_space)


class BranchZero(Branch):
    def __init__(self,
                 work_space: WorkSpace):
        super(BranchZero, self).__init__(c.BRANCH_ZERO, "Z", work_space)


class BranchNotZero(Branch):
    def __init__(self,
                 work_space: WorkSpace):
        super(BranchNotZero, self).__init__(c.BRANCH_NOT_ZERO, "N", work_space)


class BranchIsInteger(Branch):
    def __init__(self,
                 work_space: WorkSpace):
        super(BranchIsInteger, self).__init__(c.BRANCH_IS_INTEGER, "I", work_space)


class BranchIsString(Branch):
    def __init__(self,
                 work_space: WorkSpace):
        super(BranchIsString, self).__init__(c.BRANCH_IS_STRING, "S", work_space)


class BranchIsNone(Branch):
    def __init__(self,
                 work_space: WorkSpace):
        super(BranchIsNone, self).__init__(c.BRANCH_IS_NONE, "O", work_space)


class BranchIsStackFrame(Branch):
    def __init__(self,
                 work_space: WorkSpace):
        super(BranchIsStackFrame, self).__init__(c.BRANCH_IS_STACK_FRAME, "F", work_space)


class BranchIsStackBottom(Branch):
    def __init__(self,
                 work_space: WorkSpace):
        super(BranchIsStackBottom, self).__init__(c.BRANCH_IS_STACK_BOTTOM, "B", work_space)


class Cite(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(Cite, self).__init__("c", work_space)

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


class ClearStack(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(ClearStack, self).__init__("n", work_space)

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
        conscious[c.WORK_STACK].clear()
        yield


class CoordinateX(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(CoordinateX, self).__init__("x", work_space)

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


class CoordinateY(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(CoordinateY, self).__init__("y", work_space)

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


class CoordinateFloor(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(CoordinateFloor, self).__init__("f", work_space)

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


class Echo(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(Echo, self).__init__("e", work_space)

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


class ForwardMirror(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(ForwardMirror, self).__init__("/", work_space)

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
        if conscious[c.PC_V_FLOOR] == 0:
            if conscious[c.PC_V_Y] == 0:
                if conscious[c.PC_V_X] == 1:
                    conscious[c.PC_V_X] = 0
                    conscious[c.PC_V_Y] = 1
                elif conscious[c.PC_V_X] == -1:
                    conscious[c.PC_V_X] = 0
                    conscious[c.PC_V_Y] = -1
            elif conscious[c.PC_V_X] == 0:
                if conscious[c.PC_V_Y] == 1:
                    conscious[c.PC_V_X] = 1
                    conscious[c.PC_V_Y] = 0
                elif conscious[c.PC_V_Y] == -1:
                    conscious[c.PC_V_X] = -1
                    conscious[c.PC_V_Y] = 0
        conscious.step()
        yield


def _process_hallway_arg(hallway: Union[int, str, StackFrame, StackBottom, None],
                         floor: int,
                         rooms: Rooms) -> Optional[int]:

    if isinstance(hallway, str):
        hallway_str = hallway
        hallway = rooms.get_hallway_location(floor, hallway)
        if hallway is None:
            hallway = len(hallway_str)
            hallway = rooms.find_hallway_location(hallway, floor)
    else:
        hallway = rooms.find_hallway_location(_to_int(hallway), floor)

    if not isinstance(hallway, int):
        hallway = rooms.find_hallway_location(_to_int(hallway), floor)
    return hallway


def _process_floor_arg(floor: Union[int, str, StackFrame, StackBottom, None],
                       rooms: Rooms) -> int:
    if isinstance(floor, str):
        floor_str = floor
        floor = rooms.get_floor_level(floor)
        if floor is None:
            floor = len(floor_str)
        return floor
    return _to_int(floor)


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
        hallway = _process_hallway_arg(conscious[c.WORK_STACK].pop(), conscious[c.PC_FLOOR], rooms)

        if isinstance(hallway, int):
            conscious[c.FUNCTION_STACK].push(conscious[c.PC_X])
            conscious[c.FUNCTION_STACK].push(conscious[c.PC_Y])
            conscious[c.FUNCTION_STACK].push(conscious[c.PC_FLOOR])
            conscious[c.FUNCTION_STACK].push(conscious[c.PC_V_X])
            conscious[c.FUNCTION_STACK].push(conscious[c.PC_V_Y])
            conscious[c.FUNCTION_STACK].push(conscious[c.PC_V_FLOOR])
            conscious[c.FUNCTION_STACK].push(conscious[c.R0])
            conscious[c.FUNCTION_STACK].push(conscious[c.R1])
            conscious[c.FUNCTION_STACK].push(conscious[c.R2])
            conscious[c.FUNCTION_STACK].push(conscious[c.R3])
            conscious[c.FUNCTION_STACK].push(conscious[c.R4])
            conscious[c.FUNCTION_STACK].push(conscious[c.R5])
            conscious[c.FUNCTION_STACK].push(conscious[c.R6])
            conscious[c.FUNCTION_STACK].push(conscious[c.R7])
            conscious[c.FUNCTION_STACK].push(conscious[c.R8])
            conscious[c.FUNCTION_STACK].push(conscious[c.R9])
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
        floor = _process_floor_arg(conscious[c.WORK_STACK].pop(), rooms)
        hallway = _process_hallway_arg(hallway, floor, rooms)

        if isinstance(floor, int):
            # get hallway coord
            if isinstance(hallway, str):
                hallway = rooms.get_hallway_location(floor, hallway)
            else:
                hallway = _to_int(hallway)
                if rooms.find_hallway_location(hallway, floor) != hallway:
                    hallway = None

            if isinstance(hallway, int):
                conscious[c.FUNCTION_STACK].push(conscious[c.PC_X])
                conscious[c.FUNCTION_STACK].push(conscious[c.PC_Y])
                conscious[c.FUNCTION_STACK].push(conscious[c.PC_FLOOR])
                conscious[c.FUNCTION_STACK].push(conscious[c.PC_V_X])
                conscious[c.FUNCTION_STACK].push(conscious[c.PC_V_Y])
                conscious[c.FUNCTION_STACK].push(conscious[c.PC_V_FLOOR])
                conscious[c.FUNCTION_STACK].push(conscious[c.R0])
                conscious[c.FUNCTION_STACK].push(conscious[c.R1])
                conscious[c.FUNCTION_STACK].push(conscious[c.R2])
                conscious[c.FUNCTION_STACK].push(conscious[c.R3])
                conscious[c.FUNCTION_STACK].push(conscious[c.R4])
                conscious[c.FUNCTION_STACK].push(conscious[c.R5])
                conscious[c.FUNCTION_STACK].push(conscious[c.R6])
                conscious[c.FUNCTION_STACK].push(conscious[c.R7])
                conscious[c.FUNCTION_STACK].push(conscious[c.R8])
                conscious[c.FUNCTION_STACK].push(conscious[c.R9])
                conscious[c.PC_X] = 0
                conscious[c.PC_Y] = hallway
                conscious[c.PC_FLOOR] = floor
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
        r9 = conscious[c.FUNCTION_STACK].pop()
        r8 = conscious[c.FUNCTION_STACK].pop()
        r7 = conscious[c.FUNCTION_STACK].pop()
        r6 = conscious[c.FUNCTION_STACK].pop()
        r5 = conscious[c.FUNCTION_STACK].pop()
        r4 = conscious[c.FUNCTION_STACK].pop()
        r3 = conscious[c.FUNCTION_STACK].pop()
        r2 = conscious[c.FUNCTION_STACK].pop()
        r1 = conscious[c.FUNCTION_STACK].pop()
        r0 = conscious[c.FUNCTION_STACK].pop()
        v_floor = conscious[c.FUNCTION_STACK].pop()
        v_y = conscious[c.FUNCTION_STACK].pop()
        v_x = conscious[c.FUNCTION_STACK].pop()
        floor = conscious[c.FUNCTION_STACK].pop()
        y = conscious[c.FUNCTION_STACK].pop()
        x = conscious[c.FUNCTION_STACK].pop()
        if isinstance(v_x, int) and isinstance(v_y, int) and isinstance(v_floor, int):
            if isinstance(x, int) and isinstance(y, int) and isinstance(floor, int):
                conscious[c.R0] = r0
                conscious[c.R1] = r1
                conscious[c.R2] = r2
                conscious[c.R3] = r3
                conscious[c.R4] = r4
                conscious[c.R5] = r5
                conscious[c.R6] = r6
                conscious[c.R7] = r7
                conscious[c.R8] = r8
                conscious[c.R9] = r9
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
        hallway = _to_int(conscious[c.WORK_STACK].pop())
        floor = _process_floor_arg(conscious[c.WORK_STACK].pop(), rooms)
        conscious[c.WORK_STACK].push(rooms.get_hallway_name(hallway, floor))
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
        hallway = conscious[c.WORK_STACK].pop()
        floor = _process_floor_arg(conscious[c.WORK_STACK].pop(), rooms)
        if isinstance(hallway, str):
            conscious[c.WORK_STACK].push(rooms.get_hallway_location(floor, hallway))
        else:
            hallway = _to_int(hallway)
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
        hallway = _to_int(conscious[c.WORK_STACK].pop())
        floor = _process_floor_arg(conscious[c.WORK_STACK].pop(), rooms)
        hallway_name = conscious[c.WORK_STACK].pop()
        if hallway_name is not None:
            hallway_name = _cast_string(hallway_name)
        try:
            rooms.set_hallway_name(hallway, floor, hallway_name)
        except RoomsError:
            # hallway name is in valid make it None
            rooms.set_hallway_name(hallway, floor, None)
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
        floor = _process_floor_arg(conscious[c.WORK_STACK].pop(), rooms)
        hallway = _process_hallway_arg(hallway, floor, rooms)
        if isinstance(hallway, int):
            rooms.remove_hallway(hallway, floor)
        conscious.step()
        yield


class HallwayPast(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(HallwayPast, self).__init__("p", work_space)

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
        floor = _process_floor_arg(conscious[c.WORK_STACK].pop(), rooms)
        hallway = _process_hallway_arg(hallway, floor, rooms)
        if isinstance(hallway, int):
            conscious[c.WORK_STACK].push(rooms.get_past_hallway_location(hallway, floor))
        else:
            conscious[c.WORK_STACK].push(None)
        conscious.step()
        yield


class HallwayNext(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(HallwayNext, self).__init__("e", work_space)

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
        floor = _process_floor_arg(conscious[c.WORK_STACK].pop(), rooms)
        hallway = _process_hallway_arg(hallway, floor, rooms)
        if isinstance(hallway, int):
            conscious[c.WORK_STACK].push(rooms.get_next_hallway_location(hallway, floor))
        else:
            conscious[c.WORK_STACK].push(None)
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
                                             HallwayRemove,
                                             HallwayPast,
                                             HallwayNext))


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


class HopeOne(Hope):
    def __init__(self,
                 work_space: WorkSpace):
        super(HopeOne, self).__init__("1", work_space)


class HopeTwo(Hope):
    def __init__(self,
                 work_space: WorkSpace):
        super(HopeTwo, self).__init__("2", work_space)


class HopeThree(Hope):
    def __init__(self,
                 work_space: WorkSpace):
        super(HopeThree, self).__init__("3", work_space)


class HopeFour(Hope):
    def __init__(self,
                 work_space: WorkSpace):
        super(HopeFour, self).__init__("4", work_space)


class HopeFive(Hope):
    def __init__(self,
                 work_space: WorkSpace):
        super(HopeFive, self).__init__("5", work_space)


class HopeSix(Hope):
    def __init__(self,
                 work_space: WorkSpace):
        super(HopeSix, self).__init__("6", work_space)


class HopeSeven(Hope):
    def __init__(self,
                 work_space: WorkSpace):
        super(HopeSeven, self).__init__("7", work_space)


class HopeEighth(Hope):
    def __init__(self,
                 work_space: WorkSpace):
        super(HopeEighth, self).__init__("8", work_space)


class HopeNine(Hope):
    def __init__(self,
                 work_space: WorkSpace):
        super(HopeNine, self).__init__("9", work_space)


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
        yield
        if rooms.read(*conscious.at()).isdigit():
            conscious[f"R{rooms.read(*conscious.at())}"] = conscious[c.WORK_STACK].peak()
            conscious.step()
        yield


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
        conscious[c.WORK_STACK].push(_cast_to_int(item))
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
        back = _to_int(conscious[c.WORK_STACK].pop())
        front = _to_int(conscious[c.WORK_STACK].pop())
        try:
            conscious[c.WORK_STACK].push(int(self._operation(front, back)))
        except ZeroDivisionError:
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
        super(IntegerPower, self).__init__(int.__pow__, "p", work_space)


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
        item = _to_int(conscious[c.WORK_STACK].pop())
        if 0 <= item < 256:
            conscious[c.WORK_STACK].push(chr(item))
        else:
            conscious[c.WORK_STACK].push(None)
        conscious.step()
        yield


class IntegerAbsolute(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(IntegerAbsolute, self).__init__("l", work_space)

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
        item = _to_int(conscious[c.WORK_STACK].pop())
        conscious[c.WORK_STACK].push(abs(item))
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
                                             IntegerByte,
                                             IntegerAbsolute))


class LevelGetFloorName(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(LevelGetFloorName, self).__init__("n", work_space)

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
        floor = _to_int(conscious[c.WORK_STACK].pop())
        conscious[c.WORK_STACK].push(rooms.get_floor_name(floor))
        conscious.step()
        yield


class LevelGetFloorLevel(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(LevelGetFloorLevel, self).__init__("l", work_space)

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
        floor_name = _cast_string(conscious[c.WORK_STACK].pop())
        conscious[c.WORK_STACK].push(rooms.get_floor_level(floor_name))
        conscious.step()
        yield


class LevelSetFloorName(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(LevelSetFloorName, self).__init__("s", work_space)

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
        if floor_name is not None:
            floor_name = _cast_string(floor_name)
        floor_level = _to_int(conscious[c.WORK_STACK].pop())
        if isinstance(floor_name, str) or floor_name is None:
            try:
                rooms.set_floor_name(floor_level, floor_name)
            except RoomsError:
                pass
        conscious.step()
        yield


class LevelModule(RuleModule):
    def __init__(self,
                 work_space: WorkSpace):
        super(LevelModule, self).__init__("l",
                                          work_space,
                                          (LevelGetFloorName,
                                           LevelGetFloorLevel,
                                           LevelSetFloorName))


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


class PopFrame(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(PopFrame, self).__init__("a", work_space)

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
        conscious[c.WORK_STACK].pop_frame()
        conscious.step()
        yield


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
        conscious[c.BRANCH] = c.BRANCH_CLEAR


class ShifterRight(Shifter):
    def __init__(self,
                 work_space: WorkSpace):
        super(ShifterRight, self).__init__(1, 0, 0, ">", work_space)


class ShifterLeft(Shifter):
    def __init__(self,
                 work_space: WorkSpace):
        super(ShifterLeft, self).__init__(-1, 0, 0, "<", work_space)


class ShifterUp(Shifter):
    def __init__(self,
                 work_space: WorkSpace):
        super(ShifterUp, self).__init__(0, 1, 0, "^", work_space)


class ShifterDown(Shifter):
    def __init__(self,
                 work_space: WorkSpace):
        super(ShifterDown, self).__init__(0, -1, 0, "v", work_space)


class ShifterDownUpper(Shifter):
    def __init__(self,
                 work_space: WorkSpace):
        super(ShifterDownUpper, self).__init__(0, -1, 0, "V", work_space)


class ShifterUpper(Shifter):
    def __init__(self,
                 work_space: WorkSpace):
        super(ShifterUpper, self).__init__(0, 0, 1, "{", work_space)


class ShifterLower(Shifter):
    def __init__(self,
                 work_space: WorkSpace):
        super(ShifterLower, self).__init__(0, 0, -1, "}", work_space)


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
        yield
        if rooms.read(*conscious.at()).isdigit():
            conscious[c.WORK_STACK].push(conscious[f"R{rooms.read(*conscious.at())}"])
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
        item = _cast_string(conscious[c.WORK_STACK].pop())
        conscious[c.WORK_STACK].push(len(item))
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
        conscious[c.WORK_STACK].push(_cast_string(item))
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
        at = _to_int(conscious[c.WORK_STACK].pop())
        item = _cast_string(conscious[c.WORK_STACK].pop())
        try:
            conscious[c.WORK_STACK].push(item[at])
        except IndexError:
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
        item = _cast_string(conscious[c.WORK_STACK].pop())
        if len(item) <= 1:
            conscious[c.WORK_STACK].push(ord(item[0]))
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
        item = _cast_string(conscious[c.WORK_STACK].pop())
        back = item[at:]
        front = item[:at]
        conscious[c.WORK_STACK].push(back)
        conscious[c.WORK_STACK].push(front)
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
        back = _cast_string(conscious[c.WORK_STACK].pop())
        front = _cast_string(conscious[c.WORK_STACK].pop())
        conscious[c.WORK_STACK].push(front + back)
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
        string_2 = _cast_string(conscious[c.WORK_STACK].pop())
        string_1 = _cast_string(conscious[c.WORK_STACK].pop())
        conscious[c.WORK_STACK].push(int(string_1 == string_2))
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
        string_2 = _cast_string(conscious[c.WORK_STACK].pop())
        string_1 = _cast_string(conscious[c.WORK_STACK].pop())
        conscious[c.WORK_STACK].push(int(string_1 in string_2))
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
        item = _cast_string(conscious[c.WORK_STACK].pop())
        conscious[c.WORK_STACK].push(item.upper())
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
        item = _cast_string(conscious[c.WORK_STACK].pop())
        conscious[c.WORK_STACK].push(item.lower())
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


class Switch(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(Switch, self).__init__("z", work_space)

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
        item_2 = conscious[c.WORK_STACK].pop()
        item_1 = conscious[c.WORK_STACK].pop()
        conscious[c.WORK_STACK].push(item_2)
        conscious[c.WORK_STACK].push(item_1)
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
        new_conscious[c.WORK_STACK] = deepcopy(conscious[c.WORK_STACK])
        new_conscious[c.R0] = conscious[c.R0]
        new_conscious[c.R1] = conscious[c.R1]
        new_conscious[c.R2] = conscious[c.R2]
        new_conscious[c.R3] = conscious[c.R3]
        new_conscious[c.R4] = conscious[c.R4]
        new_conscious[c.R5] = conscious[c.R5]
        new_conscious[c.R6] = conscious[c.R6]
        new_conscious[c.R7] = conscious[c.R7]
        new_conscious[c.R8] = conscious[c.R8]
        new_conscious[c.R9] = conscious[c.R9]
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


class ThreadLock(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(ThreadLock, self).__init__("l", work_space)
        self.get_work_space()[KEY_HOLDER] = None
        self.get_work_space()[LOCK_COUNT] = 0

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
        if self.get_work_space()[KEY_HOLDER] is None:
            self.get_work_space()[KEY_HOLDER] = conscious[c.ID]
            self.get_work_space()[LOCK_COUNT] = 1
            conscious.step()
        elif self.get_work_space()[KEY_HOLDER] == conscious[c.ID]:
            self.get_work_space()[LOCK_COUNT] += 1
            conscious.step()
        else:   # TODO fix hack
            conscious[c.PC_X] += conscious[c.PC_V_X] * -1
            conscious[c.PC_Y] += conscious[c.PC_V_Y] * -1
            conscious[c.PC_FLOOR] += conscious[c.PC_V_FLOOR] * -1
        yield


class ThreadUnLock(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(ThreadUnLock, self).__init__("u", work_space)

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
        # check if conscious is the key holder
        if self.get_work_space()[KEY_HOLDER] == conscious[c.ID]:
            self.get_work_space()[LOCK_COUNT] += -1
            # check if lock count is 0
            if not self.get_work_space()[LOCK_COUNT]:
                # remove conscious as key holder
                self.get_work_space()[KEY_HOLDER] = None
        conscious.step()
        yield


class ThreadModule(RuleModule):
    def __init__(self,
                 work_space: WorkSpace):
        super(ThreadModule, self).__init__("t",
                                           work_space,
                                           (ThreadThread,
                                            ThreadJoin,
                                            ThreadID,
                                            ThreadLock,
                                            ThreadUnLock))


class UncommonReadFlip(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(UncommonReadFlip, self).__init__("r", work_space)

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


class UncommonWriteFlip(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(UncommonWriteFlip, self).__init__("w", work_space)

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


class UncommonHotPatch(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(UncommonHotPatch, self).__init__("h", work_space)

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
        v_floor = conscious[c.PC_V_FLOOR]
        v_y = conscious[c.PC_V_Y]
        v_x = conscious[c.PC_V_X]
        floor = conscious[c.PC_FLOOR]
        y = conscious[c.PC_Y]
        x = conscious[c.PC_X]
        item = _cast_string(conscious[c.WORK_STACK].pop())
        for character in item:
            x += v_x
            y += v_y
            floor += v_floor
            rooms.write(x, y, floor, character)
            yield
        conscious.step()
        yield


class UncommonSimpleDump(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(UncommonSimpleDump, self).__init__("s", work_space)

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
        v_floor = conscious[c.PC_V_FLOOR]
        v_y = conscious[c.PC_V_Y]
        v_x = conscious[c.PC_V_X]
        floor = _to_int(conscious[c.WORK_STACK].pop())
        y = _to_int(conscious[c.WORK_STACK].pop())
        x = _to_int(conscious[c.WORK_STACK].pop())
        item = _cast_string(conscious[c.WORK_STACK].pop())
        for character in item:
            rooms.write(x, y, floor, character)
            x += v_x
            y += v_y
            floor += v_floor
            yield
        conscious.step()
        yield


class UncommonDynamicDump(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(UncommonDynamicDump, self).__init__("d", work_space)

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
        v_floor = _to_int(conscious[c.WORK_STACK].pop())
        v_y = _to_int(conscious[c.WORK_STACK].pop())
        v_x = _to_int(conscious[c.WORK_STACK].pop())
        floor = _to_int(conscious[c.WORK_STACK].pop())
        y = _to_int(conscious[c.WORK_STACK].pop())
        x = _to_int(conscious[c.WORK_STACK].pop())
        item = _cast_string(conscious[c.WORK_STACK].pop())
        for character in item:
            rooms.write(x, y, floor, character)
            x += v_x
            y += v_y
            floor += v_floor
            yield
        conscious.step()
        yield


class UncommonDoubleDuplicate(Rule):
    def __init__(self,
                 work_space: WorkSpace):
        super(UncommonDoubleDuplicate, self).__init__("o", work_space)

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
        item_2 = conscious[c.WORK_STACK].pop()
        item_1 = conscious[c.WORK_STACK].pop()
        for _ in range(2):
            conscious[c.WORK_STACK].push(item_1)
            conscious[c.WORK_STACK].push(item_2)
        conscious.step()
        yield


class UncommonModule(RuleModule):
    def __init__(self,
                 work_space: WorkSpace):
        super(UncommonModule, self).__init__("u",
                                             work_space,
                                             (UncommonHotPatch,
                                              UncommonReadFlip,
                                              UncommonWriteFlip,
                                              UncommonSimpleDump,
                                              UncommonDynamicDump,
                                              UncommonDoubleDuplicate))


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


RULES = (BackMirror,
         BranchLessThanZero,
         BranchGreaterThanZero,
         BranchZero,
         BranchNotZero,
         BranchIsInteger,
         BranchIsString,
         BranchIsNone,
         BranchIsStackFrame,
         BranchIsStackBottom,
         Cite,
         ClearStack,
         CoordinateX,
         CoordinateY,
         CoordinateFloor,
         Duplicate,
         Echo,
         ForwardMirror,
         HallwayModule,
         Halt,
         HopeOne,
         HopeTwo,
         HopeThree,
         HopeFour,
         HopeFive,
         HopeSix,
         HopeSeven,
         HopeEighth,
         HopeNine,
         IntegerModule,
         LevelModule,
         Keep,
         Pop,
         PopFrame,
         Read,
         ShifterRight,
         ShifterLeft,
         ShifterUp,
         ShifterDown,
         ShifterDownUpper,
         ShifterUpper,
         ShifterLower,
         Store,
         Switch,
         StringModule,
         ThreadModule,
         UncommonModule,
         Write)
