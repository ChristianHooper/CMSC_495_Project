
import pygame as pg

'''
Creates the individual block object tetrominoes are composed from.

----------
Attributes
----------
position :     The (y, x) grid position of the block |[int, int]|
small_block :  The square surface object to be drawn when rendering. |pygame.rect|
block_size :   The size of the block, one pixel larger than the grid squares. |[int, int]|
decimate :     If the block is slated to be de destroyed. |boolean|
'''

class block:
    def __init__(self, block_size, color):
        self.position = [0, 0]
        #print("BLOCKSIZE: ", block_size)
        self.small_block = pg.Rect((self.position[0], self.position[1], block_size, block_size))
        self.block_size = block_size
        self.color = color
        self.decimate = False