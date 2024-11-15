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
    'z_box':      (245, 45, 40), # Red
    's_box':      (55, 245, 90), # Green
    'l_long':     (50, 100, 245), # Blue
    'long':       (100, 245, 245), # Light-blue
    'box':        (245, 235, 40), # Yellow
    'r_long':     (245, 150, 40), # Orange
    't_box':      (200, 60, 245), # Purple
    'short':      (240, 240, 250), # White

    # GUI Colors
    'red':        (245, 45, 40),
    'green':      (55, 245, 90),
    'blue':       (50, 100, 245), # Blue
    'white':      (230, 230, 245),
    'black':      (10, 10, 20 ),
    'grey':       (100, 100, 140),
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

GRAVITY_SPEED = 500 # Milliseconds
KEY_PRESS_SPEED = 100 # Milliseconds

FONTS = { # Fonts with sizes
    'default_large': pg.font.Font('resources/retro_gaming.ttf', 50),
    'default_medium': pg.font.Font('resources/retro_gaming.ttf', 24),
    'default_small': pg.font.Font('resources/retro_gaming.ttf', 18)
    # 'retro_large': pg.font.Font('resources/retro_gaming.ttf' , 50)
}

FPS_CAP = { # Game FPS cap
    'trip' : 1,
    'default': 60
    }

GRID_SIZE = (8, 10, 12, 16, 20, 24, 32) # Grid sizes for tetris surface

ASPECT = 2 # Aspect ratio of tetris frame render

GUI_GRID = 32 # The number of grids squares on the window screen width, works best as an even number.
TETROMINOES = {
    'long':     [[0,0,1,0], [0,0,1,0], [0,0,1,0], [0,0,1,0]],
    'l_long':   [[0,0,1,0], [0,0,1,0], [0,1,1,0], [0,0,0,0]],
    'r_long':   [[0,1,0,0], [0,1,0,0], [0,1,1,0], [0,0,0,0]],
    'box':      [[0,1,1,0], [0,1,1,0], [0,0,0,0], [0,0,0,0]],
    's_box':    [[0,0,1,1], [0,1,1,0], [0,0,0,0], [0,0,0,0]],
    't_box':    [[0,0,1,0], [0,1,1,1], [0,0,0,0], [0,0,0,0]],
    'z_box':    [[1,1,0,0], [0,1,1,0], [0,0,0,0], [0,0,0,0]],
    'short':    [[0,0,1,0], [0,0,1,0], [0,0,0,0], [0,0,0,0]],
    #'dev_I':    [[1,1,1,1], [0,0,1,0], [0,0,1,0], [1,1,1,1]],
    #'the_devil':[[1,0,1,0], [0,1,0,1], [1,0,1,0], [0,1,0,1]],
}
