from settingsController import settings_conduit as sc # Settings controller
from dataStructures import COLOR, GUI_GRID
import guiController as gui
import dataStructures as ds
import pygame as pg
import numpy as np


class tetris():
    def __init__(self, window_size, border):

        #self.player = player

        self.tetris_grid = [[False for x in range(sc['grid_size'])] for y in range(sc['grid_size']*2)] # Binary grid if a tetrominoes block exist at a grid square

        self.border = [x * gui.grid_square for x in border] # The x & y-axis boarder around the tetris game surface

        self.window_size = window_size # Size of the game window

        self.tetris_surface_size = ((self.window_size[1] - (self.border[1]*2) - (self.border[0]*2)) / 2, self.window_size[1] - (self.border[1]*2)) # The dimensions of the tetris game surface

        self.tetris_block_size = (self.tetris_surface_size[0]/sc['grid_size']) # The size of the tetris surface grid blocks, same size as tetrominoes blocks

        self.tetris_coordinates = self.create_coordinates() # Creates the coordinates of the tetris game surface grid for positioning

        self.tetris_surface = pg.Surface(self.tetris_surface_size)

        self.centering = (gui.grid[int(GUI_GRID/2)][0][0] - (self.tetris_surface_size[0]/2), self.border[1])

        self.tetris_grid_color = COLOR['black']

        self.tetris_surface_color = COLOR['grey']

        print(self.centering)

        # print(self.tetris_coordinates)
        #self.tetris_coordinates = list(np.array([[row_n * self.tetris_block_size for row_n in range(int(self.tetris_surface_size[1]/self.tetris_block_size))],
        #                [col_n * self.tetris_block_size for col_n in range(int(self.tetris_surface_size[0]/self.tetris_block_size))]]))

    def create_coordinates(self): # Creates the coordinates of the tetris game surface
        grid = []
        for row_n in range(len(self.tetris_grid)+1):
            if row_n > 0: grid.append(holder)
            holder=[]
            for col_n in range(len(self.tetris_grid[0])):
                holder.append([int(self.tetris_block_size * row_n), int(self.tetris_block_size * col_n)])
        return grid

    def render_grid(self, window):

        self.tetris_surface.fill(self.tetris_surface_color) # Render color of the surface

        for line_row in range(len(self.tetris_coordinates)): # Renders grid, rows
            if line_row > 0:
                pg.draw.aaline(
                    self.tetris_surface,
                    self.tetris_grid_color,
                    (0, self.tetris_coordinates[line_row][0][0]), # Start coordinates
                    (self.tetris_surface_size[0], self.tetris_coordinates[line_row][0][0]), # End coordinate
                    blend=1)

        for line_col in range(len(self.tetris_coordinates)): # Renders grid, columns
            if line_col > 0:
                pg.draw.aaline(
                    self.tetris_surface,
                    self.tetris_grid_color,
                    (self.tetris_coordinates[line_col][0][0], 0), # Start coordinates
                    (self.tetris_coordinates[line_col][0][0], self.tetris_surface_size[1])) # End coordinate

        window.blit(self.tetris_surface, self.centering) # Spans tetris game surface at the center of the screen