# das/arr with actual keydown *requires a pygame window

import pygame
import threading
import queue
import time
import sys
import os

from cetragm.config import DAS_MS, ARR_MS, SOFT_ARR_MS, KEYMAP

class InputHandler:
    def __init__(self, keymap=None, window_size = (200, 100), hidden = True):
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
        
        if self._thread is not None: # if that doesn't work bonk it
            self._thread.join(timeout= 0.25)
    
    def movement_pressed(self):
        return any(k in self._pressed for k in self._movement_keys)
    
    def _enqueue(self, action):
        try:
            self.queue.put_nowait(action)
        except Exception:
            pass
        
    def _run(self):
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (20, 20)
        
        pygame.init()
        flags = 0   
        if self.hidden:
            flags = pygame.NOFRAME
        try:
            screen = pygame.display.set_mode(self.window_size, flags)
        except Exception:
            screen = pygame.display.set_mode((320, 64))
        pygame.display.set_caption("Focus for CGM input")
        
        try: # attempt to auto-grab input, may not work on hyprland etc
            pygame.event.set_blocked(None)
            pygame.event.set_allowed([pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT])
            pygame.event.set_keyboard_grab(True)
            pygame.key.set_repeat() # turn off pygame native ARR
        except Exception:
            pass
        
        font = None
        try:
            font = pygame.font.Font(None, 18)
        except Exception:
            pass
        
        def _draw_message():
            screen.fill((0, 100, 80))
            lines = [
                "this window gets input for CGM!",
                "can't do it via terminal because",
                "there's no press/release input.",
                "press ESC to close this window,",
                "and focus it to play!",
                "-@qwik (ps rate 5 stars)"
            ]
            if font:
                y = 6
                for ln in lines:
                    surf = font.render(ln, True, (220, 220, 220))
                    screen.blit(surf, (8, y))
                    y += surf.get_height() + 2
            else:
                pass
            pygame.display.flip()
        
        _draw_message()