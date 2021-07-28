"""
Copyright 2021 Charles McMarrow

This script holds a simple portal "CPU".
"""


# built-in
from collections import deque
from string import ascii_letters, digits
from typing import Tuple, Optional, Dict, List

# backrooms
from . import backrooms_error
from .conscious import Conscious, ALIVE, ID, HALT
from . import conscious as c
from .rooms import Rooms
from .rules import Rule, RULES, WorkSpace
from . import whisper


VALID_INPUT_CHARACTERS = set(ascii_letters + digits + ",<.>/?;:'\"[{]}\\|`!@#$%^&*()-_=+ ")


class PortalError(backrooms_error.BackroomsError):
    @classmethod
    def missing_gate(cls):
        return cls("Missing entry point 'GATE'!")

    @classmethod
    def lost_count(cls):
        return cls("Lost count hit! Got lost in the backrooms!")

    @classmethod
    def lost_rule_count(cls):
        return cls("Lost rule count hit! Got lost in the backrooms!")

    @classmethod
    def error_on_space(cls, x: int, y: int, floor: int):
        return cls(f"Error on space at: ({x}, {y}, {floor})")

    @classmethod
    def start_character_collection(cls,
                                   start_character: str):
        return cls(f"{repr(start_character)} is used more then once in a work space!")


