from dataStructures import TETROMINOES, COLOR
from tetrisBlock import block as bk
import numpy as np
import random

class tetrominoes:
    def __init__(self, block_size, spawn):
        self.random_key = random.choice(list(TETROMINOES.keys()))
        self.shape_type = TETROMINOES[self.random_key]
        self.color = COLOR[self.random_key]
        self.number_shape = TETROMINOES[self.random_key]
        self.block_size = block_size + 1
        self.render_shape = self.number_convert()
        self.position = spawn
        self.static = False # If the tetromino is not moving
        self.preview_shape = [] # An image of the shape when flipped prior to commit
        self.block_locations = []; self.update_blocks() # An array where each block exists
        self.plumbed = False # If the tetrominoes has plummeted



    def number_convert(self): # Converts number matrices to object matrices (0,1) -> (None, Object)
        return [[None if x == 0 else bk(self.block_size, self.color) for x in row] for row in self.number_shape]

     # Updates the location of the blocks in the 4x4 matrices adding only the tetrominoes blocks to coordinates list
    def update_blocks(self):
        self.block_locations = []
        for y, row in enumerate(self.render_shape):
            for x, block in enumerate(row):
                if block != None: self.block_locations.append((y,x))


    # Flips the block in the tetrominoes by 90 degrees through coordinate vector rotation transformation
    def flip(self):
        tetrominoes_array = np.zeros([len(self.number_shape),len(self.number_shape)]) # Empty tetrominoes shape array

        center = np.array([(len(self.number_shape)-1)/2, (len(self.number_shape[0])-1)/2]) # Calculates matrices center based upon matrices length & width (row_center, column_center)

        # Get the indices x&y points where a block should exist based upon tetrominoes shape and subtracts the matrices centered values
        centered_coordinates = np.array([[row - center[0], col - center[0]] # Coordinate operation
        for row in range(len(self.number_shape)) # Gets row index
        for col in range(len(self.number_shape)) # Gets col index
        if self.number_shape[row][col] == 1]) # Checks for positive placement

        convert_array = np.array([[0,-1],[1,0]]) # Rotational matrices $\theta=\frac{\pi}{2}$ (LaTeX)

        # Preforms matrices multiplication for rotation while adding in center values
        translated_matrices = np.array([((convert_array @ coord_row) + center) for coord_row in centered_coordinates]).astype(int)

        for coord in translated_matrices: tetrominoes_array[coord[0]][coord[1]] = 1 # Places new coords in 0-1 matrices

        self.number_shape = list(tetrominoes_array) # Casts array to list
        self.preview_shape = self.number_convert() # Converts number array to object array
