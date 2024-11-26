from dataStructures import TETROMINOES, COLOR
from tetrisBlock import block as bk

# Imported libraries
import numpy as np
import random

'''
The class object used to represent tetrominoes objects used to play tetris.

----------
Attributes
----------
random_key :    A dictionary key used to access a tetrominoes shape matrices. |String|

number_type :   A 2D list with a typically structure of a 4x4 matrices on 1s & 0s, to define the shape of the tetrominoes. | list[[4x4]] |

color :         Color do the tetrominoes based upon the shape. | String |

number_shape :  A dictionary key used to access a tetrominoes shape matrices. | String |

block_size :    Size of the block on each tetrominoes, one pixel larger then the gird size. | int |

render_shape :  4x4 matrices that resembles self.number_shape, but is made of Object(1) & None(0). | list[[4x4]] |

position :      The top left position of where the self.render_shape matrices appears in the tetris game surface grid. |[int, int]|

static :        Is the tetrominoes object is no longer moving and is slated to be decomposed into staticlly rendered blocks. |boolean|

preview_shape : The object matrices image of the shape when flipped prior to commitment to new orientation. | list[[4x4]] |

block_location: A list of where each block in the tetrominoes exist in the grid. | List[[],[],...,[]] |

plumbed:        If the player has made the tetrominoes plummet within a small fraction of time. | boolean |

'''

class tetrominoes:
    def __init__(self, block_size, spawn):
        self.random_key = random.choice(list(TETROMINOES.keys()))
        self.color = COLOR[self.random_key]
        self.number_shape = TETROMINOES[self.random_key]
        self.block_size = block_size + 1
        self.render_shape = self.number_convert()
        self.position = spawn
        self.static = False # If the tetromino is not moving
        self.preview_shape = [] # An image of the shape when flipped prior to commit
        self.block_locations = []; self.update_blocks() # An array where each block exists
        self.plumbed = False # If the tetrominoes has plummeted


    '''
    number_convert
    -------------
    Converts number matrices to object matrices. (0, 1) -> (None, tetrisBlock)
    '''
    def number_convert(self):
        return [[None if x == 0 else bk(self.block_size, self.color) for x in row] for row in self.number_shape]


    '''
    update_blocks
    -------------
    Updates the location of the blocks in the 4x4 matrices adding only the tetrominoes blocks to coordinates list.
    '''
    def update_blocks(self):
        self.block_locations = []
        for y, row in enumerate(self.render_shape):
            for x, block in enumerate(row):
                if block != None: self.block_locations.append((y,x))

    '''
    update_blocks
    -------------
    Flips the block in the tetrominoes by 90 degrees through coordinate vector rotation transformation. (Linear algebra)
    '''
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
