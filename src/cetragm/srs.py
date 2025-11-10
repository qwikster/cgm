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

# These kick tables are not my values, they're from the Super Rotation System (or Tetris Guideline)
JLSTZ_KICKS = { 
    ("0", "r"): [(0,0), (-1,0), (-1,1), (0,-2), (-1,-2)],
    ("r", "0"): [(0,0), (1,0), (1,-1), (0,2), (1,2)],
    
    ("r", "2"): [(0,0), (1,0), (1,-1), (0,2), (1,2)],
    ("2", "r"): [(0,0), (-1,0), (-1,1), (0,-2), (-1,-2)],
    
    ("2", "l"): [(0,0), (1,0), (1,1), (0,-2), (1,-2)],
    ("l", "2"): [(0,0), (-1,0), (-1,-1), (0,2), (-1,2)],
    
    ("l", "0"): [(0,0), (-1,0), (-1,-1), (0,2), (-1,2)],
    ("0", "l"): [(0,0), (1,0), (1,1), (0,-2), (1,-2)],
}

I_KICKS = {
    ("0", "r"): [(0,0), (-2,0), (1,0), (-2,-1), (1,2)],
    ("r", "0"): [(0,0), (2,0), (-1,0), (2,1), (-1,-2)],
    
    ("r", "2"): [(0,0), (-1,0), (2,0), (-1,2), (2,-1)],
    ("2", "r"): [(0,0), (1,0), (-2,0), (1,-2), (-2,1)],
    
    ("2", "l"): [(0,0), (2,0), (-1,0), (2,1), (-1,-2)],
    ("l", "2"): [(0,0), (-2,0), (1,0), (-2,-1), (1,2)],
    
    ("l", "0"): [(0,0), (1,0), (-2,0), (1,-2), (-2,1)],
    ("0", "l"): [(0,0), (-1,0), (2,0), (-1,2), (2,-1)],
}

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

JLSTZ_KICKS_180 = {
    ("0","2"): [(0,0), (0,1), (0,2), (1,0), (-1,0), (1,1), (-1,1)],
    ("2","0"): [(0,0), (0,1), (0,2), (-1,0), (1,0), (-1,1), (1,1)],
    ("r","l"): [(0,0), (0,1), (0,2), (1,0), (-1,0), (1,1), (-1,1)],
    ("l","r"): [(0,0), (0,1), (0,2), (-1,0), (1,0), (-1,1), (1,1)],
}

I_KICKS_180 = {
    ("0","2"): [(0,0), (0,-1), (0,1), (1,0), (-1,0), (2,0), (-2,0)],
    ("2","0"): [(0,0), (0,-1), (0,1), (-1,0), (1,0), (-2,0), (2,0)],
    ("r","l"): [(0,0), (0,-1), (0,1), (1,0), (-1,0), (2,0), (-2,0)],
    ("l","r"): [(0,0), (0,-1), (0,1), (-1,0), (1,0), (-2,0), (2,0)],
}

def _kick_table(name: str):
    n = name.lower()
    if n == "i":
        return I_KICKS
    if n == "o":
        return O_KICKS
    return JLSTZ_KICKS

def _kick_table_180(name: str):
    n = name.lower()
    if n == "i":
        return I_KICKS_180
    if n == "o":
        return O_KICKS
    return JLSTZ_KICKS_180

Pos = Tuple[int, int]
CollidesFn = Callable[[str, str, Pos], bool]

def rotate_srs(
    name: str,
    pos: Pos,
    rot_label: str,
    direction: int,
    board,
    collides_fn: CollidesFn
) -> Tuple[str, Pos, bool]: # false if no kick
    name = name.lower()
    if rot_label not in ROT_SEQ:
        raise ValueError("invalid rotation")
    if direction not in (1, -1, 2):
        return rot_label, pos, False
    
    to_label = rotate_label(rot_label, direction)
    table = _kick_table_180(name) if direction == 2 else _kick_table(name)
    
    kicks = table.get((rot_label, to_label), [(0, 0)])
    for dx, dy in kicks:
        test_pos = (pos[0] + dx, pos[1] + dy)
        if not collides_fn(name, to_label, test_pos):
            return to_label, test_pos, True
    return rot_label, pos, False
    
def apply_rotate(
    piece: dict,
    direction: int,
    board,
    collides_fn: CollidesFn
) -> bool:
    name = piece["name"]
    pos = tuple(piece["pos"])
    rot = piece["rotation"]