'''
{Main script to run G5-Tetris game}
'''

# Project Files
import dataStructures as ds # Non game-loop use
import settingsController
from settingsController import settings_conduit as sc # JSON settings controller
import guiController as gui # GUI controller for element placement
from tetrominoes import tetrominoes # Tetris blocks
from gameLoop import tetris_game # Runs game-loop
from aiGameLoop import ai_player
from settings import settings # Runs settings menu
from tutorial import tutorial
from mainMenu import main_menu # Runs main menu
from soundController import SoundController # Import Sound Controller

# Import libraries
import pygame as pg
import numpy as np
import sys
import os
from resource_path import resource_path


'''
main
-------------
The entry point function fro the program that sets game variables and runs the game state machine which is the central hub for game navigation.
'''
def main(): # Main function that acts as the game controller

    # Render Parameter
    pg.init() # Initialize pygame
    os.environ['SDL_VIDEO_WINDOW_POS'] = '100,100' # Positions game window at (0, 0) Left-side of screen
    game_state = ds.GAME_STATE['menu'] # Default game state at launch
    running = True # If game is running
    window_size = ds.SCREEN_SIZE[sc['screen_size']] # Default window size (x, y)

    # Window display on GPU, dual buffer
    window = pg.display.set_mode(window_size, pg.HWSURFACE | pg.DOUBLEBUF)
    clock = pg.time.Clock() # Starts game clock
    pg.display.set_caption("G5-Tetris") # Group-Five-Tetris
    icon = pg.image.load(resource_path('resources/G5-Tetris.png'))
    pg.display.set_icon(icon)

    # Initialize Sound Controller
    sound_controller = SoundController()
    sound_controller.play_bgm()  # Start background music

# ////////////////////////////////////////////////////////////[Game state-machine]////////////////////////////////////////////////////////////////////////
    while running: # Program-loop

        if game_state == None:
            running = False # Exit state condition

        # Main menu state
        if game_state == ds.GAME_STATE['menu']: # Checks for the main menu game state
            attending_state = main_menu(window, clock, window_size) # Runs current state, returns changed state
            if attending_state == None:
                running = False
            else:
                game_state = attending_state # Used to change game start based upon returned state

        # Settings state used to change general aspect of the game
        if game_state == ds.GAME_STATE['settings']:
            attending_state = settings(window, clock, window_size)
            if attending_state == None:
                running = False
            else:
                game_state = attending_state

        # Game-loop
        if game_state == ds.GAME_STATE['tetris_game']:
            attending_state = tetris_game(window, clock, window_size, sound_controller)
            if attending_state == None:
                running = False
            else:
                game_state = attending_state

        # AI game mode
        if game_state == ds.GAME_STATE['ai']:
            attending_state = ai_player(window, clock, window_size, sound_controller)
            if attending_state == None:
                running = False
            else:
                game_state = attending_state

        # Tutorial page
        if game_state == ds.GAME_STATE['tutorial']:
            attending_state = tutorial(window, clock, window_size)
            if attending_state == None:
                running = False
            else:
                game_state = attending_state

    # Cleans & terminates program
    sound_controller.stop_bgm() # Stop background music when exiting
    pg.quit()
    sys.exit()

# /////////////////////////////////////////////////////////////////////////////////////////////

if __name__ == '__main__':
    main()
