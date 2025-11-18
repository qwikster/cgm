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
    pygame.K_d: "move_right",
    pygame.K_s: "soft_drop",
    pygame.K_w: "hard_drop",
    pygame.K_TAB: "rotate_180",
    pygame.K_SPACE: "rotate_cw",
    pygame.K_q: "rotate_ccw",
    pygame.K_ESCAPE: "pause",
    pygame.K_e: "hold",
}
