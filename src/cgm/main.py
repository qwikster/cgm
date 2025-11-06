# Main module
import os
import sys
from tables import pieces, grades, thresholds
from draw import draw_board
from game import lock_piece, get_next
from player import Player
import time
import threading
        
def render_loop(board, player, next_queue):
    draw_board(board, player.active_piece, )

def setup_board(rows, cols):
    board = [[[0] for _ in range(cols)] for _ in range(rows)]
    return board

def entry():
    player = Player()
    board = setup_board(22, 10)
    next_queue = get_next(5)
    
    player.active_piece = {"name": "t", "pos": (3, 0), "rotation": "0"}
    draw_board(board, player.active_piece, player.score, player.grade, player.time_ms, player.level, player.line_goal, player.hold_piece, next_queue)
    input()
    
    render_thread = threading.Thread(target=render_loop, args=(board, player, next_queue))
    render_thread.start()

if __name__ == "__main__":
    entry()
    
    try:
        # entry()
        os.system("clear")
        
        start = time.perf_counter()
        for _ in range(40):
            for j in ["9", "8", "7", "6", "5", "4", "3", "2", "1", "S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "Gm"]:
                piece = {"name": "t", "pos": (3, 20), "rotation": "0"}
                board, lost = lock_piece(piece, board)
                if lost:
                    sys.exit(0)
                piece = {"name": "t", "pos": (3, 0), "rotation": "0"}
                draw_board(board, piece, 1696969, j, 480000, 123, 999, "t", ["j", "l", "s", "z", "o"])
                time.sleep(0.3)
        end = time.perf_counter()
        print(f"Took {end - start} seconds")
    except KeyboardInterrupt:
        sys.exit(0)