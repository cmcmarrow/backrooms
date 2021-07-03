"""
Copyright 2021 Charles McMarrow

This script holds a the backrooms API and console interface.
"""

# built-in
import argparse
import cProfile
from typing import Optional, Tuple, Union

# backrooms
from . import backrooms_error
from .backrooms_builtins import get_builtins
from .portal import Portal
from .translator import translator, Handlers, Handler, load_dir
from .whisper import NOTSET, enable_whisper


class BackRoomsError(backrooms_error.BackroomsError):
    pass


def _str_to_bool(boolean: str):
    return boolean.lower() not in ("false", "f", "", "0")


def backrooms() -> None:    # TODO write tests
    """
    info: Console Interface
    :return: None
    """
    try:
        parser = argparse.ArgumentParser(description="backrooms")
        parser.add_argument("file",
                            type=str,
                            action="store",
                            help="path to main file")
        parser.add_argument("--lost-count",
                            default=0,
                            type=int,
                            action="store",
                            help="set lost count")
        parser.add_argument("--lost-rule-count",
                            default=0,
                            type=int,
                            action="store",
                            help="set lost rule count")
        parser.add_argument("--error-on-space",
                            default=False,
                            type=_str_to_bool,
                            action="store",
                            help="errors if portal lands on a space")
        parser.add_argument("--builtins",
                            default=True,
                            type=_str_to_bool,
                            action="store",
                            help="include built-in libraries")
        parser.add_argument("--whisper",
                            default=NOTSET,
                            type=str,
                            action="store",
                            help="set the log level [notset, debug, info, warning, error, critical]")
        parser.add_argument("--profile",
                            default=False,
                            type=_str_to_bool,
                            action="store",
                            help="profiles backrooms")
        args = parser.parse_args()
        br = backrooms_api(code=args.file,
                           lost_count=args.lost_count,
                           lost_rule_count=args.lost_rule_count,
                           error_on_space=args.error_on_space,
                           br_builtins=args.builtins,
                           whisper_level=args.whisper)
        if args.profile:
            with cProfile.Profile() as profiler:
                br()
            print(flush=True)
            profiler.print_stats()
        else:
            br()
    except backrooms_error.BackroomsError as e:
        print(f"ERROR: {e}")
    except KeyboardInterrupt:
        print("Keyboard Interrupt!")


def backrooms_api(code: Union[str, Handler, Handlers],
                  inputs: Optional[Tuple[str, ...]] = None,
                  sys_output: bool = True,
                  catch_output: bool = False,
                  lost_count: int = 0,
                  lost_rule_count: int = 0,
                  error_on_space: bool = False,
                  br_builtins: bool = True,
                  whisper_level: str = NOTSET) -> Portal:
    """
    info: An API to backrooms.
    :param code: Union[str, Handler, Handlers]
        str: Will treat str as main file and load its dir.
        Handler: Will load just the single Handler.
        Handlers: Will load the Handlers.
    :param inputs: Optional[Tuple[str, ...]]
    :param sys_output: bool
    :param catch_output: bool
    :param lost_count: int
    :param lost_rule_count: int
    :param error_on_space: bool
    :param br_builtins: bool
        Only adds builtins if code is str or Handler.
    :param whisper_level: str
    :return: Portal
    """
    try:
        if isinstance(code, str):
            main_handler, handlers = load_dir(code)
            handlers = [handlers]
            if br_builtins:
                handlers.append(get_builtins())
            rooms = translator(Handlers(main_handler, tuple(handlers)))
        elif isinstance(code, Handler):
            handlers = []
            if br_builtins:
                handlers.append(get_builtins())
            rooms = translator(Handlers(code, tuple(handlers)))
        else:
            rooms = translator(code)

        enable_whisper(whisper_level)

        return Portal(rooms,
                      inputs=inputs,
                      sys_output=sys_output,
                      catch_output=catch_output,
                      lost_count=lost_count,
                      lost_rule_count=lost_rule_count,
                      error_on_space=error_on_space)
    except backrooms_error.BackroomsError as e:
        raise BackRoomsError(e)
