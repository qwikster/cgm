# das/arr with actual keydown *requires a pygame window

import pygame
import threading
import queue
import time
import sys

from cetragm.config import DAS_MS, ARR_MS, SOFT_ARR_MS, KEYMAP

class InputHandler:
    def __init__(self, keymap=None, window_size = (300, 300), hidden = False):
        self.queue = queue.Queue()
        self._thread = None
        self._running = False
        self._pressed = set() # keys to ARR
        self._repeat_state = {} # wait for das or repeat until x
        self.keymap = keymap or KEYMAP
        self.window_size = window_size
        self.hidden = hidden
        
        self.DAS = DAS_MS / 1000.0
        self.ARR = ARR_MS / 1000.0
        self.SOFT_ARR = SOFT_ARR_MS / 100.0
        
        self._movement_keys = {k for k, v in self.keymap.items() if v in ("move_left", "move_right")} # what to apply DAS to
        
    def start(self):
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
    
    def stop(self):
        self._running = False
        try:
            pygame.event.post(pygame.event.Event(pygame.QUIT)) # try to exit gracefully
        except Exception:
            pass
        
        if self.thread is not None: # if that doesn't work bonk it
            self._thread.join(timeout= 0.25)
    
    def movement_pressed(self):
        return any(k in self._pressed for k in self._movement_keys)
    
    def _enqueue(self, action):
        try:
            self.queue.put_nowait(action)
        except Exception:
            pass
        
    def _run(self):
        pygame.init()
        flags = 0   
        