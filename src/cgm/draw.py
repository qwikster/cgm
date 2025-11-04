# Module for drawing to the screen (stdout tomfuckery time!!!)
import sys
from pieces import pieces

BLOCK = "██"
EMPTY = "  "
RESET = "\x1b[0m"
CLEAR = "\033[2J\033[H"

def draw_board(board, active_piece=None):
    height = len(board)
    width = len(board[0])
    buffer = []
    
    for y in range(height):
        row = []
        for x in range(width):
            cell = board[y][x]
            if cell[0]:
                row.append(cell[1] + BLOCK)
            else:
                row.append(EMPTY)
        buffer.append("".join(row))
    
    if active_piece:
        for (x, y) in active_piece["cells"]:
            if 0 <= y < (height * 2) and 0 <= x < (width * 2):
                line = list(buffer[y])
                line[x] = BLOCK
                buffer[y] = "".join(line)
    
    sys.stdout.write("\n".join(buffer) + "\n")
    sys.stdout.flush()