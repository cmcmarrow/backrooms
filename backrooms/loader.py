"""
Copyright 2021 Charles McMarrow
"""


from .backrooms import BackroomsD, BackRoomsCordD, Backrooms, BackRoomsCord, Hallway
from .name import is_name
from string import whitespace
from typing import List, Optional


ASM_EXTENSION = ".brs"


class LoaderError(Exception):
    @classmethod
    def loader_not_found(cls, name):
        return cls(f"Loader not found: '{name}'!")

    @classmethod
    def bad_line(cls, line: str, loader_name: str, line_number: int):
        return cls(f"{loader_name},{line_number}: {repr(line)}")


class Loader:
    def __init__(self, name: str):
        self._name = name

    def __next__(self):
        raise NotImplementedError()

    def __iter__(self):
        return self

    @property
    def name(self) -> str:
        return self._name


class StrLoader(Loader):
    def __init__(self, name: str, brs_str: str):
        super(StrLoader, self).__init__(name=name)
        self._lines = iter(brs_str.splitlines())

    def __next__(self):
        return next(self._lines)


class FileLoader(Loader):
    def __init__(self, name: str, brs_file: str):
        super(FileLoader, self).__init__(name=name)
        self._brs_file = brs_file
        self._read_lines_iter = self._read_lines(brs_file)

    def __next__(self):
        return next(self._read_lines_iter)

    @staticmethod
    def _read_lines(brs_file):
        with open(brs_file) as file:
            for line in file:
                yield line.rstrip("\n")


# TODO this could be cleaned up
class LoaderIterator:
    def __init__(self,
                 name: str,
                 priority_order_loaders: List[List[Loader]]):

        # makes priority order loader into Tuple[Dict[str, Loader]]
        self._priority_order_loaders = tuple([{loader.name: loader for loader in p} for p in priority_order_loaders])

        self._name = None
        self._new_loader = False

        self._used_names = set()
        self._loader_queue = []

        self.include(name)

    def __next__(self) -> str:
        if self._name is not None:
            self._new_loader = False
        else:
            self._new_loader = True
        # check if at least a single loader is in the queue
        if self._loader_queue:
            self._name = self._loader_queue[0].name
            try:
                # get next line
                return next(self._loader_queue[0])
            except StopIteration:
                # remove empty loader
                del self._loader_queue[0]
                while self._loader_queue:
                    self._name = self._loader_queue[0].name
                    try:
                        # get next line
                        next_line = next(self._loader_queue[0])
                        # new loader is being used
                        self._new_loader = True
                        return next_line
                    except StopIteration:
                        pass
                    # remove empty loader
                    del self._loader_queue[0]
        raise StopIteration()

    def __iter__(self):
        return self

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def new_loader(self) -> bool:
        return self._new_loader

    def include(self, name: str):
        if name in self._used_names:
            return
        self._used_names.add(name)
        for loaders in self._priority_order_loaders:
            if name in loaders:
                self._loader_queue.append(loaders[name])
                return
        raise LoaderError.loader_not_found(name)


def remove_whitespace(line: str) -> str:
    while line and line[0] in whitespace:
        line = line[1:]
    return line


def is_none(line: str) -> bool:
    if line:
        return line[0] == "|"
    return False


def get_none() -> str:
    return "|"


def get_word(line):
    word = ""
    for c in line:
        if not is_name(word + c):
            break
        word += c
    return word


def is_word(line: str) -> bool:
    return is_name(get_word(line))


def is_int(line: str) -> bool:
    return isinstance(get_int(line), int)


def get_int(line: str) -> Optional[int]:
    number = None
    number_str = ""
    for c in line:
        try:
            number_str += c
            number = int(number_str)
        except ValueError:
            if number is not None:
                return number
    return number


def get_cord(line: str, full_line: str, loader_name: str, line_number: int) -> int:
    line = remove_whitespace(line)
    if not is_int(line):
        raise LoaderError.bad_line(full_line, loader_name, line_number)

    number = get_int(line)
    line = line[len(str(number)):]

    line = remove_whitespace(line)
    if line:
        raise LoaderError.bad_line(full_line, loader_name, line_number)
    return number


