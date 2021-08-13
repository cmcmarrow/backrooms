"""
Copyright 2021 Charles McMarrow
"""


# backrooms
from backrooms.translator import StringHandler

NAME = "heap"

SCRIPT = """
%utils


=h_vector heap_vector


# WS[...] -> WS[spot, ...]
~_HEAD
/>rs"__HEAD"hcphr


# WS[...] -> WS[spot, block_size, ...]
~__HEAD
/>ri0ri9hr


# WS[AT, ID, ...] -> WS[ID, ...]
~AT
/>ZVrs"_"zbjbjhr
/  >phr


# WS[...] -> WS[PT, ...]
~_NEW
/>rs"heap_vector"rs"POP"hlOVhr
/                          >prs"_HEAD"hcri1isdfrs"__HEAD"rs"utils"rs"KEEP"hlfrs"_START"hgiarihr


# WS[...] -> WS[ID, ...]
~NEW
/>rs"_NEW"hck0ri-1imbcdfs0rs"utils"rs"NEW"hlhr


# WS[SIZE, ...] -> WS[ID, ...]
~NEW_A
/V                         >pps1hr
/>k0prs"NEW"hck1pri1>ds0isZ^pdrs"_"zbjs1zbjrs"_NEW"V
/                   ^ai1irlh"WEN"sr"slitu"srzfch...<                       


# WS[ID, ...] -> WS[item, ...]
~READ
/>fzrs"utils"rs"STORE"hlhr


# WS[AT, ID, ...] -> WS[item, ...]
~READ_A
/>rs"AT"hcrs"READ"hchr


# WS[ID, item, ...] -> WS[...]
~WRITE
/>fzrs"utils"rs"KEEP"hlhr


# WS[AT, ID, item, ...] -> WS[...]
~WRITE_A
/>rs"AT"hcrs"WRITE"hchr


# WS[ID, ...] -> WS[...]
~FREE
/>ri0>uors"AT"hcdfzhg.IVpppphr
/    ^ai1irch"EERF_"srp<


# WS[ID, ...] -> WS[...]
~_FREE
/>dfzhgOVzfzrs"utils"rs"REMOVE"hldfrs"_START"hgrs"_HEAD"hciaisZVprs"heap_vector"rs"FIND_INSERT"hlhr
/   rhpp<                                                      >pk0p>s0ri1iadrs"heap_vector"rs"PEAK"hlOVisNVV
/                                                     rhlh"PEEK"sr"slitu"sr"DAEH__"srfsigh"TRATS_"srfpp<2..<p
/                                                                   1                                       .
/                                                                   ^...........plh"POP"sr"rotcev_paeh"srp0k<


~0
/>rnri8hr


~_START
/
"""


def get_handler() -> StringHandler:
    """
    info: Gets script handler.
    :return: StringHandler
    """
    return StringHandler(NAME, SCRIPT)
