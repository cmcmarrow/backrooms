"""
Copyright 2021 Charles McMarrow
"""


# backrooms
from backrooms.translator import StringHandler

NAME = "utils"

SCRIPT = """
# write size
~WSIZE
/>rs"ri"bjddbldbliari2iak0bjrs"hr"bjds0isZVppdbldbliari3iabjrs"hr"bjhr
/                                         >pzphr

~EMPTY_BLOCK
/>k0prs"">ds0zisZVrs" ".......V
/        .       >phr         .
/        ^jbch"KCOLB_YTPME_"sr<

~_EMPTY_BLOCK
/>zk0p>ddbjds0isLVZVpphr
/     ^.......pzp< >pzphr
"""


def get_handler() -> StringHandler:
    """
    info: Gets script handler.
    :return: StringHandler
    """
    return StringHandler(NAME, SCRIPT)
