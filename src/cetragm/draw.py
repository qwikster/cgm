# DRAW.PY
# Module for drawing to the screen (stdout tomfuckery time!!!)
import sys
import shutil
from cetragm.tables import pieces, grades
from cetragm.game import collides

BLOCK = "██"
SHADOW = "▒▒"
EMPTY = "\x1b[48;2;20;20;20m\x1b[38;2;40;40;40m[]\x1b[49m\x1b[39m"
TOP_EMPTY = "  "

termwidth = 0
termheight = 0

def validate_board(board): # check for dimensions in case game loop fucked me
    if len(board) != 22:
        raise ValueError(f"Board has {len(board)} rows")
    widths = {len(r) for r in board}
    if widths != {10}:
        raise ValueError(f"Board has rows not 10 wide - {widths}")

def format_time(ms: int) -> str: # for TGM style timer at the bottom
    minutes = (ms // 1000) // 60 # Shame i can't make it obnoxiously big
    seconds = (ms // 1000) % 60  # or can i...? *mice on venus*
    hundredths = (ms % 1000) // 10
    return f"{minutes:02}:{seconds:02}:{hundredths:02}"

def color_block(piece_id: str | None): # in ["i", "z", "s", "l", "j", "t", "o"]
    if (not piece_id) and (not piece_id.endswith("_sh")):
        return EMPTY
    if not piece_id.endswith("_sh"):
        r, g, b = pieces[piece_id]["rgb"]
        return f"\x1b[38;2;{r};{g};{b}m{BLOCK}\x1b[0m"
    else:
        return f"\x1b[38;2;130;130;130m{SHADOW}\x1b[0m"

# public
def draw_board(board,                              # from game.py. Board: 2d list. Entries: [0] or [1, "t"]. 
               active_piece = None,                # {"name": "t", "pos": (0, 0), "rotation": "0"}
               score: int = 0, grade: str = "9",   # score is used to calculate TGM grade (9 -> 1 -> S1 -> S9 -> Gm)
               time_ms: int = 0,                   # BIG FLASHING TIMER
               lines: int = 0, line_goal: int = 0, # for gravity level up with timer
               hold: str | None = None,            # hold = "t"
               next_queue: list[str] | None = None # list of 5 pieces like ["t", "i", "z", "s", "o"] (7-bag)
               ):
    validate_board(board)
    height = len(board)
    width = len(board[0])
    
    # display on top of static board then check collision in game.py so it doesn't lag render loop
    overlay = [[cell[:] for cell in row] for row in board] # already the full board, needs to be colored
    
    # SHADOW PIECE
    if active_piece:
        pid = active_piece["name"]
        shape = pieces[pid]["rotations"][active_piece["rotation"]]
        px, py = active_piece["pos"]
        
        drop_y = py
        while True:
            drop_y += 1    
            if collides({"name": pid, "rotation": active_piece["rotation"], "pos": [px, drop_y]}, board):
                drop_y -= 1
                break
        
        for y, row in enumerate(shape):
            for x, val in enumerate(row):
                if val:
                    bx, by = px + x, drop_y + y
                    if 0 <= bx < width and 0 <= by < height:
                        overlay[by][bx] = [1, f"{pid}_sh"]
    
    # ACTUAL PIECE
    if active_piece:
        pid = active_piece["name"]
        shape = pieces[pid]["rotations"][active_piece["rotation"]]
        px, py = active_piece["pos"]
        for y, row in enumerate(shape):
            for x, val in enumerate(row):
                if val:
                    bx, by = px + x, py + y
                    if 0 <= bx < width and 0 <= by < height:
                        overlay[by][bx] = [1, pid]
                        
    left_lines = []
    left_lines.append("│ HOLD ▼ │")
    left_lines.append("╞════════╡")
    if hold and hold in pieces:
        for line in pieces[hold]["piece"]:
            left_lines.append(f"│{line.center(8)}│") # should already be centered but why not do it again
    else:
        left_lines.extend(["│   ╲╱   │", "│   ╱╲   │"])
    left_lines.append("╰────────┤")
    for i in grades[grade]:
        left_lines.append(i + "│")
        
    right_lines = []
    right_lines.append("│ NEXT ▼ │")
    right_lines.append("╞════════╡")
    
    if next_queue:
        for num, name in enumerate(next_queue[:5]):
            if name in pieces:
                for line in pieces[name]["piece"]:
                    right_lines.append(f"│{line.center(8)}│")
            else:
                right_lines.extend(["│   ╲╱   │", "│   ╱╲   │"])
            right_lines.append("├────────┤" if num != 4 else "├────────╯")
    else:
        for i in range(5):
            right_lines.extend(["│   ╲╱   │", "│   ╱╲   │", "├────────┤" if i != 4 else "├────────╯"])
    right_lines.append( "│         ")
    right_lines.append( "│ LEVEL:  ")
    right_lines.append(f"│  \x1b[4m{str(lines):^3}\x1b[24m")
    right_lines.append(f"│  {str(line_goal).ljust(9)}")
    
    frame_lines = []
    
    score = str(score) if len(str(score)) % 2 == 0 else ("0" + str(score))
    wid = (width - (len(score) // 2)) - 1
    frame_lines.append("╭────────┬"  + "─" * (wid) + f"╢{score}╟" + "─" * (wid) + "┬────────╮")
    
    for y in range(height):
        row_buf = []
        for x in range(width):
            cell = overlay[y][x]
            if y > 1:
                row_buf.append(color_block(cell[1]) if cell[0] else EMPTY)
            else:
                row_buf.append(color_block(cell[1]) if cell[0] else TOP_EMPTY)
                
        right = right_lines[y] if y < len(right_lines) else "│         "
        left = left_lines[y] if y < len(left_lines) else "         │"
        frame_lines.append(left + "".join(row_buf) + right)
    
    frame_lines.append( "         ├" + "──" * width + "┤")
    frame_lines.append(f"         │ ▶ {format_time(time_ms):^14}◀  │")
    frame_lines.append( "         ╰" + "──" * width + "╯")
    
    term = shutil.get_terminal_size()
    frame_width = len(frame_lines[0])
    pad_x = max((term.columns - frame_width) // 2, 0)
    pad_y = max((term.lines - len(frame_lines)) // 2, 0)
    
    global termwidth, termheight
    if pad_x != termwidth or pad_y != termheight:
        sys.stdout.write("\x1b[H\x1b[2J")
        termwidth, termheight = pad_x, pad_y
    
    centered = ("\n" * pad_y) + "\n".join(" " * pad_x + ln for ln in frame_lines)
    
    sys.stdout.write("\x1b[H" + centered + "\n\n")
    sys.stdout.flush()