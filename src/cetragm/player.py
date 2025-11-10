# module containing the Player class and its functions

import time
from cetragm.tables import thresholds, gravity

class Player:
    def __init__(self):
        self.score = 0
        self.time_ms = 0
        self.start_time = time.perf_counter()
        self.grade = "9"
        self.level = 0
        self.line_goal = 100
        self.hold_piece = ""
        self.active_piece = {}
        
        # checks for midgame
        self.can_gm = True
        self.met_gm_condition_300 = False
        self.met_gm_condition_500 = False
        self.met_gm_condition_999 = False
        
        self.combo = 0
        self.soft = 0
        self.hold_lock = False
        self.lock_resets = 0
        self.fall_progress = 0.0
    
    def upd_time(self):
        self.time_ms = int((time.perf_counter() - self.start_time) * 1000)    

    def check_grade(self):
        self.upd_time()
        # checking for GM eligibility (called every piece, so it'll be up to date)
        if not self.met_gm_condition_300 and self.level >= 300:
            if self.time_ms <= 225000 and self.score >= 12000 and self.can_gm: # 4m 15s 
                self.met_gm_condition_300 = True
            else:
                self.can_gm = False
                
        if not self.met_gm_condition_500 and self.level >= 500:
            if self.time_ms <= 450000 and self.score >= 40000 and self.can_gm: # 7m 30s 
                self.met_gm_condition_500 = True
            else:
                self.can_gm = False
            
        for name, val in thresholds.items(): # actually set grade
            if self.score >= val:
                if not self.grade == "Gm":
                    self.grade = name
            else:
                break
    
    def check_gm(self):
        self.upd_time()
        if not self.can_gm:
            return False
        
        if not (self.met_gm_condition_300 and self.met_gm_condition_500):
            return False
        
        if self.time_ms <= 810000 and self.score >= 126000:
            self.met_gm_condition_999 = True
            self.grade = "Gm"
            return True        
        return False
    
    def get_grav(self):
        keys = sorted(gravity.keys())
        current_g = gravity[0]
        for k in keys:
            if self.level >= k:
                current_g = gravity[k]
            else: 
                break
            
        if current_g <= 0:
            return float('inf')
        return current_g