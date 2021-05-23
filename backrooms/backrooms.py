"""
Copyright 2021 Charles McMarrow

BackroomsD "Backrooms Dimensions" serves as memory for the virtual machine "VM".
BackroomsD is an uncommon memory structure.
Key Differences
*   A single Unicode character makes up a memory cell.
*   An address is made up from 3 parts.
    *   x: int
    *   y: int
    *   z: int

Other than for some flags when a program is loaded into the VM must of the data will be loaded into Backrooms objects.
The backrooms_d should be immortal and cannot get corrupted during run-time.
You cannot hurt the backrooms_d but it sure can hurt you.
Because of this all objects in this file verify that that data given is
valid on initialization and on most class methods.
"""


from typing import Optional, Dict, List, Tuple
from .name import is_name


class BackRoomsError(Exception):
    @classmethod
    def bad_backroom_name(cls, name: object) -> "BackRoomsError":
        return cls(f"Not a valid Backrooms name: `{name}`!")

    @classmethod
    def bad_hallway_name(cls, name: object) -> "BackRoomsError":
        return cls(f"Not a valid Hallway name: `{name}`!")

    @classmethod
    def bad_backrooms_cord(cls, cord: object) -> "BackRoomsError":
        return cls(f"Not a valid Backrooms cord: `{cord}`!")

    @classmethod
    def bad_hallway_cord(cls, cord: object) -> "BackRoomsError":
        return cls(f"Not a valid Hallway cord: `{cord}`!")

    @classmethod
    def bad_raw_backrooms(cls, raw_backrooms: object) -> "BackRoomsError":
        return cls(f"Not a valid raw Backrooms: `{raw_backrooms}`!")

    @classmethod
    def bad_backrooms_entity(cls, entity: object) -> "BackRoomsError":
        return cls(f"Not a valid Backrooms cord: `{entity}`!")

    @classmethod
    def bad_hallways(cls, hallways: object) -> "BackRoomsError":
        return cls(f"Not a valid hallways: `{hallways}`!")

    @classmethod
    def bad_hallway(cls, hallway: object) -> "BackRoomsError":
        return cls(f"Not a valid Hallway: `{hallway}`!")

    @classmethod
    def unidentified_hallway(cls, hallway: object) -> "BackRoomsError":
        return cls(f"Hallway cant be identified: `{hallway}`!")

    @classmethod
    def bad_backrooms(cls, backrooms: object):
        return cls(f"Not a valid Backrooms: `{backrooms}`!")

    @classmethod
    def bad_backrooms_id(cls, backrooms_id: object):
        return cls(f"Not a valid Backrooms ID: `{backrooms_id}`!")

    @classmethod
    def bad_backrooms_d(cls, backrooms_d: object):
        return cls(f"Not a valid Backrooms Dimensions: `{backrooms_d}`!")

    @classmethod
    def bad_backrooms_cord_d(cls, cord: object) -> "BackRoomsError":
        return cls(f"Not a valid Backrooms Dimensions cord: `{cord}`!")


class BackRoomsCord:
    def __init__(self, x: int = 0, y: int = 0):
        self._x = x
        self._y = y

        if not isinstance(self.x, int) or not isinstance(self.y, int):
            raise BackRoomsError.bad_backrooms_cord(self)

    def __repr__(self):
        return f"<{self.__class__.__name__}: (x: {self.x}, y: {self.y})>"

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.x == other.x and self.y == other.y
        return False

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    def shift(self,
              x: int = 0,
              y: int = 0) -> "BackRoomsCord":
        return self.__class__(self.x + x, self.y + y)


