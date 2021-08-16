"""
Copyright 2021 Charles McMarrow

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

This python module "backrooms" is a Esolang.

Backrooms is inspired by:
    * Backrooms Creepypasta/MEME
    * ASCIIDOTS Esolang
    * CISC Architecture

Backrooms is designed to be:
    * Hackable VIA memory overflow attacks and poor error handling.
    * Visually pleasing.
    * Enjoyable to write small/medium programs.
    * Capable of rewriting all of a program at run-time.
"""


# backrooms
from . import backrooms
from . import backrooms_builtins
from . import backrooms_error
from . import conscious
from . import portal
from . import rooms
from . import rules
from . import stack
from . import translator
from . import whisper

AUTHOR = "Charles McMarrow"

MAJOR, MINOR, MAINTENANCE = 1, 0, 0
VERSION = (MAJOR, MINOR, MAINTENANCE)
