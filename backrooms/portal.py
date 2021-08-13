"""
Copyright 2021 Charles McMarrow

This script holds a simple portal "CPU".
"""


# built-in
from collections import deque
from pprint import pformat
from string import ascii_letters, digits
from typing import Dict, Generator, List, Optional, Tuple, Type, Union

# backrooms
from . import backrooms_error
from . import whisper
from .conscious import ALIVE, Conscious, HALT, ID
from .rooms import Rooms
from .rules import CoreDump, RULES, Rule, WorkSpace

VALID_INPUT_CHARACTERS = set(ascii_letters + digits + ",<.>/?;:'\"[{]}\\|`!@#$%^&*()-_=+ ")


class PortalError(backrooms_error.BackroomsError):
    @classmethod
    def missing_gate(cls):
        """
        info: Used to indicate no gate could be found.
        :return: PortalError
        """
        return cls("Missing entry point 'GATE'!")

    @classmethod
    def lost_count(cls):
        """
        info: Used to indicate to many Rules where ran.
        :return: PortalError
        """
        return cls("Lost count hit! Got lost in the backrooms!")

    @classmethod
    def lost_rule_count(cls):
        """
        info: Used to indicate a Rule ran for to long.
        :return: PortalError
        """
        return cls("Lost rule count hit! Got lost in the backrooms!")

    @classmethod
    def error_on_space(cls, x: int, y: int, floor: int):
        """
        info: Used to indicate space was read as a Rule.
        :return: PortalError
        """
        return cls(f"Error on space at: ({x}, {y}, {floor})")

    @classmethod
    def start_character_collection(cls,
                                   start_character: str):
        """
        info: Used to indicate two or more Rules had a start charter conflict.
        :return: PortalError
        """
        return cls(f"{repr(start_character)} is used more then once in a work space!")

    @classmethod
    def multiple_inputs_methods(cls):
        """
        info: Used to indicate that inputs and feeder where both given.
        :return: PortalError
        """
        return cls("Can't provide both inputs and feeder augments!")


class Feeder:
    def __init__(self):
        """
        Makes a Feeder which gets an input from program.
        """
        self._need_input: bool = False
        self._input: Optional[str] = None

    def need_input(self) -> None:
        """
        info: Tells Feed that input is needed.
        :return: None
        """
        self._need_input = True

    def wants_input(self) -> bool:
        """
        info: Indicates if a input is needed.
        :return: bool
        """
        return self._need_input

    def get_input(self) -> Optional[str]:
        """
        info: Gets input if any.
        :return: Optional[str]
        """
        user_input = self._input
        self._input = None
        return user_input

    def set_input(self, user_input: str) -> None:
        """
        info: Gets input for consumption.
        :param user_input: str
        :return: None
        """
        self._input = user_input
        self._need_input = False