def build(loader_iterator: LoaderIterator):
    at = BackRoomsCordD(0, 0, -1)
    backrooms_d = BackroomsD()
    line_number = 1
    loader_name = ""
    for line in loader_iterator:
        full_line = line
        if loader_iterator.new_loader:
            line_number = 1
            loader_name = loader_iterator.name
            at = at.shift(0, 0, 1)
            at = BackRoomsCordD(0, 0, at.z)
            backrooms_d.add_backrooms(at.z, Backrooms(loader_iterator.name))
        # row
        if line.startswith("/"):
            backrooms_d.write_line(at, BackRoomsCordD(1, 0, 0), line[1:])
            at = at.shift(0, -1, 0)
        # comment just throw away the line
        elif line.startswith("#"):
            pass
        # hallway
        elif line.startswith("~"):
            line = remove_whitespace(line[1:])
            if is_word(line):
                hallway = get_word(line)
                line = line[len(hallway):]
            elif is_none(line):
                hallway = None
                line = line[len(get_none()):]
            else:
                raise LoaderError.bad_line(full_line, loader_name, line_number)
            line = remove_whitespace(line)
            if line:
                raise LoaderError.bad_line(full_line, loader_name, line_number)
            backrooms_d.add_hallway(at.z, Hallway(hallway, BackRoomsCord(y=at.y)))
        elif line.startswith("%"):
            # TODO clean up import errors
            line = remove_whitespace(line[1:])
            if is_word(line):
                include = get_word(line)
                line = line[len(include):]
                line = remove_whitespace(line)
                if line:
                    raise LoaderError.bad_line(full_line, loader_name, line_number)
                loader_iterator.include(include)
            else:
                raise LoaderError.bad_line(full_line, loader_name, line_number)
        # backrooms
        elif line.startswith("+"):
            line = remove_whitespace(line[1:])
            if is_word(line):
                backrooms = get_word(line)
                line = line[len(backrooms):]
            elif is_none(line):
                backrooms = None
                line = line[len(get_none()):]
            else:
                raise LoaderError.bad_line(full_line, loader_name, line_number)
            line = remove_whitespace(line)
            if line:
                raise LoaderError.bad_line(full_line, loader_name, line_number)
            at = at.shift(0, 0, 1)
            at = BackRoomsCordD(0, 0, at.z)
            backrooms_d.add_backrooms(at.z, Backrooms(backrooms))
        # parallel
        elif line.startswith("="):
            line = remove_whitespace(line[1:])
            if is_word(line):
                p_from = get_word(line)
                line = line[len(p_from):]
            elif is_none(line):
                p_from = None
                line = line[len(get_none()):]
            else:
                raise LoaderError.bad_line(full_line, loader_name, line_number)
            line = remove_whitespace(line)
            if is_word(line):
                p_to = get_word(line)
                line = line[len(p_to):]
            elif is_none(line):
                p_to = None
                line = line[len(get_none()):]
            else:
                raise LoaderError.bad_line(full_line, loader_name, line_number)
            line = remove_whitespace(line)
            if line:
                raise LoaderError.bad_line(full_line, loader_name, line_number)

            if p_from is None:
                p_from = backrooms_d.get_backrooms(at.z)
            at = at.shift(0, 0, 1)
            backrooms_d.add_backrooms(at.z, p_from.parallel(p_to))
        # x shift
        elif line.startswith("XS"):
            line = line[2:]
            at = at.shift(get_cord(line, full_line, loader_name, line_number), at.y, at.z)
        # y shift
        elif line.startswith("YS"):
            line = line[2:]
            at = at.shift(at.x, get_cord(line, full_line, loader_name, line_number), at.z)
            # z shift
        elif line.startswith("ZS"):
            line = line[2:]
            at = at.shift(at.x, at.y, get_cord(line, full_line, loader_name, line_number))
        # x
        elif line.startswith("X"):
            line = line[1:]
            at = BackRoomsCordD(get_cord(line, full_line, loader_name, line_number), at.y, at.z)
        # y
        elif line.startswith("Y"):
            line = line[1:]
            at = BackRoomsCordD(at.x, get_cord(line, full_line, loader_name, line_number), at.z)
        # z
        elif line.startswith("Z"):
            line = line[1:]
            at = BackRoomsCordD(at.x, at.y, get_cord(line, full_line, loader_name, line_number))
        # blank just throw away the line
        elif not line:
            pass
        else:
            # loader does not know what to do with this line
            raise LoaderError.bad_line(full_line, loader_name, line_number)
        line_number += 1
    return backrooms_d
