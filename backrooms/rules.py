"""
Copyright 2021 Charles McMarrow
"""


from .btime import Rule, Fragment, BTime
from . import btime
from . import stack
from string import digits
from backrooms.backrooms import BackRoomsCordD, BackRoomsError


def get_built_in_rules() -> tuple:
    """
    Gets a tuple of all built in rules.
    """
    return (Echo(),
            TypeLoad(),
            Halt(),
            Operators(),
            Jump(),
            Return(),
            JumpM(),
            Left(),
            Right(),
            Down(),
            Up(),
            Above(),
            Below(),
            Pop(),
            Duplicate(),
            Say(),
            Write(),
            Skip(),
            Hope1(),
            Hope2(),
            Hope3(),
            Hope4(),
            Hope5(),
            Hope6(),
            Hope7(),
            Hope8(),
            Hope9(),
            Clear(),
            Negative(),
            Zero(),
            Positive(),
            Equal())


class Echo(Rule):
    def __init__(self,
                 identifier: str = "e"):
        super(Echo, self).__init__(identifier=identifier)

    def __call__(self, fragment: Fragment, b_time: BTime):
        # get item on top of workspace stack
        obj = fragment[btime.FRAGMENT_WORKSPACE_STACK_KEY].peak()
        if obj not in (stack.StackFrame, stack.StackBottom):
            # print item on top of workspace stack
            print(obj, end="")
        elif isinstance(obj, stack.StackFrame):
            # cant print StackFrame
            fragment[btime.FRAGMENT_ERROR_KEY] = 1
        else:
            # cant print StackBottom
            fragment[btime.FRAGMENT_ERROR_KEY] = 2
        fragment.step()


def process_frequency_int(fragment: Fragment) -> int:
    fragment.step()
    number_str = fragment.read()
    if number_str not in "-" + digits:
        return 0

    fragment.step()
    while True:
        digit_c = fragment.read()
        if digit_c not in digits:
            break
        number_str += digit_c
        fragment.step()
    try:
        return int(number_str)
    except ValueError:
        pass
    return 0


def process_whisper_string(fragment: Fragment) -> str:
    fragment.step()
    terminator_char = fragment.read()
    fragment.step()
    data = ""
    while True:
        c = fragment.read()
        if terminator_char == c:
            return data
        data += c

        special_c = data[-2:]
        if special_c == "\\n":
            data = data[:-2] + "\n"
        elif special_c == "\\t":
            data = data[:-2] + "\t"
        fragment.step()


class TypeLoad(Rule):
    def __init__(self,
                 identifier: str = "t"):
        super(TypeLoad, self).__init__(identifier=identifier)

    def __call__(self, fragment: Fragment, b_time: BTime):
        fragment.step()
        b_type = fragment.read()
        if b_type in "sn":
            if b_type == "n":
                fragment[btime.FRAGMENT_WORKSPACE_STACK_KEY].push(process_frequency_int(fragment))
            else:
                fragment[btime.FRAGMENT_WORKSPACE_STACK_KEY].push(process_whisper_string(fragment))
                fragment.step()
        else:
            fragment[btime.FRAGMENT_ERROR_KEY] = 1


class Halt(Rule):
    def __init__(self,
                 identifier: str = "h"):
        super(Halt, self).__init__(identifier=identifier)

    def __call__(self, fragment: Fragment, b_time: BTime) -> None:
        # haul must see a~ for it to raise the HALT flag
        fragment.step()
        c = fragment.read()
        if c == "a":
            fragment.step()
            c = fragment.read()
            if c == "~":
                fragment.step()
                fragment[btime.FRAGMENT_HALT_KEY] = True


