# cgm
### Cetra Grand Master!

A block stacker game that you might find very familiar. Built with similar design to Tetris Grand Master in mind, but runs entirely in your terminal with much more modern mechanics.

## how
`pip install cetragm`, or `pipx install cetragm` if you're on an externally managed system like Arch Linux. You may need the `pygame` module if you don't have it or if pip doesn't install it for you. Run `cgm`.

If you'd like to customise your controls, you may change them in `/src/cgm/config.py` under the project directory.

To change DAS (how long until inputs repeat) and ARR (how fast inputs repeat), you'll have to do it under your OS' settings for now. On Windows, it should be under the Mouse and Keyboard controls. On KDE Plasma, under System Settings > Keyboard > Repeat Rate. On Mac, go ask Tim Cook. On Gnome, go ask Richard Stallman's left foot. Otherwise, I'm sure you can figure it out.

## what
Features:
- Supports any terminal emulator, Windows or Linux. (Not tested on Mac but may work.)
- Rebindable controls, including hard and soft drops as well as holds.
- Grade system, up to the Gm grade (which I guarantee you won't get)
- Full color!
- Dynamic gravity (speed) as your level increases
- Scoring system
- Gameplay timer
- 7-bag piece drawing
- 5-piece next queue and level display
- Persistent TLS (or shadow piece)
- TGM's 20G gravity after level 500
- Proper ARE, lock delay, and line clear delay
- Real-time gravity (not tied to frame rates)
- The standard Super Rotation System and all its janky kicks!

Drawbacks:
- Requires manual ARR/DAS and can't press two keys at once
- Scoring is slightly off
- Lack of theming or menus at all, as well as a lose state
- No sound (background or effect)

To add by next week:
- T-spins and detection for them
- IHS and IRS (Inital Hold/Rotation System)
- Full menu with configuration
- Tiny optional input window via Pygame to add proper multi-key controls and DAS/ARR
- Config config config! maybe even a new gamemode...

## controls
You may configure these in `config.py`, but the defaults (and what I use) follow:

| Buttons | Function | huh |
| :---------: | :--------: | :---- |
| `←` `a` `j` | Move Left | |
| `→` `d` `l` | Move Right | |
| `↑` `space` `/` `c` | Rotate CW | |
| `z` `,` `q` | Rotate CCW | |
| `tab` `x` `.` | Rotate 180 | |
| `↓` `s` `k` | Soft Drop | move your piece down faster, but don't immediately lock it into place |
| `w` `i` | Hard Drop  | move your piece as far down as it will go and lock it in place, skipping the delay |
| `e` `v` | Hold Piece | put a piece aside or switch to your held piece when it doesn't fit |
| `esc` `p` | quit | why would you ever want to do that? | 


## why
Built for [Hack Club](https://hack.club)'s [Siege](https://siege.hackclub.com) program (week 10 and 11). Also, I like block stackers.