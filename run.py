# Project Files
import dataStructures as ds # Non game-loop use
import guiController as gui # GUI controller for element placement
from settingsController import settings_conduit as sc # JSON settings controller
from tetrominoes import tetrominoes # Tetris blocks
from gameLoop import one_player # Runs game-loop
from settings import settings # Runs settings menu
from tutorial import tutorial
from mainMenu import main_menu # Runs main menu
from soundController import SoundController # Import Sound Controller

# Import libraries
import pygame as pg
import numpy as np
import sys
import os

'''
Main script to run G5-Tetris game.
'''

# Game-loop functions
def get_time(): return pygame.time.get_ticks() # Gets current ticks

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

    # Initialize Sound Controller
    sound_controller = SoundController()
    sound_controller.play_bgm()  # Start background music

    # Game state-machine
    while running:

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
        if game_state == ds.GAME_STATE['p1_game']:
            attending_state = one_player(window, clock, window_size, sound_controller)
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
    #sound_controller.stop_background_music() # Stop background music when exiting
    pg.quit()
    sys.exit()


# /////////////////////////////////////////////////////////////////////////////////////////////

if __name__ == '__main__':
    main()
