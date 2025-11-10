# Definitions of the tomfuckery that is Super Rotation System (rotation and wallkicks)

from typing import Tuple, Callable, List

ROT_SEQ = ["0", "r", "2", "l"]

ROT_CW =  {"0": "r", "r": "2", "2": "l", "l": "0"}
ROT_CCW = {"0": "l", "l": "2", "2": "r", "r": "0"}
ROT_180 = {"0": "2", "2": "0", "r": "l", "l": "r"}

def rotate_label(current: str, direction:int) -> str:
    if direction == +1:
        return ROT_CW[current]
    if direction == -1:
        return ROT_CCW[current]
    if direction == 2:
        return ROT_180[current]
    return current

def _mk_kicks(pairs):
    return pairs

JLSTZ_KICKS = _mk_kicks({
    ("", ""): [(,), (,), (,), (,), (,)],
    ("", ""): [(,), (,), (,), (,), (,)],
    
    ("", ""): [(,), (,), (,), (,), (,)],
    ("", ""): [(,), (,), (,), (,), (,)],
    
    ("", ""): [(,), (,), (,), (,), (,)],
    ("", ""): [(,), (,), (,), (,), (,)],
    
    ("", ""): [(,), (,), (,), (,), (,)],
    ("", ""): [(,), (,), (,), (,), (,)],
})

I_KICKS = _mk_kicks({
    ("", ""): [(,), (,), (,), (,), (,)],
    ("", ""): [(,), (,), (,), (,), (,)],
    
    ("", ""): [(,), (,), (,), (,), (,)],
    ("", ""): [(,), (,), (,), (,), (,)],
    
    ("", ""): [(,), (,), (,), (,), (,)],
    ("", ""): [(,), (,), (,), (,), (,)],
    
    ("", ""): [(,), (,), (,), (,), (,)],
    ("", ""): [(,), (,), (,), (,), (,)],
})

O_KICKS = {
    ("", ""): [(,)],
    ("", ""): [(,)],
    ("", ""): [(,)],
    ("", ""): [(,)],
    ("", ""): [(,)],
    ("", ""): [(,)],
    ("", ""): [(,)],
    ("", ""): [(,)],
}