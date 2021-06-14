"""
Copyright 2021 Charles McMarrow

This script translates "loads" a program into Rooms "memory".
It verifies that the data that it loads into Rooms is valid.
It lets data to be translated VIA file or str.
"""

# built-in
import io
import os
import string
from collections import deque
from typing import Iterator, Optional, Tuple, Dict, List

# backrooms
from .backrooms_error import BackroomsError
from .rooms import Rooms

INCLUDE_FILE_EXTENSION = ".brs"


class TranslatorError(BackroomsError):
    @classmethod
    def missing_include(cls,
                        include: str) -> 'TranslatorError':
        """
        info: Used to indicate a missing include.
        :param include: str
        :return: TranslatorError
        """
        return cls(f"{repr(include)} is a missing include!")

    @classmethod
    def name_collision(cls, name: str):
        return cls(f"Name collision with {name}!")

    @classmethod
    def bad_line(cls,
                 line: str,
                 line_number: int,
                 handler_name: str,
                 error: str = "") -> 'TranslatorError':
        """
        info: Used to indicate line is not valid.
        :param line: str
        :param line_number: int
        :param handler_name: str
        :param error: str
        :return: TranslatorError
        """
        if not error:
            return cls(f"Bad line at {handler_name}:{line_number}: {repr(line)}!")
        return cls(f"Bad line at {handler_name}:{line_number}:{str(error)}: {repr(line)}!")


class Handler:
    def __init__(self,
                 name: str):
        """
        info: Gives data line by line.
        :param name: str
        """
        self._name: str = name
        self._is_open = True

    def get_name(self) -> str:
        """
        info: Gets the name of the Handler.
        :return: str
        """
        return self._name

    def is_open(self) -> bool:
        """
        info: Checks if file handler is still open.
        :return: bool
        """
        return self._is_open

    def close(self) -> None:
        """
        info: Closes the handler.
        :return: None
        """
        self._is_open = False

    def __del__(self):
        self.close()
    
    def __iter__(self) -> 'Handler':
        return self
    
    def __next__(self) -> str:
        raise NotImplementedError()


class FileHandler(Handler):
    def __init__(self,
                 path: str):
        """
        info: Handler for Files.
        :param path: str
        """
        self._path: str = path
        self._file_iter: Optional[Iterator[str]] = None
        self._file_handler: Optional[io.TextIOWrapper] = None
        file_name = os.path.basename(path)
        if file_name.endswith(INCLUDE_FILE_EXTENSION):
            file_name = file_name[:-len(INCLUDE_FILE_EXTENSION)]
        super(FileHandler, self).__init__(file_name)

    def close(self):
        if self.is_open() and self._file_handler is not None:
            self._file_handler.close()
        super(FileHandler, self).close()

    def __next__(self) -> str:
        if self._file_iter is None:
            self._file_handler = open(self._path)
            self._file_iter = iter(self._file_handler)
        return next(self._file_iter).rstrip("\n")


class StringHandler(Handler):
    def __init__(self,
                 name: str,
                 data: str):
        """
        info: Handler for Strings
        :param name: str
        :param data: str
        """
        self._parts: Iterator[str] = iter(data.split("\n"))
        super(StringHandler, self).__init__(name)

    def __next__(self) -> str:
        return next(self._parts)
        

