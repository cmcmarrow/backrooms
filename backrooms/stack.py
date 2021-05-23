
class StackError(Exception):
    @classmethod
    def stack_empty(cls) -> "StackError":
        return cls("Stack is Empty!")


class StackBottom:
    pass


class StackFrame:
    pass


class Stack:
    def __init__(self):
        self._stack = [StackBottom]

    def pop(self) -> any:
        if self.peak() is StackBottom:
            raise StackError.stack_empty()
        return self._stack.pop()

    def push(self,
             item: any) -> None:
        self._stack.append(item)

    def peak(self) -> any:
        return self._stack[-1]

    def add_frame(self) -> None:
        self.push(StackFrame)

    def pop_frame(self) -> None:
        while self.pop() is not StackFrame:
            pass
