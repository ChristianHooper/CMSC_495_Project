from dataStructures import TETROMINOES, COLOR
from tetrisBlock import block as bk
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