class Operators(Rule):
    def __init__(self,
                 identifier: str = "o"):
        super(Operators, self).__init__(identifier=identifier)
        self._operations = {"a": "__add__",
                            "s": "__sub__",
                            "m": "__mul__",
                            "d": "__floordiv__",
                            "p": "__pow__",
                            "o": "__mod__"}

    def __call__(self, fragment: Fragment, b_time: BTime) -> None:
        fragment.step()
        # get operation
        operation = self._operations.get(fragment.read())

        # operation not found
        if operation is None:
            return

        fragment.step()
        try:
            obj_2 = fragment[btime.FRAGMENT_WORKSPACE_STACK_KEY].pop()
            obj_1 = fragment[btime.FRAGMENT_WORKSPACE_STACK_KEY].pop()
        except stack.StackError:
            fragment[btime.FRAGMENT_ERROR_KEY] = 2
            return

        try:
            # run operation
            results = getattr(obj_1, operation)(obj_2)
        except Exception:
            fragment[btime.FRAGMENT_ERROR_KEY] = 1
            return

        fragment[btime.FRAGMENT_WORKSPACE_STACK_KEY].push(results)


class Direction(Rule):
    def __init__(self,
                 identifier: str,
                 vector: BackRoomsCordD):
        super(Direction, self).__init__(identifier=identifier)
        self._vector = vector

    def __call__(self, fragment: Fragment, b_time: BTime) -> None:
        if fragment[btime.FRAGMENT_SKIP_KEY] != 0:
            fragment[btime.FRAGMENT_SKIP_KEY] -= 1
            fragment.step()
            return

        if fragment[btime.FRAGMENT_BRANCH_KEY] != "C":
            try:
                if fragment[btime.FRAGMENT_BRANCH_KEY] == "P" and fragment[btime.FRAGMENT_WORKSPACE_STACK_KEY].peak() > 0:
                    fragment[btime.FRAGMENT_BRANCH_KEY] = "C"
                elif fragment[btime.FRAGMENT_BRANCH_KEY] == "Z" and fragment[btime.FRAGMENT_WORKSPACE_STACK_KEY].peak() == 0:
                    fragment[btime.FRAGMENT_BRANCH_KEY] = "C"
                elif fragment[btime.FRAGMENT_BRANCH_KEY] == "N" and fragment[btime.FRAGMENT_WORKSPACE_STACK_KEY].peak() < 0:
                    fragment[btime.FRAGMENT_BRANCH_KEY] = "C"
                else:
                    fragment.step()
                    return
            except Exception:
                fragment[btime.FRAGMENT_ERROR_KEY] = 1

        fragment[btime.FRAGMENT_VECTOR_KEY] = self._vector
        fragment.step()

        if fragment.read() == self.get_identifier():
            fragment.step()
            while fragment.read() not in "<>^V{}":
                fragment.step()


class Left(Direction):
    def __init__(self):
        super(Left, self).__init__("<", btime.FRAGMENT_VECTOR_LEFT)


class Right(Direction):
    def __init__(self):
        super(Right, self).__init__(">", btime.FRAGMENT_VECTOR_RIGHT)


class Up(Direction):
    def __init__(self):
        super(Up, self).__init__("^", btime.FRAGMENT_VECTOR_UP)


class Down(Direction):
    def __init__(self):
        super(Down, self).__init__("V", btime.FRAGMENT_VECTOR_DOWN)


class Above(Direction):
    def __init__(self):
        super(Above, self).__init__("}", btime.FRAGMENT_VECTOR_ABOVE)


class Below(Direction):
    def __init__(self):
        super(Below, self).__init__("{", btime.FRAGMENT_VECTOR_BELOW)


class Return(Rule):
    def __init__(self,
                 identifier: str = "r"):
        super(Return, self).__init__(identifier=identifier)

    def __call__(self, fragment: Fragment, b_time: BTime) -> None:
        try:
            fragment[btime.FRAGMENT_LOCATION_KEY] = fragment[btime.FRAGMENT_RETURN_STACK_KEY].pop()
        except stack.StackError:
            fragment[btime.FRAGMENT_ERROR_KEY] = 1
            fragment.step()


