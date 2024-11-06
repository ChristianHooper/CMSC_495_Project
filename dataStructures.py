from settingsController import settings_conduit as sc
import pygame as pg
import numpy as np
pg.init()

'''
Data structures used for calls throughout the project.
The data represented in this project should be immutable and only referenced.
Calls made in game-loop should generally only be made if imported directly.
Calls outside of game-loop can reference imported file object.
'''

GAME_STATE = {
    'menu':     0, # Main menu
    'settings': 1, # User define setting menu
    'p1_game':  2, # Single player tetris
    'tutorial': 3  # Tutorial screen
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

GRAVITY_SPEED = 500 # Millisecond

FONTS = { # Fonts with sizes
    'default_large': pg.font.Font(None, 64)
}

FPS_CAP = { # Game FPS cap
    'trip' : 1,
    'default': 60
    }

GRID_SIZE = (8, 10, 12, 16, 20, 24, 32) # Grid sizes for tetris surface

ASPECT = 2 # Aspect ratio of tetris frame render

GUI_GRID = 32 # The number of grids squares on the window screen width, works best as an even number.
TETROMINOES = {
    'long':     [[0,1,0,0], [0,1,0,0], [0,1,0,0], [0,1,0,0]],
    'l_long':   [[0,1,0,0], [0,1,0,0], [1,1,0,0], [0,0,0,0]],
    'r_long':   [[0,0,1,0], [0,0,1,0], [0,0,1,1], [0,0,0,0]],
    'box':      [[0,0,0,0], [0,1,1,0], [0,1,1,0], [0,0,0,0]],
    's_box':    [[0,0,0,0], [0,0,1,1], [0,1,1,0], [0,0,0,0]],
    't_box':    [[0,0,0,0], [0,1,1,1], [0,0,1,0], [0,0,0,0]],
    'z_box':    [[0,0,0,0], [1,1,0,0], [0,1,1,0], [0,0,0,0]],
    'z_box':    [[0,0,0,0], [1,1,0,0], [0,1,1,0], [0,0,0,0]],
    'h_box':    [[0,0,0,0], [0,0,1,0], [0,0,1,0], [0,0,0,0]],
    #'dev_I':    [[1,1,1,1], [0,0,1,0], [0,0,1,0], [1,1,1,1]],
    #'the_devil':[[1,0,1,0], [0,1,0,1], [1,0,1,0], [0,1,0,1]],
}
