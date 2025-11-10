# Main module
import os
import sys
import time
import threading
import signal
import queue

from cetragm.draw import draw_board
from cetragm.game import lock_piece, collides, rotate
from cetragm.player import Player
from cetragm.bag import Bag
from cetragm.controls import InputHandler

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

def lock_and_are(player, board, shared):
    board, cleared, loss = lock_piece(player.active_piece, board, player)
    shared["board"] = board
    
    if loss:
        lose.set()
        return "loss", 0.0
    
    player.active_piece = {}
    player.fall_progress = 0.0
    player.hold_lock = False
    player.soft = 0
    
    if cleared:
        return "line_clear", 0.0
    else:
        return "are", 0.0
    
    
def lock_now(player, board, shared, bag):
    try:
        board, cleared, loss = lock_piece(player.active_piece, board, player)
    except ValueError:
        lose.set()
        return "loss"
    shared["board"] = board
    
    if loss:
        lose.set()
        return "loss"
    elif cleared:
        player.active_piece = {}
        player.fall_progress = 0.0
        player.soft = 0
        return "line_clear"
    else:
        player.active_piece = {"name": bag.get_piece(), "pos": [3, 0], "rotation": "0"}
        player.fall_progress = 0.0
        player.soft = 0
        player.hold_lock = False
        return "active"

def input_handler(player, board, action, bag, shared, LOCK_DELAY, FRAME):
    if not player.active_piece:
        return None
    
    piece = player.active_piece
    x, y = piece["pos"]
    
    if action == "pause":
        sigint.set()
        return None

    elif action == "move_left":
        piece["pos"][0] -= 1
        if collides(piece, board):
            piece["pos"][0] += 1
        return None
    
    elif action == "move_right":
        piece["pos"][0] += 1
        if collides(piece, board):
            piece["pos"][0] -= 1
        return None
    
    elif action == "soft_drop":
        piece["pos"][1] += 1
        if collides(piece, board):
            piece["pos"][1] -= 1
            return "ground"
        player.soft += 1
        return None
    
    elif action == "hard_drop":
        while not collides(piece, board):
            piece["pos"][1] += 1
        piece["pos"][1] -= 1
        player.soft += 4
        return lock_now(player, board, shared, bag)
    
    elif action == "rotate_cw":
        old_rot = piece["rotation"]
        piece["rotation"] = rotate(old_rot, +1)
        if collides(piece, board):
            piece["rotation"] = old_rot
        return None
            
    elif action == "rotate_ccw":
        old_rot = piece["rotation"]
        piece["rotation"] = rotate(old_rot, -1)
        if collides(piece, board):
            piece["rotation"] = old_rot
        return None
            
    elif action == "rotate_180":
        old_rot = piece["rotation"]
        piece["rotation"] = rotate(old_rot, 2)
        if collides(piece, board):
            piece["rotation"] = old_rot
        return None
            
    elif action == "hold":
        if player.hold_lock:
            return None
        old = player.hold_piece
        player.hold_piece = player.active_piece["name"]
        if not old:
            player.active_piece = {"name": bag.get_piece(), "pos": [3, 0], "rotation": "0"}
            player.fall_progress = 0.0
        else:
            player.active_piece = {"name": old, "pos": [3, 0], "rotation": "0"}
            player.fall_progress = 0.0
        player.hold_lock = True
        return None
    
    return None
    
def render_loop(shared, player, bag, fps):
    frame_time = 1.0 / fps
    while not sigint.is_set():
        if lose.is_set():
            sigint.set()
        with board_lock:
            board = shared["board"]
        
        start = time.perf_counter()
        player.upd_time()
        print("\x1b[H\x1b[2J")
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
    from cetragm.config import ARE_FRAMES, LINE_CLEAR_FRAMES, LOCK_DELAY_FRAMES
    FRAME = 1.0 / fps
    
    LOCK_DELAY = LOCK_DELAY_FRAMES * FRAME
    ARE_DELAY = ARE_FRAMES * FRAME
    LINE_CLEAR_DELAY = LINE_CLEAR_FRAMES * FRAME
    
    state = "spawn"
    lock_timer = 0.0
    phase_timer = 0.0
    
    last_time = time.perf_counter()
    
    if not hasattr(player, "fall_progress"):
        player.fall_progress = 0.0
    
    while not sigint.is_set():
        now = time.perf_counter()
        dt = now - last_time
        last_time = now
        if dt > 0.1:
            dt = 0.1
        
        with board_lock:
            board = shared["board"]
            while True:
                try:
                    action = inputs.queue.get_nowait()
                except queue.Empty:
                    break
                
                new_state = input_handler(player, board, action, bag, shared, LOCK_DELAY, FRAME)
                
                if new_state == "ground":
                    lock_timer += dt
                    if lock_timer >= LOCK_DELAY:
                        state, lock_timer = lock_and_are(player, board, shared)
                        if state == "loss":
                            return
                        phase_timer = 0.0
                    continue
                
                if new_state in ("line_clear", "are", "loss"):
                    state = new_state
                    phase_timer = 0.0
                    player.hold_lock = False
                    if state == "active":
                        player.fall_progess = 0.0
                    break
            
            player.check_grade()
            
            # gravity
            if state == "active":
                g_units = player.get_grav()
                cells_per_frame = g_units / 256.0
                cells_per_second = cells_per_frame * fps
                player.fall_progress += cells_per_second * dt
                cells_to_fall = int(player.fall_progress)
                
                if cells_to_fall > 0:
                    player.fall_progress -= cells_to_fall
                    piece = player.active_piece
                    
                    for _ in range(cells_to_fall):
                        piece["pos"][1] += 1
                        if collides(piece, board):
                            piece["pos"][1] -= 1
                            lock_timer += dt
                            if lock_timer >= LOCK_DELAY:
                                state, lock_timer = lock_and_are(player, board, shared)
                                if state == "loss":
                                    return
                                phase_timer = 0.0
                            break
                    else:
                        lock_timer = 0.0
                
                piece = player.active_piece
                temp_pos = piece["pos"].copy()
                temp_pos[1] += 1
                if collides({"name": piece["name"], "pos": temp_pos, "rotation": piece["rotation"]}, board):
                    lock_timer += dt
                if lock_timer >= LOCK_DELAY:
                    state, lock_timer = lock_and_are(player, board, shared)
                    if state == "loss":
                        return
                    phase_timer = 0.0
            
            # pause after line clear
            elif state == "line_clear":
                phase_timer += dt
                if phase_timer >= LINE_CLEAR_DELAY:
                    state = "are"
                    phase_timer = 0.0
            
            # pause after a piece locking without soft drop
            elif state == "are":
                phase_timer += dt
                if phase_timer >= ARE_DELAY:
                    player.active_piece = {"name": bag.get_piece(), "pos": [3, 0], "rotation": "0"}
                    player.fall_progress = 0.0
                    lock_timer = 0.0
                    state = "active"
            
            # first piece
            elif state == "spawn":
                player.active_piece = {"name": bag.get_piece(), "pos": [3, 0], "rotation": "0"} # and again
                player.fall_progress = 0.0
                lock_timer = 0.0
                state = "active"
        
        elapsed_loop = time.perf_counter() - now
        to_sleep = FRAME - elapsed_loop
        time.sleep(to_sleep if to_sleep > 0 else 0)
        
    # sigint
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