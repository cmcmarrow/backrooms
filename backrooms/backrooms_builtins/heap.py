"""
Copyright 2021 Charles McMarrow
"""


# backrooms
from backrooms.translator import StringHandler

HEAP_NAME = "heap"

HEAP = """
# -> Pointer [str]
~NEW
/>rs"_FREE"hcdblNVCpprs"_AT"hcdri1iabcrs"ri"zbjrs"hr"bjri0rs"_AT"fhgfri1ri0dudbcddicfhsdrnzrs"SET"hchr
# Pointer [str] ->                                                       
~FREE
# Pointer [str] -> Item[object]
~GET
# Item [object] Pointer [str] ->
~SET
/>SVIVFVCV
/  C C C C       
/  . 1 2 3             >epephr
/  >...................^
/    >rs"ri"zbjrs"hr"bj^
/      >prs"rfhr"......^
/        >prs"rnhr"....^
~_AT
/ri100hr
~_FREE
/rs""hr
"""


def get_handler() -> StringHandler:
    return StringHandler(HEAP_NAME, HEAP)
