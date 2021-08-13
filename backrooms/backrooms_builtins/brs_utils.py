"""
Copyright 2021 Charles McMarrow
"""


# backrooms
from backrooms.translator import StringHandler

NAME = "utils"

SCRIPT = """
# WS[item, ...] -> WS[string, ...]
~WSIZE
/>rs"ri"bjddbldbliari2iak0bjrs"hr"bjds0isZVppdbldbliari3iabjrs"hr"bjhr
/                                         >pzphr


~EMPTY_BLOCK
# WS[block_size, ...] -> WS[empty_block_size, ...]
/>k0prs"">ds0zisZVrs" ".......V
/        .       >phr         .
/        ^jbch"KCOLB_YTPME_"sr<


~_EMPTY_BLOCK
/>zk0p>ddbjds0isLVZVpphr
/     ^.......pzp< >pzphr


# WS[item, ...] -> WS[string, ...]
~TYPE_READ
/V
/I
/>rs"ri"zbjhr
/S
/>rs"rs"ri0ibbjzbjri0ibbjhr
/F
/>prs"rf"hr
/>prs"rn"hr

#### BASE HEAP
# WS[y, f, item, ...] -> WS[...]
~KEEP
/>uors"CLEAR"hck1pk2prs"TYPE_READ"hcrs">"zbjrs"WSIZE"hck0ps0ri0s1s2ushr


# WS[y, f, ...] -> WS[item, ...]
~STORE
/>hlphr


# WS[y, f, ...] -> WS[...]
~CLEAR
/>uohlzprs"EMPTY_BLOCK"hck0pk1pk2ps0ri0s1s2ushr


# WS[y, f, ...] -> WS[...]
~REMOVE
/>uors"CLEAR"hchdhr


# WS[y, f, name, ...] -> WS[...]
~NEW
/>k0zk1zhsrs"rnri7hr"ri0s0s1ushr
####
"""


def get_handler() -> StringHandler:
    """
    info: Gets script handler.
    :return: StringHandler
    """
    return StringHandler(NAME, SCRIPT)
