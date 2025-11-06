# Main module
import os
import sys
from pieces import pieces, grades
from draw import draw_board
import time

def entry():
    pass

def setup_board(rows, cols):
    board = [[[0] for _ in range(cols)] for _ in range(rows)]
    return board

if __name__ == "__main__":
    entry()
    
    try:
        # entry()
        os.system("clear")
        board = setup_board(22, 10)
        board[21][0] = ["0", "t"]
        print(board)
        start = time.perf_counter()
        for _ in range(40):
            for j in ["9", "8", "7", "6", "5", "4", "3", "2", "1", "S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "Gm"]:
                piece = {"name": "t", "pos": (3, 0), "rotation": "0"}
                draw_board(board, piece, 1696969, j, 480000, 123, 999, "t", ["j", "l", "s", "z", "o"])
                time.sleep(0.3)
        end = time.perf_counter()
        print(f"Took {end - start} seconds")
    except KeyboardInterrupt:
        sys.exit(0)