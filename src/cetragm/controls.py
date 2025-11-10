# Module for binding and rebinding controls as well as taking input (threaded)
# DAS/ARR logic

from cetragm.config import controls
import termios
import tty
import os
import threading
import queue
import select
import sys

class InputHandler:
    def __init__(self):
        self.queue = queue.Queue()
        self.stop_flag = threading.Event()
        self.is_windows = os.name == "nt"
        self.fd = None
        self.old_settings = None
            
    def start(self):
        self.thread = threading.Thread(target=self._poll_loop, daemon=True)
        self.thread.start()
    
    def stop(self):
        self.stop_flag.set()
        if self.is_windows:
            return
        if self.fd is not None and self.old_settings is not None:
            try:
                termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)
            except termios.error:
                pass
    
    def _poll_loop(self):
        if self.is_windows:
            self._poll_windows()
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
        try:
            self.fd = os.open("/dev/tty", os.O_RDONLY)
        except OSError:
            self.fd = sys.stdin.fileno()
            
        if not os.isatty(self.fd):
            print("not a tty!! failing out", file=sys.stderr)
            return
        
        self.old_settings = termios.tcgetattr(self.fd)
        tty.setcbreak(self.fd)
        
        try:
            while not self.stop_flag.is_set():
                r, _, _ = select.select([self.fd], [], [], 0.02)
                if not r:
                    continue
                
                try:
                    ch = os.read(self.fd, 1).decode(errors="ignore")
                except OSError as e:
                    print("OSerror:", e, file=sys.stderr)
                    break
                
                if not ch:
                    continue
                
                if ch == "\x1b":
                    seq = ch
                    while select.select([self.fd], [], [], 0.001)[0]:
                        seq += os.read(self.fd, 1).decode(errors="ignore")
                    key = seq
                else:
                    key = ch
                self._process_key(key)
        finally:
            if self.old_settings is not None and os.isatty(self.fd):
                try:
                    termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)
                except termios.error:
                    pass
            if self.fd not in (None, sys.stdin.fileno()):
                try:
                    os.close(self.fd)
                except OSError as e:
                    print(e, file=sys.stderr)
          
    def _process_key(self, key):
        for action, binds in controls.items():
            if key in binds:
                self.queue.put(action)
                break