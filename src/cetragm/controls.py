# das/arr with actual keydown *requires a pygame window

import pygame
import threading
import queue
import time
import sys
import os

from cetragm.config import DAS_MS, ARR_MS, SDF, KEYMAP

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
        self.SDF = SDF / 1000.0
        
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
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (30, 30)
        
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
        
        last_time = time.monotonic()
        while self._running:
            now = time.monotonic()
            dt = now - last_time
            last_time = now
            
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    self._enqueue("pause")
                    self._running = False
                    break
                if ev.type == pygame.KEYDOWN:
                    key = ev.key
                    was_down = key in self._pressed
                    self._pressed.add(key)
                    
                    self._repeat_state[key] = {
                        "das_until": now + self.DAS,
                        "next_repeat": now + self.DAS + self.ARR
                    }
                    
                    action = self.keymap.get(key)
                    if action is None:
                        continue
                    
                    self._enqueue(action)
                
                elif ev.type == pygame.KEYUP:
                    key = ev.key
                    if key in self._pressed:
                        self._pressed.remove(key)
                    if key in self._repeat_state:
                        del self._repeat_state[key]
                        
            now = time.monotonic()
            for key, st in list(self._repeat_state.items()):
                action = self.keymap.get(key)
                if action not in ("move_left", "move_right"):
                    continue
                
                if now >= st["das_until"]:
                    if now >= st["next_repeat"]:
                        self._enqueue(action)
                        st["next_repeat"] = now + self.ARR
                        self._repeat_state[key] = st
                        
            sd_keys = [k for k in self._pressed if self.keymap.get(k) == "soft_drop"]
            if sd_keys:
                key = "__soft_drop__"
                st = self._repeat_state.get(key)
                
                if st is None:
                    self._enqueue("soft_drop")
                    self._repeat_state[key] = {
                        "next_repeat": now + self.SDF
                    }
                else:
                    if now >= st["next_repeat"]:
                        self._enqueue("soft_drop")
                        st["next_repeat"] = now + self.SDF
            else:
                self._repeat_state.pop("__soft_drop__", None)
                    
            time.sleep(0.01)
        
        try:
            pygame.event.set_keyboard_grab(False)
        except Exception:
            pass
        try:
            pygame.quit()
        except Exception:
            pass