from dataStructures import TETROMINOES, COLOR
from tetrisBlock import block as bk
import numpy as np
import random

class tetrominoes:
    def __init__(self, block_size, spawn):
        self.shape_type = random.choice(list(TETROMINOES.keys()))
        self.color = COLOR[random.choice(list(COLOR.keys()))]
        self.number_shape = TETROMINOES[self.shape_type]
        self.block_size = block_size + 1
        self.render_shape = self.number_convert()
        self.position = spawn
        self.static = False # If the tetromino is not moving

    def number_convert(self):
        return [[None if x == 0 else bk(self.block_size, self.color) for x in row] for row in self.number_shape]


    # Flips the block in the tetrominoes by 90 degrees
    def flip(self):

        tetrominoes_array = np.zeros([len(self.number_shape),len(self.number_shape)])

        center = np.array([(len(self.number_shape)-1)/2, (len(self.number_shape[0])-1)/2]) # Calculates matrices center based upon matrices length & width (row_center, column_center)

        # Get the indices x&y points where a block should exist based upon tetrominoes shape and subtracts the matrices centered values
        centered_coordinates = np.array([[row - center[0], col - center[0]] # Coordinate operation
        for row in range(len(self.number_shape)) # Gets row index
        for col in range(len(self.number_shape)) # Gets col index
        if self.number_shape[row][col] == 1]) # Checks for positive placement

        convert_array = np.array([[0,-1],[1,0]]) # Rotational matrices $\theta=\frac{\pi}{2}$ (LaTeX)

        translated_matrices = np.array([((convert_array @ coord_row) + center) for coord_row in centered_coordinates]).astype(int)

        print(translated_matrices)
        for coord in translated_matrices: tetrominoes_array[coord[0]][coord[1]] = 1

        self.number_shape = list(tetrominoes_array)
        self.render_shape = self.number_convert()
        #print(tetrominoes_array)



        print(f"{tetrominoes_array}\n")
        #print(f"{tetrominoes_array * convert_array}")