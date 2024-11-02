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

    # ///////////////////////////////////////////[Game-Loop]///////////////////////////////////////////
    while running:

        for event in pg.event.get(): # Exiting condition
            if event.type == pg.QUIT:
                running = False

        window.fill(COLOR['black']) # Game widow fill
        tetris_surface.fill(COLOR['white']) # Tetris frame fill

        # Draw grid, rows then columns
        #for line_row in grid_surface[0]: pg.draw.aaline(tetris_surface, COLOR['grey'], (0, line_row), (tetris_surface_size[0], line_row))
        #for line_col in grid_surface[1]: pg.draw.aaline(tetris_surface, COLOR['grey'], (line_col, 0), (line_col, tetris_surface_size[1]))
        gui.render_grid(window)
        ts.render_grid(window)
        #window.blit(tetris_surface, (window_size[0]/2-(tetris_surface_size[0]/2), tetris_boarder)) # Imposes tetris game surface on window (x, y)
        pg.display.flip() # Swaps buffer for rendering (Updates contents of display)


        dt = clock.tick(ds.FPS_CAP['default']) # Pauses game-loop to hold 60 FPS at default
        print(f"SPF: {dt / 1000.0} ms", end="\r") # Loop measured in milliseconds
