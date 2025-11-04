# core logic like lock, gravity, and scoring
from pieces import pieces

def get_cells(piece): # {"name": "i", "pos": (0, 0), "rotation": "0"}
    # Gets the cells in a falling piece with its current rotation and coordinates on the board
    shape = pieces[piece["name"]]["rotations"][piece["rotation"]]
    px, py = piece["pos"]
    cells = [(px + x, py + y)
             for y, row in enumerate(shape)
             for x, val in enumerate(row) if val]
    return cells

def collides(piece, board):
    # Check if the piece is colliding (will want to write a new one for srs.py)
    for (x, y) in get_cells(piece):
        if x < 0 or x >= len(board[0]) or y >= len(board):
            return True
        if y >= 0 and board[y][x][0]:
            return True
    return False