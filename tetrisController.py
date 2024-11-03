from settingsController import settings_conduit as sc # Settings controller
from dataStructures import COLOR, GUI_GRID
import tetrominoes as tm
import guiController as gui
import dataStructures as ds
import pygame as pg
import numpy as np


class tetris():
    def __init__(self, window_size, border):

        #self.player = player

        self.tetris_grid = [[None for x in range(sc['grid_size'])] for y in range(sc['grid_size']*2)] # Binary grid if a tetrominoes block exist at a grid square

        self.border = [x * gui.grid_square for x in border] # The x & y-axis boarder around the tetris game surface

        self.window_size = window_size # Size of the game window

        self.tetris_surface_size = ((self.window_size[1] - (self.border[1]*2) - (self.border[0]*2)) / 2, self.window_size[1] - (self.border[1]*2)) # The dimensions of the tetris game surface

        self.tetris_block_size = (self.tetris_surface_size[0]/sc['grid_size']) # The size of the tetris surface grid blocks, same size as tetrominoes blocks

        self.tetris_coordinates = self.create_coordinates() # Creates the coordinates of the tetris game surface grid for positioning

        self.tetris_surface = pg.Surface(self.tetris_surface_size)

        self.centering = (gui.grid[int(GUI_GRID/2)][0][0] - (self.tetris_surface_size[0]/2), self.border[1])

        self.tetris_grid_color = COLOR['black']

        self.tetris_surface_color = COLOR['grey']

        self.current_tetrominoes = None

        self.current_tetrominoes = self.generate_tetrominoes()

        self.render_points = []

        # print(self.centering)

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


    def render_tetris(self, window):
        self.tetris_surface.fill(self.tetris_surface_color) # Render color of the surface

        self.update_grid()
        self.render_tetrominoes()

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

    def generate_tetrominoes(self):
        return tm.tetrominoes(
                self.tetris_block_size, # Size of the block that makes up tetrominoes
                (3, 3) # Where the tetrominoes spawn
                )

    def update_grid(self):
        self.render_points = []
        for row in range(len(self.tetris_grid)):
            for col in range(len(self.tetris_grid[row])):
                # Checks the shape of tetrominoes against the grid
                #print(self.current_tetrominoes.shape)
                if row >= self.current_tetrominoes.position[0] and self.current_tetrominoes.position[0] + len(self.current_tetrominoes.render_shape[1]) > row:
                    if col >= self.current_tetrominoes.position[1] and self.current_tetrominoes.position[1] + len(self.current_tetrominoes.render_shape[0]) > col:
                        #print(f"C: {row - self.current_tetrominoes.position[1]}, {col - self.current_tetrominoes.position[0]}")
                        grid_square = self.current_tetrominoes.render_shape[col - self.current_tetrominoes.position[0]][row - self.current_tetrominoes.position[1]]
                        if grid_square != None:
                        # Places block object into their respective grid position based upon their current position.
                            self.tetris_grid[row][col] = grid_square
                            self.render_points.append([row, col]) # Creates a list of induces for blocks to be rendered on the grid
        #print(self.tetris_grid)

    def render_tetrominoes(self): # Access block directly instead of through tetrominoes object
        for x in self.render_points:
            block = self.tetris_grid[x[0]][x[1]] # Uses render points list to define block from tetris grid
            # print("CORDS: ", tuple(self.tetris_coordinates[x[0]][x[1]]))
            # block.position = self.tetris_coordinates[x[0]][x[1]]
            block.small_block.x = self.tetris_coordinates[x[0]][x[1]][0]
            block.small_block.y = self.tetris_coordinates[x[0]][x[1]][1]
            pg.draw.rect(self.tetris_surface, block.color, block.small_block)



    def scoring(self):
        print()