class Jump(Rule):
    def __init__(self,
                 identifier: str = "j"):
        super(Jump, self).__init__(identifier=identifier)

    def __call__(self, fragment: Fragment, b_time: BTime) -> None:
        hallway_name = process_whisper_string(fragment)
        fragment.step()
        try:
            ret = fragment[btime.FRAGMENT_LOCATION_KEY]
            hallway = fragment[btime.FRAGMENT_BACKROOMS_D_KEY].get_hallway(ret.z,
                                                                           hallway_name)
            fragment[btime.FRAGMENT_LOCATION_KEY] = BackRoomsCordD(0, hallway.y, ret.z)
            fragment[btime.FRAGMENT_RETURN_STACK_KEY].push(ret)
        except BackRoomsError:
            fragment[btime.FRAGMENT_ERROR_KEY] = 1


class JumpM(Rule):
    def __init__(self,
                 identifier: str = "m"):
        super(JumpM, self).__init__(identifier=identifier)

    def __call__(self, fragment: Fragment, b_time: BTime) -> None:
        backroom_name = process_whisper_string(fragment)
        hallway_name = process_whisper_string(fragment)
        fragment.step()
        try:
            ret = fragment[btime.FRAGMENT_LOCATION_KEY]
            backrooms = fragment[btime.FRAGMENT_BACKROOMS_D_KEY].get_backrooms_from_name(backroom_name)
            if backrooms is None:
                fragment[btime.FRAGMENT_ERROR_KEY] = 1
                return
            z = fragment[btime.FRAGMENT_BACKROOMS_D_KEY].get_backroom_id(backrooms)
            hallway = fragment[btime.FRAGMENT_BACKROOMS_D_KEY].get_hallway(z,
                                                                           hallway_name)
            fragment[btime.FRAGMENT_LOCATION_KEY] = BackRoomsCordD(0, hallway.y, z)
            fragment[btime.FRAGMENT_RETURN_STACK_KEY].push(ret)
        except BackRoomsError:
            fragment[btime.FRAGMENT_ERROR_KEY] = 1


class Pop(Rule):
    def __init__(self,
                 identifier: str = "p"):
        super(Pop, self).__init__(identifier=identifier)

    def __call__(self, fragment: Fragment, b_time: BTime) -> None:
        fragment.step()
        try:
            fragment[btime.FRAGMENT_WORKSPACE_STACK_KEY].pop()
        except stack.StackError:
            fragment[btime.FRAGMENT_ERROR_KEY] = 1


class Duplicate(Rule):
    def __init__(self,
                 identifier: str = "d"):
        super(Duplicate, self).__init__(identifier=identifier)

    def __call__(self, fragment: Fragment, b_time: BTime) -> None:
        fragment.step()
        obj = fragment[btime.FRAGMENT_WORKSPACE_STACK_KEY].peak()
        if obj == stack.StackBottom:
            fragment[btime.FRAGMENT_ERROR_KEY] = 1
        else:
            fragment[btime.FRAGMENT_WORKSPACE_STACK_KEY].push(obj)


class Say(Rule):
    def __init__(self,
                 identifier: str = "s"):
        super(Say, self).__init__(identifier=identifier)

    def __call__(self, fragment: Fragment, b_time: BTime) -> None:
        fragment.step()
        b_type = fragment.read()
        if b_type in "sn":
            if b_type == "n":
                try:
                    fragment[btime.FRAGMENT_WORKSPACE_STACK_KEY].push(int(input("> ")))
                except ValueError:
                    fragment[btime.FRAGMENT_ERROR_KEY] = 2
            else:
                user_input = "".join(input("> ").split("~"))
                fragment[btime.FRAGMENT_WORKSPACE_STACK_KEY].push(user_input)
            fragment.step()
        else:
            fragment[btime.FRAGMENT_ERROR_KEY] = 1


