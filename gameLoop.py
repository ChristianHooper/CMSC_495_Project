from settingsController import settings_conduit as sc # Settings controller
import pygame as pg
import dataStructures as ds
from dataStructures import COLOR
import numpy as np
from tetrisController import tetris
import guiController as gui


def one_player(window, clock, window_size): # Defines render aspects for a single player tetris session

    ts = tetris(window_size,
                [0, 1] # How may gui squares exists around the (x,y) boarders of the tetris game surface
    )

    running = True # Runs game-loop if true

    # ///////////////////////////////////////////[Game-Loop]///////////////////////////////////////////
    while running:

        for event in pg.event.get(): # Exiting condition
            if event.type == pg.QUIT:
                running = False

        window.fill(COLOR['black']) # Game widow fill

        gui.render_grid(window)
        ts.render_grid(window)
        #window.blit(tetris_surface, (window_size[0]/2-(tetris_surface_size[0]/2), tetris_boarder)) # Imposes tetris game surface on window (x, y)
        pg.display.flip() # Swaps buffer for rendering (Updates contents of display)


        dt = clock.tick(ds.FPS_CAP['default']) # Pauses game-loop to hold 60 FPS at default
        print(f"SPF: {dt / 1000.0} ms", end="\r") # Loop measured in milliseconds
