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

GAME_STATE = { # Game state for game state navigation
    'menu':     0, # Main menu
    'settings': 1, # User define setting menu
    'p1_game':  2, # Single player tetris
    'tutorial': 3,  # Tutorial screen
    'ai': 4 # AI versus player
}

COLOR = { # Defines all colors found in game
    'Z':      (245, 45, 40), # Red
    'S':      (55, 245, 90), # Green
    'J':     (50, 100, 245), # Blue
    'I':       (100, 245, 245), # Light-blue
    'O':        (245, 235, 40), # Yellow
    'L':     (245, 150, 40), # Orange
    'T':      (200, 60, 245), # Purple
    'i':      (240, 240, 250), # White

    # Tetrominoes Colors
    'red':        (245, 45, 40),
    'green':      (55, 245, 90),
    'blue':       (50, 100, 245),
    'white':      (230, 230, 245),
    'black':      (10, 10, 20 ),
    'grey':       (100, 100, 140),

    # Tetrominoes Colors
    'deep_red':        (207, 45, 40), # Red
    'deep_green':      (55, 207, 90), # Green
    'deep_blue':       (40, 80, 207), # Blue
    'deep_light_blue': (100, 207, 207), # Light-blue
    'deep_yellow':     (207, 200, 40), # Yellow
    'deep_orange':     (207, 120, 40), # Orange
    'deep_purple':     (160, 60, 207), # Purple
    'deep_white':      (200, 200, 210), # White


    # Color Theme
    'powder_pink':     (241, 194, 242),
    'soft_purple':     (194, 145, 242),
    'glass_purple':    (86, 77, 140),
    'vapor_blue':      (87, 170, 242),
    'abandon_food_court_in_the_middle_of_the_night_blue':       (141, 145, 219),
    'mono_white':      (217, 214, 255),
    'normal_map_blue': (128, 128, 255),
    'royal_jelly':     (250, 221, 98)
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

GRAVITY_SPEED = 500 # Starting default gravity speed for tetris game (milliseconds)
KEY_PRESS_SPEED = 100 # Default key press response rate in tetris game (milliseconds)

FONTS = { # All font objects used across the game
    'default_large': pg.font.Font('resources/retro_gaming.ttf', 50),
    'default_medium2': pg.font.Font('resources/retro_gaming.ttf', 34),
    'default_medium': pg.font.Font('resources/retro_gaming.ttf', 24),
    'default_small': pg.font.Font('resources/retro_gaming.ttf', 18),
    'title_font': pg.font.Font('resources/Gabato.ttf', 64)
    # 'retro_large': pg.font.Font('resources/retro_gaming.ttf' , 50)
}

FPS_CAP = { # Game FPS cap
    'trip' : 1,
    'default': 60
    }

GRID_SIZE = (8, 10, 12, 16, 20, 24, 32) # Basic sizes for tetris surface; can be any number that even

ASPECT = 2 # Aspect ratio of tetris frame render

GUI_GRID = 32 # The number of grids squares on the window screen width, works best as an even number

TETROMINOES = { # Shape and size of the tetrominoes defines by matrices, can be larger or smaller that 4x4
    'I':    [[0,0,1,0], [0,0,1,0], [0,0,1,0], [0,0,1,0]],
    'J':    [[0,0,1,0], [0,0,1,0], [0,1,1,0], [0,0,0,0]],
    'L':    [[0,1,0,0], [0,1,0,0], [0,1,1,0], [0,0,0,0]],
    'O':    [[0,0,1,1], [0,0,1,1], [0,0,0,0], [0,0,0,0]],
    'S':    [[0,0,1,1], [0,1,1,0], [0,0,0,0], [0,0,0,0]],
    'T':    [[0,0,1,0], [0,1,1,1], [0,0,0,0], [0,0,0,0]],
    'Z':    [[0,1,1,0], [0,0,1,1], [0,0,0,0], [0,0,0,0]],
    'i':    [[0,0,1,0], [0,0,1,0], [0,0,0,0], [0,0,0,0]],
    #'dev_I':    [[1,1,1,1], [0,0,1,0], [0,0,1,0], [1,1,1,1]],
    #'the_devil':[[1,0,1,0], [0,1,0,1], [1,0,1,0], [0,1,0,1]],
}

POPULATION = 12 # AI agent population to be tested in each epoch/generation

GENERATIONS = 100 # Number of generation AI testing simulation is run

PRIME = { # Selected chromosome of AI agent
            "Smoothness": 0.2867956688508934,
            "Maximum": 0.6312906097241524,
            "Minimum": 0.07999705718157621,
            "Lines": 0.20483005766792878,
            "Pit": 0.8249497156837208, # 0.7249497156837208
            "Hole": 1.0249497156837208, # 0.7249497156837208
            "Age": 616
        }