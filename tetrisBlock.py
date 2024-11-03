
import pygame as pg

class block:
    def __init__(self, block_size, color):
        self.position = (0, 0)
        #print("BLOCKSIZE: ", block_size)
        self.small_block = pg.Rect((self.position[0], self.position[1], block_size, block_size))
        self.block_size = block_size
        self.color = color