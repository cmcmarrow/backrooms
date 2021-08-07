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
/>rs"SIZE"hck0dfrs"START"hgri1iszisk1fzrs"utils"rs"NEW"hlfs1rs"utils"rs"KEEP"hls0ri1iafrs"_SIZE"rs"utils"rs"KEEP"hlhr

# WS[...] -> WS[item, ...]
~POP
/>rs"SIZE"hcZVri1isk0rs"READ"hcfs0bcrs"utils"rs"REMOVE"hls0frs"_SIZE"rs"utils"rs"KEEP"hlhr
/            >prnhr

# WS[spot, ...] -> WS[item, ...]
~READ
/>bcfzrs"utils"rs"STORE"hlhr

# WS[spot, item, ...] -> WS[...]
~WRITE
/>bcfzrs"utils"rs"KEEP"hlhr

# WS[spot, ...] -> WS[...]
~REMOVE
/

# WS[spot, item, ...] -> WS[...]
~INSERT
/rnrs"APPEND"hczdick0p

# WS[item, ...] -> WS[...]
~FIND_INSERT
/

~START
/
"""


def get_handler() -> StringHandler:
    """
    info: Gets script handler.
    :return: StringHandler
    """
    return StringHandler(NAME, SCRIPT)