class Portal:
    def __init__(self,
                 rooms: Rooms,
                 consciouses: Optional[Tuple[Conscious, ...]] = None,
                 inputs: Optional[Tuple[str, ...]] = None,
                 sys_output: bool = True,
                 catch_output: bool = False,
                 lost_count: int = 0,
                 lost_rule_count: int = 0,
                 error_on_space: bool = False):
        self._done: bool = False
        self._rooms: Rooms = rooms

        if not consciouses:
            hallway_cord = rooms.find_a_hallway("GATE")
            if hallway_cord is None:
                raise PortalError.missing_gate()
            y, floor = hallway_cord
            consciouses = (Conscious(PC_Y=y, PC_FLOOR=floor, ID=0),)

        self._consciouses: deque = deque(consciouses)
        self._lost_count: int = lost_count
        self._lost_rule_count: int = lost_rule_count
        self._sys_output: bool = sys_output
        if inputs is not None:
            inputs = list(inputs[::-1])
        self._inputs: Optional[List[str]] = inputs
        self._catch_output: bool = catch_output
        self._catch_output_steam: List[str] = []
        self._error_on_space: bool = error_on_space

        work_space = WorkSpace()
        rules_obj = [rule(work_space=work_space) for rule in RULES]
        self._rules: Dict[str: Rule] = {}

        for rule in rules_obj:
            if rule.get_start_character() in self._rules:
                raise PortalError.start_character_collection(rule.get_start_character())
            self._rules[rule.get_start_character()] = rule

        used_ids = set(conscious[ID] for conscious in self._consciouses)
        self._next_free_id = max(used_ids) + 1
        self._free_ids: set = set()

        for free_id in range(self._next_free_id):
            if free_id not in used_ids:
                self._free_ids.add(free_id)

        self._rule_step_visuals: List[Tuple[int, int, int]] = []

    def __call__(self):
        for operation_generator in self:
            for step in operation_generator:
                whisper.debug(f"Step: {step}")

    def __iter__(self):
        return self

    def __next__(self):
        if self.is_done():
            raise StopIteration()

        def _run_rule():
            # check if any consciouses remain
            if not len(self._consciouses):
                self._done = True
                whisper.debug("HALT")
            else:
                # get next conscious
                conscious = self._consciouses.popleft()
                # whisper conscious location
                whisper.info(f"{conscious[ID]} {conscious.at()}: {repr(self._rooms.read(*conscious.at()))}")
                whisper.debug(f"{conscious[c.R0]} {conscious[c.R1]} "
                              f"{conscious[c.R2]} {conscious[c.R3]} {conscious[c.R4]} {conscious[c.R5]} "
                              f"{conscious[c.R6]} {conscious[c.R7]} {conscious[c.R8]} {conscious[c.R9]}")
                whisper.debug(f"{conscious[c.BRANCH]} {repr(conscious[c.WORK_STACK].peak())} "
                              f"{conscious[c.FUNCTION_STACK].peak()}")
                # get rule
                rule = self._rules.get(self._rooms.read(*conscious.at()))
                self._rule_step_visuals.clear()
                self._rule_step_visuals.append(conscious.at())
                if rule is not None:
                    whisper.debug(f"Rule found: {rule.__class__.__name__}")
                    # run operation "rule"
                    for step, _ in enumerate(rule(self, self._rooms, conscious, self._rule_step_visuals)):
                        step += 1
                        if step == self._lost_rule_count:
                            raise PortalError.lost_rule_count()
                        yield step
                else:
                    # whisper that no rule was found for charter
                    whisper.debug(f"No rule found!")
                    if self._error_on_space and self._rooms.read(*conscious.at()) == " ":
                        raise PortalError.error_on_space(*conscious.at())
                    conscious.step()
                # check if conscious is still alive
                if conscious[ALIVE]:
                    # add conscious back to thread queue
                    self._consciouses.append(conscious)
                else:
                    whisper.debug("not ALIVE")
                    # free conscious id
                    self._free_ids.add(conscious[ID])
                    while self._next_free_id - 1 in self._free_ids:
                        self._free_ids.remove(self._next_free_id - 1)
                        self._next_free_id += -1
                    # check if any consciouses remain
                    if not len(self._consciouses):
                        # program is done running
                        self._done = True
                        whisper.debug("HALT")

                whisper.debug(f"Step visuals: {self._rule_step_visuals}")

                # check if conscious raised HALT
                if conscious[HALT] and not self.is_done():
                    # program is done running
                    self._done = True
                    whisper.debug("HALT")

                # check if lost count has been hit
                if self._lost_count > 0:
                    self._lost_count += -1
                    if not self._lost_count:
                        raise PortalError.lost_count()
        return _run_rule()

    def is_done(self) -> bool:
        return self._done

    def get_rooms(self) -> Rooms:
        return self._rooms

    def get_consciouses(self) -> Tuple[Conscious, ...]:
        return tuple(self._consciouses)

    def new_conscious(self) -> Conscious:
        new_conscious = Conscious()
        if self._free_ids:
            # TODO min(set) is Big-O(n)
            free_id = min(self._free_ids)
            self._free_ids.remove(free_id)
            new_conscious[ID] = free_id
        else:
            new_conscious[ID] = self._next_free_id
            self._next_free_id += 1
        self._consciouses.append(new_conscious)
        return new_conscious

    def read_input(self) -> str:    # TODO write test
        """
        info: Gets input from portal
        :return: str
        """
        data = ""
        if self._inputs is None:
            data = input()
        elif self._inputs:
            data = self._inputs.pop()

        valid_data = ""
        for character in data:
            if character in VALID_INPUT_CHARACTERS:
                valid_data += character
        return valid_data

    def write_output(self, output: str) -> None:    # TODO write test for
        """
        info: Writes out to Portal.
        :param output: str
        :return: None
        """
        if self._sys_output:
            print(output, end="", flush=True)

        if self._catch_output:
            self._catch_output_steam.append(output)

    def get_output_stream(self) -> List[str]:   # TODO write test for
        """
        info: Gets the output stream.
            Note anything can be done to the list returned.
        :return: List[str]
        """
        return self._catch_output_steam

    def get_step_visuals(self) -> List[Tuple[int, int, int]]:   # TODO write test for
        """
        info: Gets step visuals for current rule that is executing.
            Note the list should only be read and the list will change when portal takes another step.
        :return: List[Tuple[int, int, int]]
        """
        return self._rule_step_visuals
