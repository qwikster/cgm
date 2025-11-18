# cgm
### Cetra Grand Master!

A block stacker game that you might find very familiar. Built with similar design to Tetris Grand Master in mind, but runs entirely in your terminal with much more modern mechanics.

What's Tetris Grand Master? It's a really old Japanese arcade franchise that used a lot of nonstandard features and was regarded as being incredibly hard. Your goal is to survive from levels 500 to 999 in 20g (pieces instantly falling to the bottom) and achieve the rank of Grandmaster. Yeah uh... nobody here is doing that, so it's just really hard Tetris. If anyone gets an S1+ rank, DM me @qwik!

## how
`pip install cetragm`, or `pipx install cetragm` if you're on an externally managed system like Arch Linux. You may need the `pygame` module if you don't have it or if pip doesn't install it for you. Run `cgm`.

## demo


Additions from last week:
- Entire UI system
- Rebindable controls
- SRS (Super Rotation System)
- DAS/ARR/SDF customization
- New input system, allowing said changes
- Improved game loop
- Tweaks to difficulty and progression

how does it fit the theme?
uuh technically the main gameplay of tetris is avoiding SPACEs in your stack... yeah, it's a stretch, but I had no time to do better.

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
- Full UI system
- Fixed, fully rebindable controls

To add:
- T-spins and detection for them
- IHS and IRS (Inital Hold/Rotation System)

## controls
There's a menu for that! I recommend you pick your own controls - they'll save automatically.

DAS: Delayed Auto Shift, how long until keys start to repeat.\n
ARR: Auto Repeat Rate, how quickly keys repeat.\n
SDF: Soft Drop Force, how fast your soft drop key goes down.

## why
Built for [Hack Club](https://hack.club)'s [Siege](https://siege.hackclub.com) program (week 10 and 11). Also, I like block stackers.
