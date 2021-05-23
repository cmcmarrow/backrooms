"""
Copyright 2021 Charles McMarrow

This file holds the definition for valid Backrooms names.
Why not use other Unicode charters for the name. Well, they can’t pronounce them and
they cannot know what is not inside my head.
They do not make many people into their vessels nor are they interested into learning are language.
"""

from string import ascii_letters, digits


NAME_CHARS = set(ascii_letters + digits + "_")


def is_name(name: str) -> bool:
    for c in name:
        if c not in NAME_CHARS:
            return False
    return bool(name)
