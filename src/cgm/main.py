# Main module
import sys
from pieces import pieces
import time

def entry():
    while(1):
        for rot in ["0", "r", "2", "l"]:
            for k in pieces:
                for i in pieces[k]["rotations"][rot]:
                    r, g, b = pieces[k]["rgb"]
                    print(f"\x1b[38;2;{r};{g};{b}m", end = "")
                    for j in i:
                        if j:
                            print("██", end="")
                        else:
                            print("  ", end="")
                    print()
            time.sleep(0.3)
            print("\033[2J\033[H")

if __name__ == "__main__":
    try:
        entry()
    except KeyboardInterrupt:
        sys.exit(0)