class Hallway:
    def __init__(self,
                 name: Optional[str] = None,
                 cord: Optional[BackRoomsCord] = None):
        self._name = name

        # check for valid name
        if self._name is not None and (not isinstance(self._name, str) or not is_name(self._name)):
            raise BackRoomsError.bad_hallway_name(self._name)

        if cord is None:
            cord = BackRoomsCord()

        self._cord = cord

        # check if cord is valid
        if not isinstance(cord, BackRoomsCord) or cord.y != 0:
            raise BackRoomsError.bad_hallway_cord(cord)

    def __repr__(self):
        return f"<{self.__class__.__name__}: (name: {self.name}, x: {self.x})>"

    def __hash__(self):
        return hash((self.name, self.cord))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.x == other.x
        return False

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self.x < other.x
        return False

    def __gt__(self, other):
        if isinstance(other, self.__class__):
            return self.x > other.x
        return False

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def cord(self) -> BackRoomsCord:
        return self._cord

    @property
    def x(self) -> int:
        return self._cord.x


class Backrooms:
    def __init__(self,
                 name: Optional[str] = None,
                 raw_backroom: Optional[Dict[BackRoomsCord, str]] = None,
                 hallways: Optional[List[Hallway]] = None):
        self._name = name

        # check for valid name
        if self._name is not None and (not isinstance(self._name, str) or not is_name(self._name)):
            raise BackRoomsError.bad_backroom_name(self._name)

        if raw_backroom is None:
            raw_backroom = {}

        self._raw_backroom = raw_backroom

        # check for valid raw backroom
        if not isinstance(self._raw_backroom, dict):
            raise BackRoomsError.bad_raw_backrooms(self._raw_backroom)

        for cord, entity in self._raw_backroom.items():
            # check if cord is valid
            if not isinstance(cord, BackRoomsCord):
                raise BackRoomsError.bad_backrooms_cord(cord)

            # check if entity is valid
            if not isinstance(entity, str) or len(entity) != 1:
                raise BackRoomsError.bad_backrooms_entity(entity)

        if hallways is None:
            hallways = []

        self._hallways = hallways

        # check if hallways is valid
        if not isinstance(self._hallways, list) or len(set([h.x for h in self._hallways])) != len(self._hallways):
            raise BackRoomsError.bad_hallways(self._hallways)

        for hallway in hallways:
            # check if hallway is valid
            if not isinstance(hallway, Hallway):
                raise BackRoomsError.bad_hallway(hallway)

        # sort hallways in reverse max to min
        self._hallways.sort(reverse=True)

        # make hallways immutable
        self._hallways = tuple(self._hallways)

        self._hallway_names = {}
        self._hallway_ids = {}
        self._hallways_set = set(self._hallways)

        for hallway_id, hallway in enumerate(hallways):
            self._hallway_names[hallway] = hallway.name
            self._hallway_ids[hallway] = hallway_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def hallways(self) -> Tuple[Hallway]:
        return self._hallways

    def write(self,
              cord: BackRoomsCord,
              entity: str):

        # check if cord is valid
        if not isinstance(cord, BackRoomsCord):
            raise BackRoomsError.bad_backrooms_cord(cord)

        # check if entity is valid
        if not isinstance(entity, str) or len(entity) != 1:
            raise BackRoomsError.bad_backrooms_entity(entity)

        self._raw_backroom[cord] = entity

    def read(self,
             cord: BackRoomsCord) -> str:
        # check if cord is valid
        if not isinstance(cord, BackRoomsCord):
            raise BackRoomsError.bad_backrooms_cord(cord)
        return self._raw_backroom.get(cord, " ")

    def is_vacant(self, cord: BackRoomsCord) -> bool:
        # check if cord is valid
        if not isinstance(cord, BackRoomsCord):
            raise BackRoomsError.bad_backrooms_cord(cord)
        return cord in self._raw_backroom

    def get_hallway(self, name: str) -> Optional[Hallway]:
        # check for valid name
        if not isinstance(name, str) or not is_name(name):
            raise BackRoomsError.bad_hallway_name(name)
        return self._hallway_names.get(name)

    def get_higher_hallway(self, hallway: Hallway) -> Optional[Hallway]:
        # check if hallway is valid
        if not isinstance(hallway, Hallway):
            raise BackRoomsError.bad_hallway(hallway)

        # check that hallway is being used in theses backrooms
        if hallway not in self._hallways_set:
            raise BackRoomsError.unidentified_hallway(hallway)
        hallway_id = self._hallway_ids[hallway]
        if hallway_id == 0:
            return
        return self.hallways[hallway_id - 1]

    def get_lower_hallway(self, hallway: Hallway) -> Optional[Hallway]:
        # check if hallway is valid
        if not isinstance(hallway, Hallway):
            raise BackRoomsError.bad_hallway(hallway)

        # check that hallway is being used in theses backrooms
        if hallway not in self._hallways_set:
            raise BackRoomsError.unidentified_hallway(hallway)
        hallway_id = self._hallway_ids[hallway]
        if hallway_id + 1 == len(self.hallways):
            return
        return self.hallways[hallway_id + 1]

    def in_hallway(self, cord: BackRoomsCord) -> Optional[Hallway]:
        # check if cord is valid
        if not isinstance(cord, BackRoomsCord):
            raise BackRoomsError.bad_backrooms_cord(cord)

        # TODO make this faster
        in_hallway = None
        for hallway in self.hallways:
            if cord.x <= hallway.x:
                in_hallway = hallway
        return in_hallway

    def parallel(self, name: Optional[str] = None) -> "Backrooms":
        return self.__class__(name=name, raw_backroom=self._raw_backroom.copy(), hallways=list(self.hallways))


