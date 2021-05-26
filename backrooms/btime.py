"""
Copyright 2021 Charles McMarrow
"""


from .backrooms import BackroomsD, BackRoomsCordD
from .stack import Stack

from typing import Optional, Tuple


FRAGMENT_LOCATION_KEY = "location"

FRAGMENT_VECTOR_KEY = "vector"
FRAGMENT_VECTOR_LEFT = BackRoomsCordD(-1, 0, 0)
FRAGMENT_VECTOR_RIGHT = BackRoomsCordD(1, 0, 0)
FRAGMENT_VECTOR_UP = BackRoomsCordD(0, 1, 0)
FRAGMENT_VECTOR_DOWN = BackRoomsCordD(0, -1, 0)
FRAGMENT_VECTOR_ABOVE = BackRoomsCordD(0, 0, -1)
FRAGMENT_VECTOR_BELOW = BackRoomsCordD(0, 0, 1)

FRAGMENT_HALT_KEY = "halt"
FRAGMENT_SILENT_KEY = "silent"
FRAGMENT_MERCIFUL_KEY = "merciful"
FRAGMENT_BACKROOMS_D_KEY = "backrooms_d"
FRAGMENT_WORKSPACE_STACK_KEY = "workspace_stack"
FRAGMENT_RETURN_STACK_KEY = "return_stack"
FRAGMENT_ERROR_KEY = "error"
FRAGMENT_SKIP_KEY = "skip"
FRAGMENT_BRANCH_KEY = "branch"


class BTimeError(Exception):
    @classmethod
    def missing_gate(cls):
        return cls("Backrooms don't have an open 'GATE'!")

    @classmethod
    def rule_collision(cls, rule_identifier: str):
        # some like to give rules that make it impossible to leave.
        # For these types don't open the gate, they lack self control
        return cls(f"Rule collision: '{rule_identifier}'")

    @classmethod
    def merciful(cls):
        return cls("MERCIFUL!")


class Fragment(dict):
    def __init__(self,
                 backrooms_d: BackroomsD,
                 location: BackRoomsCordD,
                 vector: Optional[BackRoomsCordD] = None,
                 **kwargs: dict):
        super(Fragment, self).__init__()

        if vector is None:
            vector = FRAGMENT_VECTOR_RIGHT

        self[FRAGMENT_BACKROOMS_D_KEY] = backrooms_d
        self[FRAGMENT_LOCATION_KEY] = location
        self[FRAGMENT_VECTOR_KEY] = vector
        self[FRAGMENT_WORKSPACE_STACK_KEY] = Stack()
        self[FRAGMENT_RETURN_STACK_KEY] = Stack()
        self[FRAGMENT_HALT_KEY] = False
        self[FRAGMENT_ERROR_KEY] = 0
        self[FRAGMENT_SKIP_KEY] = 0
        self[FRAGMENT_BRANCH_KEY] = "C"
        self.update(kwargs)

    def step(self):
        vector = self[FRAGMENT_VECTOR_KEY]
        self[FRAGMENT_LOCATION_KEY] = self[FRAGMENT_LOCATION_KEY].shift(vector.x, vector.y, vector.z)

    def read(self):
        return self[FRAGMENT_BACKROOMS_D_KEY].read(self[FRAGMENT_LOCATION_KEY])

    def write(self, entity: str):
        self[FRAGMENT_BACKROOMS_D_KEY].write(self[FRAGMENT_LOCATION_KEY], entity)


class Rule:
    def __init__(self, identifier: str):
        self._identifier = identifier

    def __call__(self, fragment: Fragment, b_time: "BTime"):
        raise NotImplementedError()

    def get_identifier(self) -> str:
        return self._identifier


class BTime:
    def __init__(self,
                 backrooms_d: BackroomsD,
                 rules: Tuple[Rule],
                 silent=False,
                 merciful=False,
                 dummy_input=None):
        self._backrooms_d = backrooms_d
        # TODO rule colletion
        self._rules = {rule.get_identifier(): rule for rule in rules}
        self._silent = silent
        self._merciful = merciful
        self._halted = False
        self._step_count = 0

        entity_point = self._backrooms_d.get_first_hallway("GATE")
        if entity_point is None:
            raise BTimeError.missing_gate()
        # TODO fragment to fragments
        self._fragment = Fragment(self._backrooms_d,
                                  entity_point)

        self._dummy_output = []
        if dummy_input is None:
            dummy_input = []
        self._dummy_input = dummy_input
        self._dummy_input.reverse()

    def __next__(self):
        if self.is_haled():
            raise StopIteration()
        print()
        print("AT:", self._fragment[FRAGMENT_LOCATION_KEY], repr(self._fragment.read()))
        print("STACK:", self._fragment[FRAGMENT_WORKSPACE_STACK_KEY])
        entity = self._fragment.read()
        # got lost in the backrooms
        if entity == " " and self._merciful:
            raise BTimeError.merciful()

        rule = self._rules.get(entity)
        # execute rule
        if rule is not None:
            rule(self._fragment, self)
        else:
            # no rule given NOP do nothing but take a step
            self._fragment.step()
        self._step_count += 1
        # check if fragment raised halt flag
        self._halted = self._fragment[FRAGMENT_HALT_KEY]

    def __iter__(self):
        return self

    def run(self) -> None:
        for _ in self:
            pass

    def is_haled(self) -> bool:
        return self._halted

    def get_step_count(self) -> int:
        return self._step_count

    @property
    def dummy_output(self):
        return self._dummy_output

    @property
    def dummy_input(self):
        return self._dummy_input

    def dummy_write(self, output):
        self.dummy_output.append(output)

    def dummy_read(self):
        if self.dummy_input:
            return self.dummy_input.pop()
        # ran out of dummy input
        return ""
