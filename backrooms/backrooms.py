"""
Copyright 2021 Charles McMarrow

This script holds a the backrooms API and console interface.
"""

# built-in
import argparse
import cProfile
from copy import deepcopy
import pstats
from pstats import SortKey
from typing import Optional, Tuple, Union, Type

# backrooms
import backrooms as brs
from . import backrooms_error
from .backrooms_builtins import get_builtins
from .portal import Portal
from .translator import translator, Handlers, Handler, load_dir, StringHandler, FileHandler
from .whisper import NOTSET, enable_whisper
from .rules import Rule


class BackRoomsError(backrooms_error.BackroomsError):
    pass


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
        parser.add_argument("-a",
                            "--author",
                            default=False,
                            action="store_true",
                            help="get author of backrooms")
        parser.add_argument("-b",
                            "--builtins",
                            default=True,
                            action="store_false",
                            help="don't include built-in libraries")
        parser.add_argument("-c",
                            "--core_dump",
                            default=False,
                            action="store_true",
                            help="enables CoreDump rule \"?\"")
        parser.add_argument("-e",
                            "--error-on-space",
                            default=False,
                            action="store_true",
                            help="errors if portal lands on a space")
        parser.add_argument("-p",
                            "--profile",
                            default=False,
                            action="store_true",
                            help="profiles backrooms")
        parser.add_argument("-s",
                            "--system-out",
                            default=True,
                            action="store_false",
                            help="don't write to stdio")
        parser.add_argument("-v",
                            "--version",
                            default=False,
                            action="store_true",
                            help="get version of backrooms")
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
        parser.add_argument("--profile_range",
                            default=1,
                            type=int,
                            action="store",
                            help="")
        parser.add_argument("--whisper",
                            default=NOTSET,
                            type=str,
                            action="store",
                            help="set the log level [notset, debug, info, warning, error, critical]")
        args = parser.parse_args()

        if args.author:
            print(brs.AUTHOR)

        if args.version:
            print(f"v{brs.MAJOR}.{brs.MINOR}.{brs.MAINTENANCE}")

        if args.profile:
            try:
                with cProfile.Profile(builtins=False) as profiler_translator:
                    for _ in range(args.profile_range):
                        br = backrooms_api(code=args.file,
                                           sys_output=args.system_out,
                                           lost_count=args.lost_count,
                                           lost_rule_count=args.lost_rule_count,
                                           error_on_space=args.error_on_space,
                                           br_builtins=args.builtins,
                                           core_dump=args.core_dump,
                                           whisper_level=args.whisper)

                profiler_run_time = cProfile.Profile(builtins=False)
                for _ in range(args.profile_range):
                    profiler_run_time.disable()
                    br_copy = deepcopy(br)
                    profiler_run_time.enable(builtins=False)
                    br_copy()
                profiler_run_time.disable()
            finally:
                print(flush=True)
                print("TRANSLATOR PROFILE:")
                stats = pstats.Stats(profiler_translator)
                stats.sort_stats(SortKey.TIME)
                stats.print_stats()
                if "profiler_run_time" in locals():
                    print(flush=True)
                    print("RUN TIME PROFILE:")
                    stats = pstats.Stats(profiler_run_time)
                    stats.sort_stats(SortKey.TIME)
                    stats.print_stats()
        else:
            br = backrooms_api(code=args.file,
                               sys_output=args.system_out,
                               lost_count=args.lost_count,
                               lost_rule_count=args.lost_rule_count,
                               error_on_space=args.error_on_space,
                               br_builtins=args.builtins,
                               core_dump=args.core_dump,
                               whisper_level=args.whisper)
            br()
    except backrooms_error.BackroomsError as e:
        print(f"\nERROR: {e}", flush=True)
    except KeyboardInterrupt:
        print("\nKeyboard Interrupt!", flush=True)


def backrooms_api(code: Union[str, Handler, Handlers],
                  inputs: Optional[Tuple[str, ...]] = None,
                  sys_output: bool = True,
                  catch_output: bool = False,
                  lost_count: int = 0,
                  lost_rule_count: int = 0,
                  error_on_space: bool = False,
                  br_builtins: bool = True,
                  core_dump: bool = False,
                  rules: Optional[Tuple[Type[Rule]]] = None,
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
    :param core_dump: bool
    :param rules: Optional[Tuple[Type[Rule]]]
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
                      error_on_space=error_on_space,
                      core_dump=core_dump,
                      rules=rules)
    except backrooms_error.BackroomsError as e:
        raise BackRoomsError(e)
