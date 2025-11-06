# Main module
import os
import sys
from tables import pieces, grades, thresholds
from draw import draw_board
from game import lock_piece, collides
from player import Player
from bag import Bag
import time
import threading
import signal

sigint = threading.Event()

def sigint_handler(sig, frame):
    sigint.set()
    print("goodbye!")
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

def setup_board(rows, cols):
    board = [[[0] for _ in range(cols)] for _ in range(rows)]
    return board

def render_loop(board, player, bag, fps):
    frame_time = 1.0 / fps
    while not sigint.is_set():
        start = time.perf_counter()
        player.upd_time()
        draw_board(
            board,
            player.active_piece,
            player.score,
            player.grade,
            player.time_ms,
            player.level,
            player.line_goal,
            player.hold_piece,
            bag.get_preview()
        ) # got damn
        elapsed = time.perf_counter() - start
        sleep_time = frame_time - elapsed
        if sleep_time > 0:
            time.sleep(sleep_time)
        else:
            raise TimeoutError("running under 60fps!")

def entry():
    player = Player()
    bag = Bag(preview_size=5)
    board = setup_board(22, 10)
    try:
        render_thread = threading.Thread(target=render_loop, args=(board, player, bag, 60))
        render_thread.start()
    except KeyboardInterrupt:
        sigint.set()
    
    while(1):
        player.active_piece = {"name": bag.get_piece(), "pos": [3, 0], "rotation": "0"}
        input()

        last_y = player.active_piece["pos"][1]
        
        for i in range(0, 22): # can use this for a shadow piece later and it works for hard drop logic :)
            player.active_piece["pos"][1] = i
            if collides(player.active_piece, board):
                player.active_piece["pos"][1] = last_y
                board, cleared = lock_piece(player.active_piece, board)
                break
            last_y = i

if __name__ == "__main__":    
    try:
        os.system("clear")
        entry()
    except KeyboardInterrupt:
        sys.exit(0)