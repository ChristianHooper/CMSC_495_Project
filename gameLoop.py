from settingsController import settings_conduit as sc # Settings controller
import pygame as pg
import dataStructures as ds
from dataStructures import COLOR
import numpy as np


def one_player(window, clock, window_size): # Defines render aspects for a single player tetris session

    aspect_ratio = sc['aspect_ratio'] # Defines aspect ratio for tetris frame render
    running = True # Runs game-loop if true

    # Size of the tetris game surface (x, y) Defines width through division of screen length size.
    tetris_surface_size = (window_size[1]/aspect_ratio, window_size[1])

    grid_size = (tetris_surface_size[0]/sc['grid_size'], tetris_surface_size[1]/sc['grid_size']*aspect_ratio) # Tetris grid size, settings call

    tetris_boarder = grid_size[0] # Boarder thickness around tetris surface (x, y) measured is grid units

    tetris_surface_size = tuple(int(axis - tetris_boarder*2) for axis in tetris_surface_size) # Negate boarder from tetris frame

    tetris_surface = pg.Surface(tetris_surface_size) # Object frame where tetris game is played

    # tetris_surface_p2 = tetris_surface # Second player tetris game surface

    # Grid surface render points, immutable
    grid_surface = np.array([[row_n * tetris_boarder for row_n in range(int(tetris_surface_size[1]/tetris_boarder))],
                            [col_n * tetris_boarder for col_n in range(int(tetris_surface_size[1]/tetris_boarder))]])

    print("Grid Points: ", grid_surface)

    # ///////////////////////////////////////////[Game-Loop]///////////////////////////////////////////
    while running:

        for event in pg.event.get(): # Exiting condition
            if event.type == pg.QUIT:
                running = False

        window.fill(COLOR['black']) # Game widow fill
        tetris_surface.fill(COLOR['white']) # Tetris frame fill

        # Draw grid, rows then columns
        for line_row in grid_surface[0]: pg.draw.aaline(tetris_surface, COLOR['grey'], (0, line_row), (tetris_surface_size[0], line_row))
        for line_col in grid_surface[1]: pg.draw.aaline(tetris_surface, COLOR['grey'], (line_col, 0), (line_col, tetris_surface_size[1]))

        window.blit(tetris_surface, (window_size[0]/2-(tetris_surface_size[0]/2), tetris_boarder)) # Imposes tetris game surface on window (x, y)
        pg.display.flip() # Swaps buffer for rendering (Updates contents of display)


        dt = clock.tick(ds.FPS_CAP['default']) # Pauses game-loop to hold 60 FPS at default
        print(f"SPF: {dt / 1000.0} ms", end="\r") # Loop measured in milliseconds
