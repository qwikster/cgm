# core logic like lock, gravity, and scoring
from cetragm.tables import pieces, ROT_180, ROT_CCW, ROT_CW
import math

def get_cells(piece): # {"name": "i", "pos": (0, 0), "rotation": "0"}
    # Gets the cells in a falling piece with its current rotation and coordinates on the board
    shape = pieces[piece["name"]]["rotations"][piece["rotation"]]
    px, py = piece["pos"]
    cells = [(px + x, py + y)
             for y, row in enumerate(shape)
             for x, val in enumerate(row) if val]
    return cells

def collides(piece, board):
    for (x, y) in get_cells(piece):
        if x < 0 or x >= len(board[0]) or y >= len(board):
            return True
        if y >= 0 and board[y][x][0]:
            return True
    return False

def lock_piece(piece, board, player):
    if collides(piece, board):
        if piece["pos"][1] == 0:
            return board, 0, True
        else:
            raise ValueError("Tried to lock outside the board or lock piece over another piece (and it wasn't a loss)")
    for i in get_cells(piece):
        board[i[1]][i[0]] = [1, piece["name"]]
        
    board, cleared = clear_lines(board)
    board_empty = all(cell[0] for row in board for cell in row)
    soft = player.soft # TODO: ADD SOFT, OR SOFT DROP CALC
    
    if board_empty:
        player.score += 2500
    
    score_gain, player.combo = get_score(player.level, cleared, player.combo, board_empty, soft)
    player.score += score_gain
    
    update_level(player, cleared)

    return board, cleared, False

def clear_lines(board):
    new_board = []
    cleared = 0
    
    for row in board:
        if all(cell[0] for cell in row):
            cleared += 1
        else:
            new_board.append(row)
            
    for _ in range(cleared):
        new_board.insert(0, [[0] for _ in range(len(board[0]))])
    
    return new_board, cleared

def get_score(level, lines_cleared, combo, board_empty, soft):
    if lines_cleared == 0:
        return 0, 1 # 0 score, reset combo
    
    combo = combo + (2 * lines_cleared) - 2 if combo > 1 else (2 * lines_cleared) - 1
    if combo <1:
        combo = 1
    bravo = 4 if board_empty else 1
    
    score = (math.ceil((level + lines_cleared) / 4) + soft) * lines_cleared * combo * bravo
    return score, combo

def update_level(player, cleared):
    if player.level >= 999:
        player.line_goal = 999
        player.level = 999
        return
    
    old_level = player.level
    temp = old_level + 1 + int(cleared)
    temp = 999 if temp > 999 else temp
        
    old_sect = old_level // 100
    new_sect = temp // 100
    
    if new_sect > old_sect and cleared == 0:
        temp = min(temp, (old_sect * 100 + 99))
        
    player.level = min(temp, 999)
    
    if player.level > 900:
        player.line_goal = 999
    else:
        player.line_goal = ((player.level // 100) + 1) * 100
        
def rotate(current, direction):
    if direction == +1:
        return ROT_CW[current]
    elif direction == -1:
        return ROT_CCW[current]
    elif direction == 2:
        return ROT_180[current]
    raise ValueError("direction should be -1, +1, or 2.")
    return current