# Module for configuration the user probably wouldn't see, keymaps and gravity etc

import pygame

MAX_LOCK_RESETS = 15
ARE_FRAMES = 20
LINE_CLEAR_FRAMES = 20
LOCK_DELAY_FRAMES = 30

DAS_MS = 150
ARR_MS = 50
SDF = 50

KEYMAP = {
    pygame.K_a: "move_left",
    pygame.K_j: "move_left",
    pygame.K_LEFT: "move_left",

    pygame.K_d: "move_right",
    pygame.K_l: "move_right",
    pygame.K_RIGHT: "move_right",

    pygame.K_s: "soft_drop",
    pygame.K_k: "soft_drop",
    pygame.K_DOWN: "soft_drop",

    pygame.K_w: "hard_drop",
    pygame.K_i: "hard_drop",
    pygame.K_f: "hard_drop",

    pygame.K_c: "rotate_cw",
    pygame.K_SPACE: "rotate_cw",
    pygame.K_UP: "rotate_cw",
    pygame.K_SLASH: "rotate_cw",
    
    pygame.K_z: "rotate_ccw",
    pygame.K_q: "rotate_ccw",
    pygame.K_COMMA: "rotate_ccw",

    pygame.K_TAB: "rotate_180",
    pygame.K_x: "rotate_180",
    pygame.K_PERIOD: "rotate_180",

    pygame.K_e: "hold",
    pygame.K_v: "hold",

    pygame.K_ESCAPE: "pause",
    pygame.K_p: "pause",
}
 
""" # keymap for normal people
KEYMAP = {
    pygame.K_LEFT: "move_left",
    pygame.K_RIGHT: "move_right",
    pygame.K_DOWN: "soft_drop",
    pygame.K_SPACE: "hard_drop",
    pygame.K_LSHIFT: "hold",
    pygame.K_a: "rotate_180",
    pygame.K_UP: "rotate_cw",
    pygame.K_x: "rotate_cw",
    pygame.K_z: "rotate_ccw",
    pygame.K_ESCAPE: "pause",
}
"""

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