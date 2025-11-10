# Definitions of the tomfuckery that is Super Rotation System (rotation and wallkicks)

from typing import Tuple, Callable, List, Dict

Pos = Tuple[int, int]
CollidesFn = Callable[[str, str, Pos], bool]

ROT_SEQ = ["0", "r", "2", "l"]
ROT_CW =  {"0": "r", "r": "2", "2": "l", "l": "0"}
ROT_CCW = {"0": "l", "l": "2", "2": "r", "r": "0"}
ROT_180 = {"0": "2", "2": "0", "r": "l", "l": "r"}
JLSTZ_OFFSETS = {"0": (0,0), "r": (0,0), "2": (0,0), "l": (0,0)}

I_OFFSETS = {
    "0": (-1, 0),
    "r": (1, 0),
    "2": (0, 1),
    "l": (0, -1),
}

# These kick tables are not my values, they're from the Super Rotation System (or Tetris Guideline)
# Also they were originally inverted until the commit that added this comment so i made an LLM invert them because im too lazy
JLSTZ_KICKS = { 
    ("0", "r"): [(0,0), (-1,0), (-1,-1), (0,2), (-1,2)],
    ("r", "0"): [(0,0), (1,0), (1,1), (0,-2), (1,-2)],
    
    ("r", "2"): [(0,0), (1,0), (1,1), (0,-2), (1,-2)],
    ("2", "r"): [(0,0), (-1,0), (-1,-1), (0,2), (-1,2)],
    
    ("2", "l"): [(0,0), (1,0), (1,-1), (0,2), (1,2)],
    ("l", "2"): [(0,0), (-1,0), (-1,1), (0,-2), (-1,-2)],
    
    ("l", "0"): [(0,0), (-1,0), (-1,1), (0,-2), (-1,-2)],
    ("0", "l"): [(0,0), (1,0), (1,-1), (0,2), (1,2)],
}

I_KICKS = {
    ("0", "r"): [(0,0), (-2,0), (1,0), (-2,1), (1,-2)],
    ("r", "0"): [(0,0), (2,0), (-1,0), (2,-1), (-1,2)],
    
    ("r", "2"): [(0,0), (-1,0), (2,0), (-1,-2), (2,1)],
    ("2", "r"): [(0,0), (1,0), (-2,0), (1,2), (-2,-1)],
    
    ("2", "l"): [(0,0), (2,0), (-1,0), (2,-1), (-1,2)],
    ("l", "2"): [(0,0), (-2,0), (1,0), (-2,1), (1,-2)],
    
    ("l", "0"): [(0,0), (1,0), (-2,0), (1,2), (-2,-1)],
    ("0", "l"): [(0,0), (-1,0), (2,0), (-1,-2), (2,1)],
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
    ("0","2"): [(0,0), (0,-1), (0,-2), (1,0), (-1,0), (1,-1), (-1,-1)],
    ("2","0"): [(0,0), (0,-1), (0,-2), (-1,0), (1,0), (-1,-1), (1,-1)],
    ("r","l"): [(0,0), (0,-1), (0,-2), (1,0), (-1,0), (1,-1), (-1,-1)],
    ("l","r"): [(0,0), (0,-1), (0,-2), (-1,0), (1,0), (-1,-1), (1,-1)],
}

I_KICKS_180 = {
    ("0","2"): [(0,0), (0,1), (0,-1), (1,0), (-1,0), (2,0), (-2,0)],
    ("2","0"): [(0,0), (0,1), (0,-1), (-1,0), (1,0), (-2,0), (2,0)],
    ("r","l"): [(0,0), (0,1), (0,-1), (1,0), (-1,0)],
    ("l","r"): [(0,0), (0,1), (0,-1), (-1,0), (1,0)],
}

def rotate_label(current: str, direction:int) -> str:
    if direction == +1:
        return ROT_CW[current]
    if direction == -1:
        return ROT_CCW[current]
    if direction == 2:
        return ROT_180[current]
    return current

def _offset_for(name: str, rot: str) -> Pos:
    n = name.lower()
    if n == "i":
        return I_OFFSETS[rot]
    return JLSTZ_OFFSETS[rot]

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

def _get_kicks_for(name: str, fr: str, to: str, direction: int) -> List[Tuple[int,int]]:
    table = _kick_table_180(name) if direction == 2 else _kick_table(name)
    if (fr, to) in table:
        return list(table[(fr,to)])
    if (to, fr) in table:
        return [(-dx, -dy) for dx, dy in table[(to, fr)]]
    return [(0,0)]

def try_rotate_srs(
    name: str,
    pos: Pos,
    rot_label: str,
    direction: int,
    board,
    collides_fn: CollidesFn,
) -> Tuple[str, Pos, bool]: # false if no kick
    name = name.lower()
    if rot_label not in ROT_SEQ:
        raise ValueError("invalid rotation")
    if direction not in (1, -1, 2):
        return rot_label, pos, False
    
    to_label = rotate_label(rot_label, direction)
    
    off_from = _offset_for(name, rot_label)
    off_to = _offset_for(name, to_label)
    delta_off = (off_from[0] - off_to[0], off_from[1] - off_to[1])
    
    kicks = _get_kicks_for(name, rot_label, to_label, direction)
        
    for dx, dy in kicks:
        tx = pos[0] + dx + delta_off[0]
        ty = pos[1] + dy + delta_off[1]
        if not collides_fn(name, to_label, (tx, ty)):
            return to_label, (tx, ty), True
    return rot_label, pos, False
    
def rotate_srs(
    piece: dict,
    direction: int,
    board,
    collides_fn: CollidesFn,
) -> bool:
    name = piece["name"]
    pos = tuple(piece["pos"])
    rot = piece["rotation"]
    new_rot, new_pos, ok = try_rotate_srs(name, pos, rot, direction, board, collides_fn)
    if ok:
        piece["rotation"] = new_rot
        piece["pos"] = [int(new_pos[0]), int(new_pos[1])]
        return True
    return False