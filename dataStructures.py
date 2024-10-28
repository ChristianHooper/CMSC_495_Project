'''
Data structures used for calls throughout the project.
The data represented in this project should be immutable and only referenced once game-loop begins.
Calls made in game-loop should generally only be made if imported directly, outside of game-loop they can just be called.
'''

GAME_STATE = {
    'menu':     0,
    'settings': 1,
    'p1_game':  2
}

COLOR = { # Defines colors
    'red':   (200, 0, 25),
    'green': (0, 200, 25),
    'blue':  (0, 25, 200),
    'white': (200, 200, 250),
    'black': (10, 10, 30 ),
    'grey':  (100, 100, 140)
    }

SCREEN_SIZE = { # Defines possible screen resolutions
    '1920x1080': (1920, 1080),
    '1366x768':  (1366, 768),
    '1280x1024': (1280, 1024),
    '1440x900':  (1440, 900),
    '1600x900':  (1600, 900),
    '1680x1050': (1680, 1050),
    '1280x800':  (1280, 800),
    '1024x768':  (1024, 768),
    '2560x1440': (2560, 1440),
    '3840x2160': (3840, 2160),
    }

ANIMATION_SPEED = { # Game FPS cap
    'default': 60,
    }

GRID_SIZE = (8, 10, 12, 16, 20, 24, 32) # Grid sizes for tetris surface

ASPECT = 2 # Aspect ratio of tetris frame render