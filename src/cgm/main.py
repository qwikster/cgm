# Main module
import os
import sys
import time
import threading
import signal
import queue

from draw import draw_board
from game import lock_piece, collides, rotate
from player import Player
from bag import Bag
from controls import InputHandler

def sigint_handler(sig, frame):
    sigint.set()
    print("\x1b[2j\x1b[Hgoodbye!")

sigint = threading.Event()
lose = threading.Event()
board_lock = threading.Lock()
ROT_SEQ = ["0", "r", "2", "l"]

signal.signal(signal.SIGINT, sigint_handler)

def setup_board(rows, cols):
    board = [[[0] for _ in range(cols)] for _ in range(rows)]
    return board

def _try_lock_piece(player, board, shared, bag, lock_timer, LOCK_DELAY):
    board, cleared, loss = lock_piece(player.active_piece, board, player)
    shared["board"] = board
    
    if loss:
        lose.set()
        return "loss", 0.0
    elif cleared:
        player.active_piece = {}
        return "line_clear", 0.0
    else:
        player.active_piece = {"name": bag.get_piece(), "pos": [3, 0], "rotation": "0"}
        player.hold_lock = False
        player.fall_progress = 0.0
        return "active", 0.0

def input_handler(player, board, action, bag, shared, LOCK_DELAY):
    if not player.active_piece:
        return None, 0.0 # state, lock_timer
    
    piece = player.active_piece
    x, y = piece["pos"]
    
    if action == "pause":
        sigint.set()
        return None, 0.0

    elif action == "move_left":
        piece["pos"][0] -= 1
        if collides(piece, board):
            piece["pos"][0] += 1
    
    elif action == "move_right":
        piece["pos"][0] += 1
        if collides(piece, board):
            piece["pos"][0] -= 1
    
    elif action == "soft_drop":
        piece["pos"][1] += 1
        if collides(piece, board):
            piece["pos"][1] -= 1
            return None, 0.0
        player.soft += 1
    
    elif action == "hard_drop":
        while not collides(piece, board):
            piece["pos"][1] += 1
        piece["pos"][1] -= 1
        return _try_lock_piece(player, board, shared, bag, 0.0, LOCK_DELAY)
    
    elif action == "rotate_cw":
        old_rot = piece["rotation"]
        piece["rotation"] = rotate(old_rot, +1)
        if collides(piece, board):
            piece["rotation"] = old_rot
            
    elif action == "rotate_ccw":
        old_rot = piece["rotation"]
        piece["rotation"] = rotate(old_rot, -1)
        if collides(piece, board):
            piece["rotation"] = old_rot
            
    elif action == "rotate_180":
        old_rot = piece["rotation"]
        piece["rotation"] = rotate(old_rot, 2)
        if collides(piece, board):
            piece["rotation"] = old_rot
            
    elif action == "hold":
        if player.hold_lock:
            return None, 0.0
        old = player.hold_piece
        player.hold_piece = player.active_piece["name"]
        if not old:
            player.active_piece = {"name": bag.get_piece(), "pos": [3, 0], "rotation": "0"}
            player.fall_progress = 0.0
        else:
            player.active_piece = {"name": old, "pos": [3, 0], "rotation": "0"}
            player.fall_progress = 0.0
        player.hold_lock = True
    
    return None, 0.0
    
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
            print("\x1b[H\x1b[31mRunning below 60fps!! Performance will be degraded\x1b[0m")

def game_loop(shared, player, bag, inputs, fps):
    from config import ARE_FRAMES, LINE_CLEAR_FRAMES, LOCK_DELAY_FRAMES, MAX_LOCK_RESETS
    FRAME = 1 / fps
    
    LOCK_DELAY = LOCK_DELAY_FRAMES * FRAME
    ARE_DELAY = ARE_FRAMES * FRAME
    LINE_CLEAR_DELAY = LINE_CLEAR_FRAMES * FRAME
    
    state = "spawn"
    lock_timer = 0.0
    lock_resets = 0
    phase_timer = 0.0
    fall_time = time.perf_counter()
    
    player.active_piece = {"name": bag.get_piece(), "pos": [3, 0], "rotation": "0"}
    
    while not sigint.is_set():
        now = time.perf_counter()
        elapsed = now-fall_time
        fall_interval = player.get_grav() # s/cell
        
        with board_lock:
            board = shared["board"]
            
            try:
                action = inputs.queue.get_nowait()
                new_state, lock_timer = input_handler(player, board, action, bag, shared, LOCK_DELAY)
                if new_state in ("line_clear", "are", "loss"):
                    state = new_state
                    phase_timer = 0.0
                    player.hold_lock = False
                    
                    if state == "active":
                        fall_time = now
                    continue
            except queue.Empty:
                pass
            
            player.check_grade()
            
            if state == "active": # ADD HIGH SPEED GRAVITY
                if elapsed >= fall_interval:
                    fall_time = now
                    piece = player.active_piece
                    piece["pos"][1] += 1
                    
                    if collides(piece, board):
                        piece["pos"][1] -= 1
                        lock_timer += fall_interval
                        if lock_timer >= LOCK_DELAY:
                            state, lock_timer = _try_lock_piece(player, board, shared, bag, lock_timer, LOCK_DELAY)
                            if state == "loss":
                                return
                            player.hold_lock = False
                            phase_timer = 0.0
                            fall_time = now
                            continue
                    else:
                        lock_timer = 0.0
                        lock_resets = 0
            
            elif state == "line_clear":
                phase_timer += FRAME
                if phase_timer >= LINE_CLEAR_DELAY:
                    state = "are"
                    phase_timer = 0.0
                
            elif state == "are":
                phase_timer += FRAME
                if phase_timer >= ARE_DELAY:
                    player.active_piece = {"name": bag.get_piece(), "pos": [3, 0], "rotation": "0"}
                    state = "active"
                    fall_time = time.perf_counter()
                
            elif state == "spawn":
                player.active_piece = {"name": bag.get_piece(), "pos": [3, 0], "rotation": "0"} # and again
                fall_time = now
                state = "active"
                
        time.sleep(FRAME)
    inputs.stop()

def entry():
    player = Player()
    bag = Bag(preview_size=5)
    shared = { "board": setup_board(22, 10) }
    
    inputs = InputHandler()
    inputs.start()
    
    try:
        render_thread = threading.Thread(target=render_loop, args=(shared, player, bag, 60))
        render_thread.start()
        
        game_thread = threading.Thread(target=game_loop, args=(shared, player, bag, inputs, 60))
        game_thread.start()
        
    except KeyboardInterrupt:
        sigint.set()
        inputs.stop()
        game_thread.join()
        render_thread.join()

if __name__ == "__main__":    
    try:
        os.system("clear")
        entry()
    except KeyboardInterrupt:
        sys.exit(0)