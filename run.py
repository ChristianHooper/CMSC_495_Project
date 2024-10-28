# Project Files
import dataStructures as ds # Non game-loop use
from dataStructures import COLOR # Game-loop use
from tetrominoes import tetrominoes # Tetris blocks


# Import libraries
import pygame as pg
import numpy as np
import os


pg.init() # Initialize pygame
os.environ['SDL_VIDEO_WINDOW_POS'] = '0,0' # Positions game window at (0, 0) Left-side of screen

# Game-loop functions
def get_time(): return pygame.time.get_ticks() # Gets current ticks

# ///////////////////////////////////////////[Render Parameters]///////////////////////////////////////////
running = True # If game is running
window_size = ds.SCREEN_SIZE['1920x1080'] # Window size (x, y)

aspect_ratio = ds.ASPECT # Defines aspect ratio for tetris frame render

# Size of the tetris game surface (x, y) Defines width through division of screen length size.
tetris_surface_size = (window_size[1]/aspect_ratio, window_size[1])

grid_size = (tetris_surface_size[0]/ds.GRID_SIZE[2], tetris_surface_size[1]/ds.GRID_SIZE[2]*aspect_ratio) # Tetris grid size

tetris_boarder = grid_size[0]# Boarder thickness around tetris surface (x, y) measured is grid units

tetris_surface_size = tuple(int(axis - tetris_boarder*2) for axis in tetris_surface_size) # Negate boarder from tetris frame

tetris_surface = pg.Surface(tetris_surface_size) # Object frame where tetris game is played

# tetris_surface_p2 = tetris_surface # Second player tetris game surface

# Grid surface render points, immutable
grid_surface = np.array([[row_n * tetris_boarder for row_n in range(int(tetris_surface_size[1]/tetris_boarder))],
                [col_n * tetris_boarder for col_n in range(int(tetris_surface_size[1]/tetris_boarder))]])

print("Grid Points: ", grid_surface)

window = pg.display.set_mode(window_size, pg.HWSURFACE | pg.DOUBLEBUF) # Window display on GPU, dual buffer
clock = pg.time.Clock() # Starts game clock


pg.display.set_caption("G5-Tetris") # Group-Five-Tetris

# /////////////////////////////////////////////////////////////////////////////////////////////


'''
Main game-loop for CMSC-495 G5-Tetris game.
'''
while running:

    for event in pg.event.get(): # Exiting condition
        if event.type == pg.QUIT:
            running = False

    window.fill(COLOR['black']) # Game widow fill
    tetris_surface.fill(COLOR['white']) # Tetris frame fill
    #print("[]")




    # Draw grid, rows then columns
    for line_row in grid_surface[0]: pg.draw.aaline(tetris_surface, COLOR['grey'], (0, line_row), (tetris_surface_size[0], line_row))
    for line_col in grid_surface[1]: pg.draw.aaline(tetris_surface, COLOR['grey'], (line_col, 0), (line_col, tetris_surface_size[1]))

    window.blit(tetris_surface, (tetris_boarder, tetris_boarder)) # Imposes tetris game surface on window (x, y)
    pg.display.flip() # Swaps buffer for rendering


    dt = clock.tick(ds.ANIMATION_SPEED['default']) # Pauses game-loop to hold 60 FPS at default
    print(f"SPF: {dt / 1000.0} ms", end="\r") # Loop measured in milliseconds


#if __name__ == '__main__':