import sys
import shutil
import time
import pygame
import queue

from cetragm import config

MENU_COLOR_SELECTED = "\x1b;38;2;127;255;212m"
MENU_COLOR_NORMAL   = "\x1b;38;2;220;220;220m"
MENU_COLOR_VALUE    = "\x1b;38;2;13;152;186m"

def center_lines(lines):
    term = shutil.get_terminal_size()
    max_width = max(len(ln) for ln in lines) if lines else 0
    pad_x = max((term.columns - max_width) // 2, 0)
    pad_y = max((term.lines - len(lines)) // 2, 0)
    centered = ("\n" * pad_y) + "\n".join(" " * pad_x + ln for ln in lines)
    sys.stdout.write("\x1b[H\x1b[2J" + centered + "\n\n")
    sys.stdout.flush

def draw_menu(title, options, selected):
    width = max(len(opt) for opt in options)
    lines = []
    lines.append("╭" + "─" * (width - 2) + "╮")
    lines.append("│" + title.center(width - 2) + "│")
    lines.append("├" + "─" * (width - 2) + "│")

    for i, opt in enumerate(options):
        color = MENU_COLOR_SELECTED if i == selected else MENU_COLOR_NORMAL
        reset = MENU_COLOR_NORMAL if i == selected else ""
        lines.append("│ " + color + opt.ljust(width - 4) + reset + " │")
    
    lines.append("╰" + "─" * (width - 2) + "╯")
    center_lines(lines)

def draw_lose_screen(score, grade, time_ms, options, selected):
    lines = []
    lines.append( "╭──────────────────╮")
    lines.append( "│    GAME  OVER    │")
    lines.append( "├──────────────────┤")
    lines.append(f"│ SCORE: {str(score).rjust(10)} │")
    lines.append(f"│ GRADE: {grade.rjust(10)} │")
    lines.append(f"│ TIME:  {format_time(time_ms).rjust(10)} │")
    lines.append( "├──────────────────┤")
    for i, opt in enumerate(options):
        color = MENU_COLOR_SELECTED if i == selected else MENU_COLOR_NORMAL
        reset = MENU_COLOR_NORMAL if i == selected else ""
        lines.append("│" + color + opt.center(18) + reset + "│")
    lines.append( "╰──────────────────╯")

def format_time(ms: int) -> str:
    return f"{((ms // 1000) // 60):02}:{((ms // 1000) % 60):02}:{((ms % 1000) // 10):02}"

def draw_rebind_prompt(action_name):
    title = "REBIND KEYS"
    prompt = f"Press key for {action_name.replace("_", " ").title()}"
    width = len(prompt) + 6
    lines = []
    lines.append("╭" + "─" * (width - 2) + "╮")
    lines.append("│" + title.center(width - 2) + "│")
    lines.append("├" + "─" * (width - 2) + "┤")
    lines.append("│ " + prompt.ljust(width - 4) + " │")
    lines.append("╰" + "─" * (width - 2) + "╯")
    center_lines(lines)

def save_config():
    with open("config.py", "w") as f:
        f.write( "import pygame\n\n")
        f.write(f"MAX_LOCK_RESETS = {config.MAX_LOCK_RESETS}\n")
        f.write(f"ARE_FRAMES = {config.ARE_FRAMES}\n")
        f.write(f"LINE_CLEAR_FRAMES = {config.LINE_CLEAR_FRAMES}\n")
        f.write(f"LOCK_DELAY_FRAMES = {config.LOCK_DELAY_FRAMES}\n")
        f.write(f"DAS_MS = {config.DAS_MS}\n")
        f.write(f"ARR_MS = {config.ARR_MS}\n")
        f.write(f"SDF = {config.SDF}\n")
        f.write( "KEYMAP = {\n")
        for key,value in config.KEYMAP.items():
            key_name = pygame.key.name(key)
            f.write(f"    pygame.K_{key_name}: \"{value}\",\n")
        f.write("}\n")

def run_main_menu(inputs):
    inputs.menu_mode = True
    selected = 0
    options = ["Play", "Space Race", "Settings", "Quit"]
    while True:
        draw_menu("CGM", options, selected)
        time.sleep(1/60)
        try:
            action = inputs.queue.get_nowait()
        except queue.Empty:
            continue
        if action == "up":
            selected = (selected - 1) % len(options)
        elif action == "down":
            selected = (selected + 1) % len(options)
        elif action == "select":
            inputs.menu_mode = False
            if selected == 0:
                return "play"
            elif selected == 1:
                return "spacerace"
            elif selected == 2:
                run_settings_menu(inputs)
            elif selected == 3:
                return "quit"
        elif action == "back":
            inputs.menu_mode = False
            return "quit"


# need: input parser menu mod, space race (cheese race), main loop integ., setup, lose integ., lose screen for spacerace 