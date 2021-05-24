from .btime import Rule, Fragment, BTime
from . import btime
from . import stack


def get_built_in_rules() -> tuple:
    return (Echo(),
            EchoN(),
            BType(),
            Halt())


class Echo(Rule):
    def __init__(self,
                 identifier: str = "e"):
        super(Echo, self).__init__(identifier=identifier)

    def __call__(self, fragment: Fragment, b_time: BTime):
        obj = fragment[btime.FRAGMENT_WORKSPACE_STACK_KEY].peak()
        if not isinstance(obj, (stack.StackFrame, stack.StackBottom)):
            pass
        elif isinstance(obj, stack.StackFrame):
            fragment[btime.FRAGMENT_ERROR] = 1
        else:
            fragment[btime.FRAGMENT_ERROR] = 2
        print(obj, end="")
        fragment.step()


class EchoN(Rule):
    def __init__(self,
                 identifier: str = "n"):
        super(EchoN, self).__init__(identifier=identifier)

    def __call__(self, fragment: Fragment, b_time: BTime):
        obj = fragment[btime.FRAGMENT_WORKSPACE_STACK_KEY].peak()
        if not isinstance(obj, (stack.StackFrame, stack.StackBottom)):
            pass
        elif isinstance(obj, stack.StackFrame):
            fragment[btime.FRAGMENT_ERROR] = 1
        else:
            fragment[btime.FRAGMENT_ERROR] = 2
        print(obj)
        fragment.step()


class BType(Rule):
    def __init__(self,
                 identifier: str = "t"):
        super(BType, self).__init__(identifier=identifier)

    def __call__(self, fragment: Fragment, b_time: BTime):
        fragment.step()
        btype = fragment.read()
        if btype in "sn":
            if btype == "n":
                # TODO write
                fragment.step()
            else:
                # TODO add /n /t
                fragment.step()
                exit_char = fragment.read()
                fragment.step()
                data = ""
                while True:
                    c = fragment.read()
                    if exit_char == c:
                        break
                    data += c
                    fragment.step()
                fragment[btime.FRAGMENT_WORKSPACE_STACK_KEY].push(data)
            fragment.step()
        else:
            fragment[btime.FRAGMENT_ERROR] = 1


class Halt(Rule):
    def __init__(self,
                 identifier: str = "h"):
        super(Halt, self).__init__(identifier=identifier)

    def __call__(self, fragment: Fragment, b_time: BTime):
        fragment.step()
        c = fragment.read()
        if c == "a":
            fragment.step()
            c = fragment.read()
            if c == "*":
                fragment.step()
                fragment[btime.FRAGMENT_HALT_KEY] = True
