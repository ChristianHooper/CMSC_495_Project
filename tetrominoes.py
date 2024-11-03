from dataStructures import TETROMINOES, COLOR
from tetrisBlock import block as bk
import numpy as np
import random


class tetrominoes:
    '''

    ----------
    Attributes
    ----------
    '''

    def __init__(self, block_size, spawn):
        self.number_shape = TETROMINOES[random.choice(list(TETROMINOES.keys()))] # Shape of tetrominoes
        self.color = COLOR[random.choice(list(COLOR.keys()))]
        self.block_size = block_size+1  # Adjust rendering size
        self.render_shape = self.number_convert()
        self.position = spawn # Where tetrominoes first spawns

        self.static = True

    def number_convert(self):
        print(self.number_shape)
        print([[ None if x==0 else bk(self.block_size, self.color) for x in row] for row in self.number_shape])
        return [[ None if x==0 else bk(self.block_size, self.color) for x in row] for row in self.number_shape]


    def movement(self, direction): # Called for movement
        print()

    def flip(self):
        print()

    def excelerate(self):
        print()

    def block_search(self):
        print()