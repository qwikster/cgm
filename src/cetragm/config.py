# Module for configuration the user probably wouldn't see, keymaps and gravity etc

import pygame

MAX_LOCK_RESETS = 15
ARE_FRAMES = 20
LINE_CLEAR_FRAMES = 20
LOCK_DELAY_FRAMES = 30

DAS_MS = 150
ARR_MS = 50
SOFT_ARR_MS = 50

KEYMAP = {
    pygame.K_a: "move_left",
    pygame.K_d: "move_right",
    pygame.K_s: "soft_drop",
    pygame.K_w: "hard_drop",
    pygame.K_e: "hold",
    pygame.K_TAB: "rotate_180",
    pygame.K_SPACE: "rotate_cw",
    pygame.K_q: "rotate_ccw",
    pygame.K_ESCAPE: "pause",
}

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