# Project Files
import dataStructures as ds # Non game-loop use
from dataStructures import COLOR # Game-loop use
from tetrominoes import tetrominoes # Tetris blocks
from gameLoop import one_player # Runs game-loop
import settings # Runs settings menu
from menu import menu # Runs main menu


# Import libraries
import pygame as pg
import numpy as np
import sys
import os


# ///////////////////////////////////////////[]///////////////////////////////////////////
# Game-loop functions
def get_time(): return pygame.time.get_ticks() # Gets current ticks


'''
Main starting functions for CMSC-495 G5-Tetris game.
'''
def main():

    # Render Parameter
    pg.init() # Initialize pygame
    os.environ['SDL_VIDEO_WINDOW_POS'] = '0,0' # Positions game window at (0, 0) Left-side of screen
    game_state = ds.GAME_STATE['p1_game'] # Default game state at launch
    running = True # If game is running
    window_size = ds.SCREEN_SIZE['1920x1080'] # Default window size (x, y)
    # Window display on GPU, dual buffer
    window = pg.display.set_mode(window_size, pg.HWSURFACE | pg.DOUBLEBUF)
    clock = pg.time.Clock() # Starts game clock
    pg.display.set_caption("G5-Tetris") # Group-Five-Tetris


    # Game state machine
    while running:

        #for event in pg.event.get(): # Exiting state condition
            #if event.type == pg.QUIT: running = False

        # Main menu state
        if game_state == ds.GAME_STATE['menu']:
            attending_state = menu(window, clock, window_size) # Runs current state, returns changed state
            if game_state == None: running = False # If game state is exited
            else: game_state = attending_state

        # Settings state used to change general aspect of the game
        if game_state == ds.GAME_STATE['settings']:
            attending_state = settings(window, clock, window_size) # Runs current state, returns changed state
            if game_state == None: running = False
            else: game_state = attending_state

        # Game-loop
        if game_state == ds.GAME_STATE['p1_game']:
            attending_state = one_player(window, clock, window_size) # Runs current state, returns changed state
            if game_state == None: running = False
            else: game_state = attending_state

        # Cleans & terminates program
        pg.quit()
        sys.exit()


# /////////////////////////////////////////////////////////////////////////////////////////////


if __name__ == '__main__':
    main()