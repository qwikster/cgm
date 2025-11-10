# Module for configuration the user probably wouldn't see, keymaps and gravity etc

MAX_LOCK_RESETS = 15
ARE_FRAMES = 20
LINE_CLEAR_FRAMES = 20
LOCK_DELAY_FRAMES = 30

controls = {
    "move_left":  ["a", "j", "\x1b[D"], # left arrow
    "move_right": ["d", "l", "\x1b[C"], # right
    "soft_drop":  ["s", "k", "\x1b[B"], # down
    "hard_drop":  ["w", "i"],
    "rotate_cw":  ["c", " ", "\x1b[A", "/"], # up
    "rotate_ccw": ["z", "q", ","],
    "rotate_180": ["\t", "x", "."], # tab
    "hold":       ["e", "v"],
    "pause":      ["\x1b", "p"],
}