class Handlers:
    def __init__(self,
                 main: Handler,
                 name_spaces: Tuple[Tuple[Handler, ...], ...] = ()):
        """
        info: Holder all the Handles need it for a program.
            Builds the name_spaces so includes can be prioritized.
            Makes sure a handler is not included more than once.
        :param main: Handler
        :param name_spaces: Tuple[Tuple[Handler]])
        """
        self._handlers: deque[Handler] = deque((main,))
        self._name_spaces: Optional[Tuple[Dict[str, Handler]]] = None

        name_spaces_dicts = []
        for name_space in name_spaces:
            name_space_dict = {}
            for handler in name_space:
                if handler.get_name() in name_space_dict:
                    raise TranslatorError.name_collision(handler.get_name())
                name_space_dict[handler.get_name()] = handler
            name_spaces_dicts.append(name_space_dict)
        self._name_spaces: Tuple[Dict[str, Handler]] = tuple(name_spaces_dicts)

        self._line_number: int = -1
        self._used_names = {main.get_name()}
    
    def __iter__(self) -> 'Handlers':
        return self
    
    def __next__(self) -> str:
        while self._handlers:
            try:
                self._line_number += 1
                return next(self._handlers[0])
            except StopIteration:
                if self._line_number == -1:
                    # return a single bank line from the handler with no data
                    self._line_number = 0
                    return ""
                self._handlers.popleft()
                self._line_number = -1
        raise StopIteration()

    def __bool__(self):
        return bool(self._handlers)

    def get_name(self) -> Optional[str]:
        """
        info: Gets the current name.
        :return: Optional[str]
        """
        if self._handlers:
            return self._handlers[0].get_name()

    def get_line_number(self) -> Optional[int]:
        """
        info: Gets the current line.
        :return: Optional[int]
        """
        if self._line_number >= 0:
            return self._line_number

    def include(self,
                name: str) -> None:
        """
        info: Includes name if it has not been included all ready.
        :param name: str
        :exception TranslatorError
            raises TranslatorError is include cant be found.
        :return: None
        """
        # check that name has not be included yet
        if name not in self._used_names:
            for name_space in self._name_spaces:
                if name in name_space:
                    self._used_names.add(name)
                    self._handlers.append(name_space[name])
                    return
            # could not find the include handler
            raise TranslatorError.missing_include(name)


def _tokenize_line(line: str) -> List[str]:
    """
    info: Tokenize line.
    :param line: str
    :return: List[str]
    """
    tokens = [""]
    for character in line:
        # split and remove white space
        if character in string.whitespace:
            if tokens[-1]:
                tokens.append("")
        # split and add "@" which acts as None
        elif character == "@":
            if not tokens[-1]:
                tokens[-1] += "@"
            else:
                tokens.append("@")
            tokens.append("")
        else:
            tokens[-1] += character
    if not tokens[-1]:
        del tokens[-1]
    return tokens


def _read_number(tokens: List[str],
                 full_line: str,
                 line_number: int,
                 handler_name: str) -> int:
    """
    info: Checks and pops an int from tokens.
    :param tokens: List[str]
    :param full_line: str
    :param line_number: int
    :param handler_name: str
    :exception TranslatorError
            raises TranslatorError no tokens was given.
    :exception ValueError
            raises ValueError if int() fails.
    :return: int
    """
    if tokens:
        return int(tokens.pop(0))
    raise TranslatorError.bad_line(full_line, line_number, handler_name)


def _read_single_number(line: str,
                        full_line: str,
                        line_number: int,
                        handler_name: str) -> int:
    """
    info: Checks that line holds only a single int.
    :param line: str
    :param full_line: str
    :param line_number: int
    :param handler_name: str
    :exception TranslatorError
            raises TranslatorError if line makes more or less than one token.
    :exception ValueError
            raises ValueError if int() fails.
    :return: int
    """
    tokens = _tokenize_line(line)
    if len(tokens) == 1:
        return int(tokens[0])
    raise TranslatorError.bad_line(full_line, line_number, handler_name)


