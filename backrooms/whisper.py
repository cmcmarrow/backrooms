"""
Copyright 2021 Charles McMarrow

This script holds a simple whisper_level system "log".
"""

# built-in
import logging
from functools import partial
from typing import Callable

WHISPER = logging.getLogger("backrooms")
WHISPER_HANDLER = logging.StreamHandler()
WHISPER_FORMATTER = logging.Formatter('[%(asctime)s][%(thread)d][%(levelname)s] %(message)s')
WHISPER_HANDLER.setFormatter(WHISPER_FORMATTER)
WHISPER.addHandler(WHISPER_HANDLER)
WHISPER_RUNNING = False


NOTSET = "NOTSET"
DEBUG = "DEBUG"
INFO = "INFO"
WARNING = "WARNING"
ERROR = "ERROR"
CRITICAL = "CRITICAL"


WHISPER_LEVEL_STR_TO_INT = {NOTSET: logging.NOTSET,
                            DEBUG: logging.DEBUG,
                            INFO: logging.INFO,
                            WARNING: logging.WARNING,
                            ERROR: logging.ERROR,
                            CRITICAL: logging.CRITICAL}


def enable_whisper(level: str = DEBUG) -> None:
    """
    info: Sets the whisper_level leve.
    :param level: str
    :return: None
    """
    global WHISPER_RUNNING

    level = level.upper()
    if level != NOTSET:
        WHISPER_RUNNING = True
    else:
        WHISPER_RUNNING = False
    level = WHISPER_LEVEL_STR_TO_INT.get(level, logging.NOTSET)
    WHISPER.setLevel(level)


def _whisper(level: Callable, data: str) -> None:
    """
    info: Checks if logging is enabled, then logs data.
        This is done because python logging slows down the program even
        if the logger is not enabled.
    :param level: Callable
    :param data: str
    :return: None
    """
    if WHISPER_RUNNING:
        level(data)


debug = partial(_whisper, WHISPER.debug)
info = partial(_whisper, WHISPER.info)
warning = partial(_whisper, WHISPER.warning)
error = partial(_whisper, WHISPER.error)
critical = partial(_whisper, WHISPER.critical)