class Write(Rule):
    def __init__(self,
                 identifier: str = "w"):
        super(Write, self).__init__(identifier=identifier)

    def __call__(self, fragment: Fragment, b_time: BTime) -> None:
        fragment.step()
        terminator_char = fragment.read()
        try:
            obj = fragment[btime.FRAGMENT_WORKSPACE_STACK_KEY].peak()
        except stack.StackError:
            fragment[btime.FRAGMENT_ERROR_KEY] = 1
            return

        if isinstance(obj, (int, str)):
            if isinstance(obj, str):
                fragment.step()
                raw_obj = "ts" + terminator_char + obj + terminator_char
            else:
                raw_obj = "tn" + str(obj)
            fragment[btime.FRAGMENT_BACKROOMS_D_KEY].write_line(fragment[btime.FRAGMENT_LOCATION_KEY],
                                                                fragment[btime.FRAGMENT_VECTOR_KEY],
                                                                raw_obj)
            for _ in range(len(raw_obj)):
                fragment.step()
        else:
            fragment[btime.FRAGMENT_ERROR_KEY] = 2


class Skip(Rule):
    def __init__(self,
                 identifier: str = "!"):
        super(Skip, self).__init__(identifier=identifier)

    def __call__(self, fragment: Fragment, b_time: BTime) -> None:
        fragment.step()
        fragment[btime.FRAGMENT_SKIP_KEY] += 1


class Hope(Rule):
    def __init__(self,
                 identifier: str):
        super(Hope, self).__init__(identifier=identifier)

    def __call__(self, fragment: Fragment, b_time: BTime) -> None:
        fragment.step()
        for _ in range(int(self.get_identifier())):
            fragment.step()


class Hope1(Hope):
    def __init__(self):
        super(Hope1, self).__init__(identifier="1")


class Hope2(Hope):
    def __init__(self):
        super(Hope2, self).__init__(identifier="2")


class Hope3(Hope):
    def __init__(self):
        super(Hope3, self).__init__(identifier="3")


class Hope4(Hope):
    def __init__(self):
        super(Hope4, self).__init__(identifier="4")


class Hope5(Hope):
    def __init__(self):
        super(Hope5, self).__init__(identifier="5")


class Hope6(Hope):
    def __init__(self):
        super(Hope6, self).__init__(identifier="6")


class Hope7(Hope):
    def __init__(self):
        super(Hope7, self).__init__(identifier="7")


class Hope8(Hope):
    def __init__(self):
        super(Hope8, self).__init__(identifier="8")


class Hope9(Hope):
    def __init__(self):
        super(Hope9, self).__init__(identifier="9")


class Branch(Rule):
    def __init__(self,
                 identifier: str):
        super(Branch, self).__init__(identifier=identifier)

    def __call__(self, fragment: Fragment, b_time: BTime) -> None:
        fragment[btime.FRAGMENT_BRANCH_KEY] = self.get_identifier()
        fragment.step()


class Clear(Branch):
    def __init__(self):
        super(Clear, self).__init__(identifier="C")


class Positive(Branch):
    def __init__(self):
        super(Positive, self).__init__(identifier="P")


class Zero(Branch):
    def __init__(self):
        super(Zero, self).__init__(identifier="Z")


class Negative(Branch):
    def __init__(self):
        super(Negative, self).__init__(identifier="N")


class Equal(Rule):
    def __init__(self,
                 identifier: str = "="):
        super(Equal, self).__init__(identifier=identifier)

    def __call__(self, fragment: Fragment, b_time: BTime) -> None:
        fragment.step()
        try:
            obj_2 = fragment[btime.FRAGMENT_WORKSPACE_STACK_KEY].pop()
            obj_1 = fragment[btime.FRAGMENT_WORKSPACE_STACK_KEY].pop()
        except stack.StackError:
            fragment[btime.FRAGMENT_ERROR_KEY] = 2
            return

        try:
            # run operation
            results = int(obj_1 == obj_2)
        except Exception:
            fragment[btime.FRAGMENT_ERROR_KEY] = 1
            return

        fragment[btime.FRAGMENT_WORKSPACE_STACK_KEY].push(results)