def translator(handlers: Handlers) -> Rooms:
    """
    info: Load program into Rooms "memory"
    :param handlers: Handlers
    :exception TranslatorError
            raises TranslatorError if handlers give an invalid line.
    :return: Rooms
    """
    rooms = Rooms()
    x, y, floor = 0, 0, -1
    for line in handlers:
        full_line = line
        # throw away lead white space
        while line:
            if line[0] not in string.whitespace:
                break
            line = line[1:]
        try:
            # enter new handler
            if handlers.get_line_number() == 0:
                # reset x and y to zero
                x = 0
                y = 0
                # go up a floor
                floor += 1
                # set the floor name to the handlers name
                rooms.set_floor_name(floor, handlers.get_name())

            # row
            if line.startswith("/"):
                # write row into rooms
                rooms.write_line(x, y, floor, line[1:], 1, 0, 0)
                # go down a row
                y += -1
            # comment
            elif line.startswith("#"):
                # just throw away the comment
                pass
            # hallway
            elif line.startswith("~"):
                tokens = _tokenize_line(line[1:])
                hallway_name = None
                # check if hallway has a name
                if tokens:
                    if tokens[0] == "@":
                        del tokens[0]
                    else:
                        hallway_name = tokens.pop(0)
                    # check that we are out of tokens
                    if tokens:
                        raise TranslatorError.bad_line(full_line, handlers.get_line_number(), handlers.get_name())
                rooms.set_hallway_name(y, floor, hallway_name)
            # new floor
            elif line.startswith("+"):
                tokens = _tokenize_line(line[1:])
                floor_name = None
                # check if floor has a name
                if tokens:
                    if tokens[0] == "@":
                        del tokens[0]
                    else:
                        floor_name = tokens.pop(0)
                    # check that we are out of tokens
                    if tokens:
                        raise TranslatorError.bad_line(full_line, handlers.get_line_number(), handlers.get_name())
                floor += 1
                y = 0
                rooms.set_floor_name(floor, floor_name)
            # include
            elif line.startswith("%"):
                tokens = _tokenize_line(line[1:])
                # check that we have include name
                if tokens:
                    handlers.include(tokens.pop(0))
                    # check that we are out of tokens
                    if tokens:
                        raise TranslatorError.bad_line(full_line, handlers.get_line_number(), handlers.get_name())
                else:
                    raise TranslatorError.bad_line(full_line, handlers.get_line_number(), handlers.get_name())
            # parallel
            elif line.startswith("="):
                tokens = _tokenize_line(line[1:])

                from_name = None
                to_name = None
                from_spot = None
                to_spot = None

                if tokens:
                    if tokens[0] != "@":
                        from_name = tokens.pop(0)
                    else:
                        tokens.pop(0)
                    if tokens:
                        if tokens[0] != "@":
                            to_name = tokens.pop(0)
                        else:
                            tokens.pop(0)
                        if tokens:
                            if tokens[0] != "@":
                                from_spot = int(tokens.pop(0))
                            else:
                                tokens.pop(0)
                            if tokens:
                                if tokens[0] != "@":
                                    to_spot = int(tokens.pop(0))
                                else:
                                    tokens.pop(0)
                                if tokens:
                                    raise TranslatorError.bad_line(full_line,
                                                                   handlers.get_line_number(),
                                                                   handlers.get_name())

                if from_name is not None and from_spot is not None:
                    raise TranslatorError.bad_line(full_line,
                                                   handlers.get_line_number(),
                                                   handlers.get_name(),
                                                   "Cant provided both 'from_name' and 'from_location'!")

                if from_name is not None:
                    # duplicate from name
                    from_spot = rooms.get_floor_level(from_name)
                elif from_spot is None:
                    from_spot = floor

                if to_spot is None:
                    # duplicate onto the floor above
                    to_spot = floor + 1
                    floor += 1

                # duplicate floor
                rooms.duplicate_floor(from_spot, to_spot)
                # set floor name
                rooms.set_floor_name(to_spot, to_name)
            # shift x
            elif line.startswith("XS"):
                x += _read_single_number(line[2:], full_line, handlers.get_line_number(), handlers.get_name())
            # x
            elif line.startswith("X"):
                x = _read_single_number(line[1:], full_line, handlers.get_line_number(), handlers.get_name())
            # shift y
            elif line.startswith("YS"):
                y += _read_single_number(line[2:], full_line, handlers.get_line_number(), handlers.get_name())
            # y
            elif line.startswith("Y"):
                y = _read_single_number(line[1:], full_line, handlers.get_line_number(), handlers.get_name())
            # floor shift
            elif line.startswith("FS"):
                floor += _read_single_number(line[2:], full_line, handlers.get_line_number(), handlers.get_name())
            # floor
            elif line.startswith("F"):
                floor = _read_single_number(line[1:], full_line, handlers.get_line_number(), handlers.get_name())
            # blank line
            elif not line:
                # just throw away the blank line
                pass
            # unknown line
            else:
                raise TranslatorError.bad_line(full_line, handlers.get_line_number(), handlers.get_name())
        except TranslatorError as e:
            raise e
        except Exception as e:
            raise TranslatorError.bad_line(full_line, handlers.get_line_number(), handlers.get_name(), str(e))
    return rooms
