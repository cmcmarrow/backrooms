"""
Copyright 2021 Charles McMarrow

This module "backrooms" is a Esolang.

backrooms was inspired by:
    * backrooms Creepypasta/MEME
    * ASCIIDOTS Esolang
    * CISC Architecture

Backrooms was designed to be:
    * hackable VIA memory overflow attacks, poor unhandled error handling, ect.
    * visually pleasing.
    * enjoy able to write small/medium programs.
    * capable to rewrite all of a program at run-time.
"""

# backrooms
from . import backrooms_error
from . import rooms
from . import rules
from . import translator

AUTHOR = "Charles McMarrow"

MAJOR, MINOR, MAINTENANCE = 0, 1, 0
VERSION = (MAJOR, MINOR, MAINTENANCE)
