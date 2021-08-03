"""
Copyright 2021 Charles McMarrow

This script is the core of backrooms.
It holds the backrooms memory structure and everything need it for it to operate.
"""

# built-in
from functools import lru_cache
from string import ascii_letters, digits
from typing import Optional, Dict, Tuple, List, Set, Union

# backrooms
from .backrooms_error import BackroomsError
from . import whisper


CHARACTER_SET = set([chr(character) for character in range(256)])
NAME_SET = set(ascii_letters + digits + "_")


class RoomsError(BackroomsError):
    @classmethod
    def bad_name(cls, bad_name: str) -> 'RoomsError':
        """
        info: Used to indicate a bad name was given.
        :param bad_name: str
        :return: RoomsError
        """
        return cls(f"{repr(bad_name)} is not a name!")

    @classmethod
    def bad_character(cls, bad_character: str) -> 'RoomsError':
        """
        info: Used to indicate a bad character was given.
        :param bad_character:
        :return: RoomsError
        """
        return cls(f"{repr(bad_character)} is not a character!")


def is_character(character: str) -> bool:
    """
    info: Checks if a character is valid.
    :param character: str
    :return: bool
    """
    return character in CHARACTER_SET


@lru_cache(2048)
def is_name(name: str) -> bool:
    """
    info: Checks if a name is valid.
    :param name: str
    :return: bool
    """
    for character in name:
        if character not in NAME_SET:
            return False
    return bool(name)


def _find_a_hallway_key(key: int) -> Union[int, float]:
    """
    info: Makes sorted works out from 0. EX: 0, 1, -1, 2, -2, 3, ...
    :param key: str
    :return: Union[int, float]
    """
    if key < 0:
        return abs(key) - 0.5
    return key


