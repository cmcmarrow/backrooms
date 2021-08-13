"""
Copyright 2021 Charles McMarrow
"""


# backrooms
from backrooms.translator import StringHandler

NAME = "h_vector"

SCRIPT = """
%utils


# WS[...] -> WS[size, ...]
~SIZE
/>rs"_SIZE"hcphr


~_SIZE
/>ri0ri9hr


# WS[item, ...] -> WS[...]
~APPEND
/>rs"SIZE"hck0dfrs"_START"hg-zisk1fzrs"utils"rs"NEW"hlfs1rs"utils"rs"KEEP"hls0+frs"_SIZE"rs"utils"rs"KEEP"hlhr


# WS[...] -> WS[item, ...]
~POP
/>rs"SIZE"hcZV-k0rs"READ"hcfs0bcrs"utils"rs"REMOVE"hls0frs"_SIZE"rs"utils"rs"KEEP"hlhr
/            >prnhr


# WS[...] -> WS[item, ...]
~PEAK
/>rs"SIZE"hcZV-rs"READ"hchr
/            >prnhr


# WS[spot, ...] -> WS[item, ...]
~READ
/>bcfzrs"utils"rs"STORE"hlhr


# WS[spot, item, ...] -> WS[...]
~WRITE
/>bcfzrs"utils"rs"KEEP"hlhr


# WS[spot, ...] -> WS[...]
~REMOVE
/V                    >ppprs"POP"hcphr
/>ic+rs"SIZE"hcz>uoisZ^pddrs"READ"V
/               ^+ch"ETIRW"sr-zch.<


# WS[spot, item, ...] -> WS[...]
~INSERT
/V                                       >pprs"WRITE"hchr
/>icd-k0prs"SIZE"hc-rnrs"APPEND"hc>ds0isZ^pddrs"READ"V
/                                 ^-ch"ETIRW"sr+zch..<


# WS[item, ...] -> WS[...]
~FIND_INSERT
/V                                                                      V..............................p2kp<
/>k0pri0k1prs"SIZE"hck2ZVps0ri0rs"READ"hcis.GVZV>ps0s2-rs"READ"hcisLVZVp>s2s1isri2ids1iadrs"READ"hcs0isGVZV^
/      rhch"DNEPPA"sr0sp<rhch"TRESNI"sr0ir0sp<.<   rhch"DNEPPA"sr0sp<.< ^....p1kppVZVLsi0sch"DAER"srd+dp<.<
/                                                                                 >.>ps0zrs"INSERT"hcphr


~_START
/
"""


def get_handler() -> StringHandler:
    """
    info: Gets script handler.
    :return: StringHandler
    """
    return StringHandler(NAME, SCRIPT)