class BackRoomsCordD(BackRoomsCord):
    def __init__(self,
                 x: int = 0,
                 y: int = 0,
                 z: int = 0):
        self._z = z

        try:
            super(BackRoomsCordD, self).__init__(x=x, y=y)
        except BackRoomsError:
            raise BackRoomsError.bad_backrooms_cord_d(self)

        # check if z is valid
        if not isinstance(self.z, int):
            raise BackRoomsError.bad_backrooms_cord_d(self)

    def __repr__(self):
        return f"<{self.__class__.__name__}: (x: {self.x}, y: {self.y}, z:{self.z})>"

    def __hash__(self):
        return hash((super(BackRoomsCordD, self).__hash__(), self._z))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.z == other.z and super(BackRoomsCordD, self).__eq__(other)
        return False

    @property
    def z(self) -> int:
        return self._z

    def shift(self,
              x: int = 0,
              y: int = 0,
              z: int = 0) -> "BackRoomsCordD":
        return self.__class__(self.x + x, self.y + y, self.z + z)


class BackroomsD:
    def __init__(self,
                 backrooms_d: Optional[Dict[int, Backrooms]] = None):
        if backrooms_d is None:
            backrooms_d = {}

        self._backrooms_d = backrooms_d

        # check if backrooms_d is valid
        if not isinstance(self._backrooms_d, dict):
            raise BackRoomsError.bad_backrooms_d(self._backrooms_d)

        for backrooms_id, backrooms in self._backrooms_d.items():
            # check if backrooms_id is valid
            if not isinstance(backrooms_id, int):
                raise BackRoomsError.bad_backrooms_id(backrooms_id)
            # check if backrooms is valid
            if not isinstance(backrooms, Backrooms):
                raise BackRoomsError.bad_backrooms(backrooms)

        self._rebuild()

    # "reconnect"
    def _rebuild(self):
        # find all the first hallways that have a name
        self._first_hallways = {}
        # dick of all the first names of hallways which points to its cords
        backrooms_d_ordered = list(self._backrooms_d.keys())
        backrooms_d_ordered.sort(reverse=True)
        for backrooms_d_id in backrooms_d_ordered:
            backrooms = self._backrooms_d[backrooms_d_id]
            for hallway in backrooms.hallways:
                hallway_name = hallway.name
                # check that hallway has name and it is the first hallway with that name
                if hallway_name is not None and hallway_name not in self._first_hallways:
                    self._first_hallways[hallway_name] = BackRoomsCordD(x=hallway.x, z=backrooms_d_id)

        self._backrooms_d_inverse = {backrooms: backrooms_id for backrooms_id, backrooms in self._backrooms_d.items()}

        self._backroom_names = {}
        for _, backrooms in self._backrooms_d.items():
            backrooms_name = backrooms.name
            if backrooms_name is not None:
                # check to make sure no backrooms share the same name
                if backrooms_name in self._backroom_names:
                    raise BackRoomsError.bad_backrooms_d(self._backrooms_d)
                self._backroom_names[backrooms_name] = backrooms

    def add_backrooms(self,
                      backrooms_id: int,
                      backrooms: Optional[Backrooms]) -> None:
        # check if backrooms_id is valid
        if not isinstance(backrooms_id, int):
            raise BackRoomsError.bad_backrooms_id(backrooms_id)

        # check if backrooms is valid
        if not isinstance(backrooms, Backrooms):
            raise BackRoomsError.bad_backrooms(backrooms)

        self._backrooms_d[backrooms_id] = backrooms
        self._rebuild()

    def find_first_hallway(self,
                           name: str = "GATE") -> Optional[BackRoomsCordD]:
        return self._first_hallways.get(name)

    def get_backrooms(self,
                      backrooms_id: int) -> Backrooms:
        # check if backrooms_id is valid
        if not isinstance(backrooms_id, int):
            raise BackRoomsError.bad_backrooms_id(backrooms_id)

        # make "find" a new back room
        if backrooms_id not in self._backrooms_d:
            self._backrooms_d.setdefault(backrooms_id, Backrooms())
            self._backrooms_d_inverse[self._backrooms_d[backrooms_id]] = backrooms_id
        return self._backrooms_d[backrooms_id]

    def get_backrooms_from_name(self,
                                name: str) -> Optional[Backrooms]:
        # check if backrooms_id is valid
        if not isinstance(name, str):
            raise BackRoomsError.bad_backroom_name(name)
        return self._backroom_names.get(name)

    def write(self,
              cord: BackRoomsCordD,
              entity: str):

        # check if cord is valid
        if not isinstance(cord, BackRoomsCordD):
            raise BackRoomsError.bad_backrooms_cord_d(cord)

        backrooms = self.get_backrooms(cord.z)
        backrooms.write(cord, entity)

    def read(self,
             cord: BackRoomsCordD) -> str:
        # check if cord is valid
        if not isinstance(cord, BackRoomsCord):
            raise BackRoomsError.bad_backrooms_cord_d(cord)
        backrooms = self.get_backrooms(cord.z)
        return backrooms.read(cord)

    def is_vacant(self, cord: BackRoomsCord) -> bool:
        # check if cord is valid
        if not isinstance(cord, BackRoomsCordD):
            raise BackRoomsError.bad_backrooms_cord_d(cord)

        backrooms = self.get_backrooms(cord.z)
        return backrooms.is_vacant(cord)

    def get_hallway(self,
                    backrooms_id: int,
                    name: str) -> Optional[Hallway]:
        # check if backrooms_id is valid
        if not isinstance(backrooms_id, int):
            raise BackRoomsError.bad_backrooms_id(backrooms_id)
        backrooms = self.get_backrooms(backrooms_id)
        return backrooms.get_hallway(name)

    def get_higher_hallway(self,
                           backrooms_id: int,
                           hallway: Hallway) -> Optional[Hallway]:
        # check if backrooms_id is valid
        if not isinstance(backrooms_id, int):
            raise BackRoomsError.bad_backrooms_id(backrooms_id)
        backrooms = self.get_backrooms(backrooms_id)
        return backrooms.get_higher_hallway(hallway)

    def get_lower_hallway(self,
                          backrooms_id: int,
                          hallway: Hallway) -> Optional[Hallway]:
        # check if backrooms_id is valid
        if not isinstance(backrooms_id, int):
            raise BackRoomsError.bad_backrooms_id(backrooms_id)
        backrooms = self.get_backrooms(backrooms_id)
        return backrooms.get_lower_hallway(hallway)

    def in_hallway(self,
                   cord: BackRoomsCordD) -> Optional[Hallway]:
        # check if cord is valid
        if not isinstance(cord, BackRoomsCordD):
            raise BackRoomsError.bad_backrooms_cord_d(cord)

        backrooms = self.get_backrooms(cord.z)
        return backrooms.in_hallway(cord)
