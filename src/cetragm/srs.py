# Definitions of the tomfuckery that is Super Rotation System (rotation and wallkicks)

from typing import Tuple, Callable, Dict, List

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

# These kick tables are not my values, they're from the Super Rotation System (or Tetris Guideline)
JLSTZ_KICKS = _mk_kicks({ 
    ("0", "r"): [(0,0), (-1,0), (-1,1), (0,-2), (-1,-2)],
    ("r", "0"): [(0,0), (1,0), (1,-1), (0,2), (1,2)],
    
    ("r", "2"): [(0,0), (1,0), (1,-1), (0,2), (1,2)],
    ("2", "r"): [(0,0), (-1,0), (-1,1), (0,-2), (-1,-2)],
    
    ("2", "l"): [(0,0), (1,0), (1,1), (0,-2), (1,-2)],
    ("l", "2"): [(0,0), (-1,0), (-1,-1), (0,2), (-1,2)],
    
    ("l", "0"): [(0,0), (-1,0), (-1,-1), (0,2), (-1,2)],
    ("0", "l"): [(0,0), (1,0), (1,1), (0,-2), (1,-2)],
})

I_KICKS = _mk_kicks({
    ("0", "r"): [(0,0), (-2,0), (1,0), (-2,-1), (1,2)],
    ("r", "0"): [(0,0), (2,0), (-1,0), (2,1), (-1,-2)],
    
    ("r", "2"): [(0,0), (-1,0), (2,0), (-1,2), (2,-1)],
    ("2", "r"): [(0,0), (1,0), (-2,0), (1,-2), (-2,1)],
    
    ("2", "l"): [(0,0), (2,0), (-1,0), (2,1), (-1,-2)],
    ("l", "2"): [(0,0), (-2,0), (1,0), (-2,-1), (1,2)],
    
    ("l", "0"): [(0,0), (1,0), (-2,0), (1,-2), (-2,1)],
    ("0", "l"): [(0,0), (-1,0), (2,0), (-1,2), (2,-1)],
})

O_KICKS = {
    ("0", "r"): [(0,0)],
    ("r", "2"): [(0,0)],
    
    ("2", "l"): [(0,0)],
    ("l", "0"): [(0,0)],
    
    ("r", "0"): [(0,0)],
    ("2", "r"): [(0,0)],
    
    ("l", "2"): [(0,0)],
    ("0", "l"): [(0,0)],
}