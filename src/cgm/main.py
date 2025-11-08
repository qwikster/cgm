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
lose = threading.Event()
board_lock = threading.Lock()

def sigint_handler(sig, frame):
    sigint.set()
    print("goodbye!")
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

def setup_board(rows, cols):
    board = [[[0] for _ in range(cols)] for _ in range(rows)]
    return board

def render_loop(shared, player, bag, fps):
    frame_time = 1.0 / fps
    while not sigint.is_set():
        if lose.is_set():
            return
        
        with board_lock:
            board = shared["board"]
        
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
            print("\x1b[H\x1b[31mRunning below 60fps!! Performance will be degraded")

def game_loop(shared, player, bag, fps):
    gravity_timer = 0
    fall_interval = 0.2 # TODO: make dynamic
    fall_time = time.perf_counter()
    
    player.active_piece = {"name": bag.get_piece(), "pos": [3, 0], "rotation": "0"}
    
    while not sigint.is_set():
        now = time.perf_counter()
        elapsed = now-fall_time
        
        if elapsed >= fall_interval:
            fall_time = now
            with board_lock:
                board = shared["board"]
                player.active_piece["pos"][1] += 1
                
                if collides(player.active_piece, board):
                    player.active_piece["pos"][1] -= 1 # move this back if it starts to cause issues
                    board, cleared = lock_piece(player.active_piece, board, player)
                    shared["board"] = board
                    
                    if cleared:
                        lose.set()
                        return
                    
                    player.level += 1 # one piece placed
                    player.active_piece = {"name": bag.get_piece(), "pos": [3, 0], "rotation": "0"} # and again

        time.sleep(0.01)


def entry():
    player = Player()
    bag = Bag(preview_size=5)
    shared = { "board": setup_board(22, 10) }
    
    try:
        render_thread = threading.Thread(target=render_loop, args=(shared, player, bag, 60))
        render_thread.start()
        
        game_thread = threading.Thread(target=game_loop, args=(shared, player, bag, 60))
        game_thread.start()
    except KeyboardInterrupt:
        sigint.set()

if __name__ == "__main__":    
    try:
        os.system("clear")
        entry()
    except KeyboardInterrupt:
        sys.exit(0)