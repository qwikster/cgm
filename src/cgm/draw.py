# Module for drawing to the screen (stdout tomfuckery time!!!)
import sys
import shutil
from pieces import pieces

BLOCK = "██"
EMPTY = "  "
RESET = "\x1b[0m"
CLEAR = "\033[2J\033[H"

def get_cells(piece): # {"name": "i", "pos": (0, 0), "rotation": "0"}
    # Gets the cells in a falling piece with its current rotation and coordinates on the board
    shape = pieces[piece["name"]]["rotations"][piece["rotation"]]
    px, py = piece["pos"]
    cells = [(px + x, py + y)
             for y, row in enumerate(shape)
             for x, val in enumerate(row) if val]
    return cells

def get_color(piece_id: str | None): # ["i", "z", "s", "l", "j", "t", "o"]
    if not piece_id:
        return EMPTY
    r, g, b = pieces[piece_id]["rgb"]
    return f"\x1b[38;2;{r};{g};{b}m{BLOCK}{RESET}" # color, block ascii, reset

def collides(piece, board):
    # Check if the piece is colliding (will want to write a new one for srs.py)
    for (x, y) in get_cells(piece):
        if x < 0 or x >= len(board[0]) or y >= len(board):
            return True
        if y >= 0 and board[y][x][0]:
            return True
    return False
