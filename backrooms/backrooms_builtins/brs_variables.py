"""
Copyright 2021 Charles McMarrow
"""


# backrooms
from backrooms.translator import StringHandler

NAME = "vars"

SCRIPT = """
%utils


=h_vector vars_vector


# WS[...] -> WS[spot, ...]
~_HEAD
/>rs"__HEAD"hcphr


# WS[...] -> WS[spot, block_size, ...]
~__HEAD
/>ri0ri9hr


# WS[name, ...] -> WS[...]
~_HAS
/>dfzhgIVprs"vars_vector"rs"POP"hlOVfzrs"utils"rs"NEW"hlhr
/   rhpp<                          >prs"_HEAD"hc-dfrs"__HEAD"rs"utils"rs"KEEP"hlfrs"_START"hgiafzV
/                                                                            rhlh"WEN"sr"slitu"sr<


# WS[name, ...] -> WS[item, ...]
~GET
/>drs"_HAS"hcfzrs"utils"rs"STORE"hlhr


# WS[name item, ...] -> WS[...]
~SET
/>drs"_HAS"hcfzrs"utils"rs"KEEP"hlhr


# WS[name, ...] -> WS[...]
~DEL
/>dfzhgOVzfzrs"utils"rs"REMOVE"hldfrs"_START"hgrs"_HEAD"hciaisZVprs"vars_vector"rs"FIND_INSERT"hlhr
/   rhpp<                                                      >pk0p>s0+drs"vars_vector"rs"PEAK"hlOVisNVV
/                                                 rhlh"PEEK"sr"slitu"sr"DAEH__"srfsigh"TRATS_"srfpp<2..<p
/                                                                   1                                   .
/                                                                   ^.......plh"POP"sr"rotcev_srav"srp0k<

~_START
/
"""


def get_handler() -> StringHandler:
    """
    info: Gets script handler.
    :return: StringHandler
    """
    return StringHandler(NAME, SCRIPT)