class Rooms:
    def __init__(self):
        """
        info: 3D memory structure that stores a single ASCII letter in a cell.
        """
        self._floors: Dict[int: Dict[Tuple[int, int]], str] = {}
        self._floor_levels_to_names: Dict[int, str] = {}
        self._floors_names_to_levels: Dict[str, int] = {}

        self._hallways: Dict[int, List[int]] = {}
        self._hallways_set: Dict[int: Set[int]] = {}
        self._hallway_locations_to_names: Dict[int, Dict[int, str]] = {}
        self._hallway_names_to_locations: Dict[int, Dict[str, int]] = {}

    def read(self,
             x: int,
             y: int,
             floor_level: int) -> str:
        """
        info: Reads a memory cell.
        :param x: int
        :param y: int
        :param floor_level: int
        :return: str
        """
        return self._floors.get(floor_level, {}).setdefault((x, y), " ")

    def write(self,
              x: int,
              y: int,
              floor_level: int,
              character: str) -> None:
        """
        info: _Write a character to a memory cell.
        :param x: int
        :param y: int
        :param floor_level: int
        :param character: str
        :exception RoomsError
            raises RoomsError if a bad character is given.
        :return: None
        """

        if not is_character(character):
            if whisper.WHISPER_RUNNING:
                whisper.critical(f"{repr(character)} was attempted to be written at {(x, y, floor_level)}!")
            raise RoomsError.bad_character(character)

        if character == " ":
            # " " is the default character save space by removing the cell all together
            if (x, y) in self._floors.setdefault(floor_level, {}):
                del self._floors[floor_level][(x, y)]
        else:
            self._floors.setdefault(floor_level, {})[(x, y)] = character

    def write_line(self,
                   x: int,
                   y: int,
                   floor_level: int,
                   characters: str,
                   vector_x: int = 0,
                   vector_y: int = 0,
                   vector_floor_level: int = 0) -> None:
        """
        info: Writes a characters to memory cells.
            The vector variables get added to the coordinates per character.
        :param x: int
        :param y: int
        :param floor_level: int
        :param characters: str
        :param vector_x: int
        :param vector_y: int
        :param vector_floor_level: int
        :exception RoomsError
            raises RoomsError if a bad character is given.
        :return: None
        """
        for character in characters:
            self.write(x, y, floor_level, character)
            x += vector_x
            y += vector_y
            floor_level += vector_floor_level

    def set_floor_name(self,
                       floor_level: int,
                       floor_name: Optional[str] = None) -> None:
        """
        info: Sets a floor name.
        :param floor_level: int
        :param floor_name: Optional[str]
            If the floor name all ready is use it will just be over writen.
            If the floor name is None then that floor name  will be removed.
        :exception RoomsError
            raises RoomsError if a bad name is given.
        :return: None
        """
        if floor_name is None:
            if floor_level in self._floor_levels_to_names:
                # remove floor name
                del self._floors_names_to_levels[self._floor_levels_to_names[floor_level]]
                del self._floor_levels_to_names[floor_level]
        elif is_name(floor_name):
            # check if name is in use
            if floor_name in self._floors_names_to_levels:
                # remove floor name before overwriting it
                self.set_floor_name(self._floors_names_to_levels[floor_name])
            # add floor name
            self._floor_levels_to_names[floor_level] = floor_name
            self._floors_names_to_levels[floor_name] = floor_level
        else:
            # bad name
            if whisper.WHISPER_RUNNING:
                whisper.error(f"{repr(floor_name)} bad floor name attempted to be written at {floor_level}!")
            raise RoomsError.bad_name(floor_name)

    def get_floor_name(self,
                       floor_level: int) -> Optional[str]:
        """
        info: Gets a floor name if it has one.
        :param floor_level: int
        :return: Optional[str]
        """
        return self._floor_levels_to_names.get(floor_level)

    def get_floor_level(self,
                        floor_name: str) -> Optional[int]:
        """
        info: Gets floor level if floor name is used.
        :param floor_name: str
        :return: Optional[str]
        """
        return self._floors_names_to_levels.get(floor_name)

    def set_hallway_name(self,
                         y: int,
                         floor_level: int,
                         hallway_name: Optional[str] = None) -> None:
        """
        info: Makes a hallway and gives it a name.
        :param y: int
        :param floor_level: int
        :param hallway_name: Optional[str]
        :return: None
        """
        # add hallway
        if hallway_name is None or is_name(hallway_name):
            if hallway_name is not None:
                old_hallway_y = self.get_hallway_location(floor_level, hallway_name)
                # remove hallway that shares same name
                if old_hallway_y is not None:
                    self.remove_hallway(old_hallway_y, floor_level)
            # find location in hallway list to add new hallway
            hallway_block_in_at = self._find_hallway_at(y, floor_level)
            if hallway_block_in_at is None:
                hallway_block_in_at = -1
            # update hallway structures
            self._hallways.setdefault(floor_level, []).insert(hallway_block_in_at + 1, y)
            self._hallways_set.setdefault(floor_level, set()).add(y)
            if hallway_name is not None:
                self._hallway_locations_to_names.setdefault(floor_level, {})[y] = hallway_name
                self._hallway_names_to_locations.setdefault(floor_level, {})[hallway_name] = y
            # remove old hallway name if replaced by a None hallway
            elif y in self._hallway_locations_to_names.setdefault(floor_level, {}):
                old_hallway_name = self._hallway_locations_to_names[floor_level][y]
                del self._hallway_locations_to_names[floor_level][y]
                del self._hallway_names_to_locations[floor_level][old_hallway_name]
        else:
            # bad name
            if whisper.WHISPER_RUNNING:
                whisper.error(f"{repr(hallway_name)} bad hallway name attempted to be written at {(y, floor_level)}!")
            raise RoomsError.bad_name(hallway_name)

    def remove_hallway(self,
                       y: int,
                       floor_level: int) -> None:
        """
        info: Removes a hallway if it exists.
        :param y: int
        :param floor_level: int
        :return: None
        """
        # remove hallway
        if y in self._hallways_set.setdefault(floor_level, set()):
            # find hallway location
            hallway_block_at = self._find_hallway_at(y, floor_level)
            # update hallway structures
            del self._hallways[floor_level][hallway_block_at]
            self._hallways_set[floor_level].remove(y)
            hallway_name = self._hallway_locations_to_names[floor_level].get(y)
            if hallway_name is not None:
                del self._hallway_locations_to_names[floor_level][y]
                del self._hallway_names_to_locations[floor_level][hallway_name]

    def get_hallway_name(self,
                         y: int,
                         floor_level: int) -> Optional[str]:
        """
        info: Get hallway name from location..
        :param y: int
        :param floor_level: int
        :return: Optional[str]
        """
        return self._hallway_locations_to_names.setdefault(floor_level, {}).get(y)

    def get_hallway_location(self,
                             floor_level: int,
                             hallway_name: str) -> Optional[int]:
        """
        info: Get hallway location from coordinates.
        :param floor_level: int
        :param hallway_name: str
        :return: Optional[int]
        """
        return self._hallway_names_to_locations.setdefault(floor_level, {}).get(hallway_name)

    def get_next_hallway_location(self,
                                  hallway_location: int,
                                  floor_level: int) -> Optional[int]:
        """
        info: Get coordinates to next hallway.
        :param hallway_location: int
        :param floor_level: int
        :return: Optional[str]
        """
        hallway_at = self._find_hallway_at(hallway_location, floor_level)
        # check that hallway exists
        if hallway_at is not None:
            hallway_at -= 1
            # check that next hallway exists
            if hallway_at != -1:
                return self._hallways[floor_level][hallway_at]

    def get_past_hallway_location(self,
                                  hallway_location: int,
                                  floor_level: int) -> Optional[int]:
        """
        info: Get coordinates to past hallway.
        :param hallway_location: int
        :param floor_level: int
        :return: Optional[str]
        """
        hallway_at = self._find_hallway_at(hallway_location, floor_level)
        # check that hallway exists
        if hallway_at is not None:
            hallway_at += 1
            # check that past hallway exists
            if hallway_at != len(self._hallways[floor_level]):
                return self._hallways[floor_level][hallway_at]

    def find_hallway_location(self,
                              y: int,
                              floor_level: int) -> Optional[int]:
        """
        info: Find what hallway y is in.
        :param y: int
        :param floor_level: int
        :return: Optional[int]
        """
        hallway_at = self._find_hallway_at(y, floor_level)
        if hallway_at is not None:
            return self._hallways[floor_level][hallway_at]

    def _find_hallway_at(self,
                         y: int,
                         floor_level: int) -> Optional[int]:
        """
        info: Finds what hallway the coordinates are in.
        :param y: int
        :param floor_level: int
        :return: Optional[int]
        """
        hallways = self._hallways.setdefault(floor_level, [])

        # check that hallways is not empty
        if not hallways:
            return

        # check that coordinates is not in front of all hallways
        if y > hallways[0]:
            return

        # check that coordinates is not in the last hallway
        if hallways[-1] >= y:
            return len(hallways) - 1

        block_start = 0
        block_end = len(hallways) - 1

        # Big-O(log n)
        # find last hallway that greater than equal to y
        while True:
            # find the middle of block
            at = block_start + (block_end - block_start)//2
            hallway_location = hallways[at]
            # hallway is behind coordinates
            if hallway_location < y:
                # remove back half of block
                block_end = at
            # hallway is in font of coordinates
            elif hallway_location > y:
                # last hallway is not in front of coordinates
                if y > hallways[at + 1]:
                    return at
                # remove first half of block
                block_start = at
            # coordinates is a hallway coordinates
            else:
                return at

    def remove_floor(self,
                     floor_level: int) -> None:
        """
        info: Removes the specified floor and everything associated with it.
        :param floor_level: int
        :return: None
        """
        floor_name = self.get_floor_name(floor_level)
        # remove floor data
        if floor_name is not None:
            del self._floors_names_to_levels[floor_name]

        if floor_level in self._floor_levels_to_names:
            del self._floor_levels_to_names[floor_level]

        if floor_level in self._floors:
            del self._floors[floor_level]

        # remove hallway data
        if floor_level in self._hallways:
            del self._hallways[floor_level]

        if floor_level in self._hallway_names_to_locations:
            del self._hallway_names_to_locations[floor_level]

        if floor_level in self._hallway_locations_to_names:
            del self._hallway_locations_to_names[floor_level]

    def duplicate_floor(self,
                        floor_level_from: int,
                        floor_level_to: int) -> None:
        """
        info: Copies floor onto another floor and everything associated with it.
        :param floor_level_from: int
        :param floor_level_to: int
        :return: None
        """
        # make sure "to" floor is fully removed
        self.remove_floor(floor_level_to)

        # duplicate floor data
        if floor_level_from in self._floors:
            self._floors[floor_level_to] = self._floors[floor_level_from].copy()

        # duplicate hallway data
        if floor_level_from in self._hallways:
            self._hallways[floor_level_to] = self._hallways[floor_level_from].copy()

        if floor_level_from in self._hallway_names_to_locations:
            self._hallway_names_to_locations[floor_level_to] = self._hallway_names_to_locations[floor_level_from].copy()

        if floor_level_from in self._hallway_locations_to_names:
            self._hallway_locations_to_names[floor_level_to] = self._hallway_locations_to_names[floor_level_from].copy()

    def find_a_hallway(self,
                       hallway_name: str) -> Optional[Tuple[int, int]]:
        """
        info: Finds a hallway with that name.
            Works out from 0. EX: 0, 1, -1, 2, -2, 3, ...
        :param hallway_name: str
        :return: Optional[Tuple[int, int]]
        """
        for floor in sorted(self._hallway_names_to_locations, key=_find_a_hallway_key):
            if hallway_name in self._hallway_names_to_locations[floor]:
                return self._hallway_names_to_locations[floor][hallway_name], floor
