# DRAW.PY
# Module for drawing to the screen (stdout tomfuckery time!!!)
import sys
import shutil
from pieces import pieces

BLOCK = "██"
EMPTY = "  "

def validate_board(board): # check for dimensions in case game loop fucked me
    if len(board) != 22:
        raise ValueError(f"Board has {len(board)} rows")
    widths = {len(r) for r in board}
    if widths != {10}:
        raise ValueError(f"Board has rows not 10 wide - {widths}")

def format_time(ms: int) -> str: # for TGM style timer at the bottom
    minutes = (ms // 1000) // 60 # Shame i can't make it obnoxiously big
    seconds = (ms // 1000) % 60  # or can i...? *mice on venus*
    hundredths = (ms % 1000) // 10
    return f"{minutes:02}:{seconds:02}:{hundredths:02}"

def color_block(piece_id: str | None): # in ["i", "z", "s", "l", "j", "t", "o"]
    if (not piece_id) or (piece_id not in pieces):
        return EMPTY
    r, g, b = pieces[piece_id]["rgb"]
    return f"\x1b[38;2;{r};{g};{b}m{BLOCK}\x1b[0m" # color, block ascii, reset

# public
def draw_board(board,                              # from game.py. Board: 2d list. Entries: [0] or [1, "t"]. 
               active_piece = None,                # {"name": "t", "pos": (0, 0), "rotation": "0"}
               score: int = 0, grade: str = "9",   # score is used to calculate TGM grade (9 -> 1 -> S1 -> S9 -> Gm)
               time_ms: int = 0,                   # BIG FLASHING TIMER
               lines: int = 0, line_goal: int = 0, # for gravity level up with timer
               hold: str | None = None,            # hold = "t"
               next_queue: list[str] | None = None # list of 5 pieces like ["t", "i", "z", "s", "o"] (7-bag)
               ):
    pass