class Portal:
    def __init__(self,
                 rooms: Rooms,
                 consciouses: Optional[Tuple[Conscious, ...]] = None,
                 inputs: Optional[Union[Tuple[str, ...], List[str]]] = None,
                 feeder: Optional[Feeder] = None,
                 sys_output: bool = True,
                 catch_output: bool = False,
                 lost_count: int = 0,
                 lost_rule_count: int = 0,
                 error_on_space: bool = False,
                 core_dump: bool = False,
                 yields: bool = False,
                 rules: Optional[Union[Tuple[Type[Rule], ...], List[Type[Rule]]]] = None):
        """
        info: Makes a Portal which executes Rules in Rooms.
        :param rooms: Rooms
        :param consciouses: Optional[Tuple[Conscious, ...]]
        :param inputs: Optional[Union[Tuple[str, ...], List[str]]]
        :param feeder: Optional[Feeder]
        :param sys_output: bool
        :param catch_output: bool
        :param lost_count: int
        :param lost_rule_count: int
        :param error_on_space: bool
        :param core_dump: bool
        :param yields: bool
        :param rules: Optional[Union[Tuple[Type[Rule], ...], List[Type[Rule]]]]
        :exception PortalError
            raises PortalError if no gate could be found.
            raises PortalError if two or more Rules had a start charter conflict.
        """
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
        self._feeder: Optional[Feeder] = feeder

        if inputs is not None and feeder is not None:
            raise PortalError.multiple_inputs_methods()

        self._catch_output: bool = catch_output
        self._catch_output_steam: List[object] = []
        self._error_on_space: bool = error_on_space

        work_space = WorkSpace()

        if rules is None:
            rules = RULES

        if core_dump:
            rules = list(rules) + [CoreDump]
        rules_obj = [rule(work_space=work_space, yields=yields) for rule in rules]
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

    def __call__(self) -> None:
        """
        info: Will execute the program.
        :return: None
        """
        for operation_generator in self:
            for step in operation_generator:
                if whisper.WHISPER_RUNNING:
                    whisper.debug(f"Step: {step}")

    def __iter__(self) -> 'Portal':
        """
        info: Gives the iter that gives the next Rule to be executed.
        :return: 'Portal'
        """
        return self

    def __next__(self) -> Generator[int, None, None]:
        """
        info: Gives the Rule to be executed.
        :return: Generator[int, None, None]
        """
        if self._done:
            raise StopIteration()
        self._rule_step_visuals.clear()
        return self._run_rule()

    def _run_rule(self) -> Generator[int, None, None]:
        """
        info: Will execute a Rule.
        :exception PortalError
            PortalError if to many Rules where ran.
            PortalError if a Rule ran for to long.
            PortalError if space was read as a Rule.
        :return: Generator[int, None, None]
        """
        # check if any consciouses remain
        if not len(self._consciouses):
            self._done = True
            if whisper.WHISPER_RUNNING:
                whisper.debug("HALT")
        else:
            # get next conscious
            conscious = self._consciouses.popleft()
            if whisper.WHISPER_RUNNING:
                # whisper conscious location
                whisper.info(f"{conscious[ID]} {conscious.at()}: {repr(self._rooms.read(*conscious.at()))}")
                whisper.debug("Conscious:\n" + pformat(conscious))
            # get rule
            rule = self._rules.get(self._rooms.read(*conscious.at()))
            self._rule_step_visuals.append(conscious.at())
            if rule is not None:
                if whisper.WHISPER_RUNNING:
                    whisper.debug(f"Rule found: {rule.__class__.__name__}")
                # run operation "rule"
                for step, _ in enumerate(rule(self,
                                              self._rooms,
                                              conscious,
                                              conscious.at(),
                                              self._rule_step_visuals)):
                    step += 1
                    if step == self._lost_rule_count:
                        raise PortalError.lost_rule_count()
                    yield step
            else:
                # whisper that no rule was found for charter
                if whisper.WHISPER_RUNNING:
                    whisper.debug("No rule found!")
                if self._error_on_space and self._rooms.read(*conscious.at()) == " ":
                    raise PortalError.error_on_space(*conscious.at())
                conscious.step()
            # check if conscious is still alive
            if conscious[ALIVE]:
                # add conscious back to thread queue
                self._consciouses.append(conscious)
            else:
                if whisper.WHISPER_RUNNING:
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
                    if whisper.WHISPER_RUNNING:
                        whisper.debug("HALT")

            if whisper.WHISPER_RUNNING:
                whisper.debug(f"Step visuals: {self._rule_step_visuals}")

            # check if conscious raised HALT
            if conscious[HALT] and not self._done:
                # program is done running
                self._done = True
                if whisper.WHISPER_RUNNING:
                    whisper.debug("HALT")

            # check if lost count has been hit
            if self._lost_count > 0:
                self._lost_count += -1
                if not self._lost_count:
                    raise PortalError.lost_count()

    def is_done(self) -> bool:
        """
        info: Checks if program is done running.
        :return: bool
        """
        return self._done

    def get_rooms(self) -> Rooms:
        """
        info: Gets Rooms used by program.
        :return: Rooms
        """
        return self._rooms

    def get_consciouses(self) -> Tuple[Conscious, ...]:
        """
        info: Gets all running consciouses.
        :return: Tuple[Conscious, ...]
        """
        return tuple(self._consciouses)

    def new_conscious(self) -> Conscious:
        """
        info: Makes a new Conscious and put it into the update loop.
        :return: Conscious
        """
        new_conscious = Conscious()
        if self._free_ids:
            free_id = min(self._free_ids)
            self._free_ids.remove(free_id)
            new_conscious[ID] = free_id
        else:
            new_conscious[ID] = self._next_free_id
            self._next_free_id += 1
        self._consciouses.append(new_conscious)
        return new_conscious

    def read_input(self) -> Optional[str]:
        """
        info: Gets input from Portal.
        :return: str
        """
        data = ""
        if self._inputs is None and self._feeder is None:
            data = input()
        elif self._inputs is not None:
            if self._inputs:
                data = self._inputs.pop()
        else:
            data = self._feeder.get_input()
            if data is None:
                self._feeder.need_input()
                return data

        valid_data = ""
        for character in data:
            if character in VALID_INPUT_CHARACTERS:
                valid_data += character
        return valid_data

    def write_output(self, output: object) -> None:
        """
        info: Writes out to Portal.
        :param output: object
        :return: None
        """
        if self._sys_output:
            print(output, end="", flush=True)

        if self._catch_output:
            self._catch_output_steam.append(output)

    def get_output_stream(self) -> List[object]:
        """
        info: Gets the output stream.
            Note anything can be done to the list returned.
        :return: List[object]
        """
        return self._catch_output_steam

    def get_step_visuals(self) -> List[Tuple[int, int, int]]:
        """
        info: Gets step visuals for current rule that is executing.
            Note the list should only be read and the list will change when portal takes another step.
        :return: List[Tuple[int, int, int]]
        """
        return self._rule_step_visuals
