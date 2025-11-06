# Main module
import os
import sys
from pieces import pieces, grades, thresholds
from draw import draw_board
from game import lock_piece
import time

class Player:
    def __init__(self):
        self.score = 0
        self.time_ms = 0
        self.start_time = time.perf_counter()
        self.grade = "9"
        self.level = 0
        self.line_goal = 0
        self.hold_piece = ""
        self.active_piece = {}
        
        # checks for midgame
        self.can_gm = True
        self.met_gm_condition_300 = False
        self.met_gm_condition_500 = False
        self.met_gm_condition_999 = False
    
    def check_grade(self):
        self.upd_time()
        
        # checking for GM eligibility (called every piece, so it'll be up to date)
        if not self.met_gm_condition_300 and self.level >= 300:
            if self.time_ms <= 225000 and self.can_gm and self.score >= 12000: # 4m 15s 
                self.met_gm_condition_300 = True
            else:
                self.can_gm = False
                
        if not self.met_gm_condition_500 and self.level >= 500:
            if self.time_ms <= 450000 and self.can_gm and self.score >= 40000: # 7m 30s 
                self.met_gm_condition_500 = True
            else:
                self.can_gm = False
            
        for name, val in thresholds: # actually set grade
            if name == "Gm":
                if self.level >= 999:
                    self.grade = name # GAME END
                else:
                    self.grade = "S9"
                    return
            if self.score >= val:
                self.grade = name
            else:
                break
    
    def upd_time(self):
        self.time_ms = int((time.perf_counter() - self.start_time) * 1000)
        
def render_loop(board, player, next_queue):
    pass

def setup_board(rows, cols):
    board = [[[0] for _ in range(cols)] for _ in range(rows)]
    return board

def entry():
    player = Player()
    time.sleep(3)
    player.upd_time()
    print(player.time_ms)
    input()

if __name__ == "__main__":
    entry()
    
    try:
        # entry()
        os.system("clear")
        board = setup_board(22, 10)
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