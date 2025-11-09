# Module for binding and rebinding controls as well as taking input (threaded)
# DAS/ARR logic

from config import controls
import termios
import tty
import sys
import os
import threading
import queue

class InputHandler:
    def __init__(self):
        self.queue = queue.Queue()
        self.stop_flag = threading.Event()
        self.is_windows = os.name == "nt"
        if not self.is_windows:
            self.fd = sys.stdin.fileno()
            self.old_settings = termios.tcgetattr(self.fd)
            
    def start(self):
        self.thread = threading.Thread(target=self._poll_loop, daemon=True)
        self.thread.start()
    
    def stop(self):
        self.stop_flag.set()
        if not self.is_windows:
            termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)
            
    def _poll_loop(self):
        if self.is_windows:
            self._poll_windows
        else:
            self._poll_linux()
    
    def _poll_windows(self):
        import msvcrt
        while not self.stop_flag.is_set():
            if msvcrt.kbhit():
                ch = msvcrt.getwch()
                self._process_key(ch)
            else:
                threading.Event().wait(0.01)
    
    def _poll_linux(self):
        tty.setcbreak(self.fd)
        while not self.stop_flag.is_set():
            r, _, _ = select.select([sys.stdin], [], [], 0.01)
            if r:
                ch = sys.stdin.read(1)
                if ch == "\x1b":
                    print("recv escape code")
                    seq = ch + sys.stdin.read(2)
                    self._process_key(seq)
                else:
                    self._process_key(ch)
                    
    def _process_key(self, key):
        print("key", key)
        for action, binds in controls.items():
            if key in binds:
                self.queue.put(action)
                break