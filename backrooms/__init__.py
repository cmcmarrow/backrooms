"""
Copyright 2021 Charles McMarrow

This python module "backrooms" is a Esolang.

backrooms was inspired by:
    * backrooms Creepypasta/MEME
    * ASCIIDOTS Esolang
    * CISC Architecture

Backrooms was designed to be:
    * hackable VIA memory overflow attacks, poor error handling, ect.
    * visually pleasing.
    * enjoy able to write small/medium programs.
    * capable to rewrite all of a program at run-time.
"""

# backrooms
from . import backrooms_error
from . import backrooms
from . import rooms
from . import rules
from . import translator
from . import stack
from . import conscious
from . import portal
from . import whisper
from . import backrooms_builtins

AUTHOR = "Charles McMarrow"

MAJOR, MINOR, MAINTENANCE = 0, 4, 0
VERSION = (MAJOR, MINOR, MAINTENANCE)
