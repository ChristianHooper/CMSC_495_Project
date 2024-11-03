from settingsController import settings_conduit as sc
from dataStructures import COLOR, GUI_GRID
import tetrominoes as tm
import guiController as gui
import pygame as pg

class TetrisController:
    def __init__(self, window_size, border):
        # Initialize attributes
        self.tetris_grid = [[None for _ in range(sc['grid_size'])] for _ in range(sc['grid_size'] * 2)]
        self.border = [x * gui.grid_square for x in border]
        self.window_size = window_size

        self.tetris_surface_size = (
            (self.window_size[1] - (self.border[1] * 2) - (self.border[0] * 2)) / 2,
            self.window_size[1] - (self.border[1] * 2),
        )
        self.tetris_block_size = self.tetris_surface_size[0] / sc['grid_size']
        self.tetris_coordinates = self.create_coordinates()
        self.tetris_surface = pg.Surface(self.tetris_surface_size)
        self.centering = (gui.grid[int(GUI_GRID / 2)][0][0] - (self.tetris_surface_size[0] / 2), self.border[1])
        self.tetris_grid_color = COLOR['black']
        self.tetris_surface_color = (100, 100, 100)

        # Initialize the current and next tetromino
        self.current_tetrominoes = self.generate_tetrominoes()
        self.next_tetrominoes = self.generate_tetrominoes()

        self.render_points = []
        self.line_cleared = False
        self.game_over = False

    def create_coordinates(self):
        grid = []
        for row_n in range(len(self.tetris_grid) + 1):
            if row_n > 0:
                grid.append(holder)
            holder = []
            for col_n in range(len(self.tetris_grid[0])):
                holder.append([int(self.tetris_block_size * row_n), int(self.tetris_block_size * col_n)])
        return grid

    def render_tetris(self, window):
        self.tetris_surface.fill(self.tetris_surface_color)
        self.update_grid()
        self.render_tetrominoes()

        # Render the game grid lines
        for line_row in range(len(self.tetris_coordinates)):
            if line_row > 0:
                pg.draw.aaline(
                    self.tetris_surface,
                    self.tetris_grid_color,
                    (0, self.tetris_coordinates[line_row][0][0]),
                    (self.tetris_surface_size[0], self.tetris_coordinates[line_row][0][0]),
                    blend=1,
                )
        for line_col in range(len(self.tetris_coordinates)):
            if line_col > 0:
                pg.draw.aaline(
                    self.tetris_surface,
                    self.tetris_grid_color,
                    (self.tetris_coordinates[line_col][0][0], 0),
                    (self.tetris_coordinates[line_col][0][0], self.tetris_surface_size[1]),
                )

        # Display the next tetromino
        self.render_next_tetromino(window)

        window.blit(self.tetris_surface, self.centering)

    def generate_tetrominoes(self):
        print("Generating Tetromino shape")
        return tm.tetrominoes(self.tetris_block_size, [3, 0])  # Start from row 0 for downward movement

    def update_grid(self):  # [row]=y, [col]=x
        self.render_points = []
        self.tetris_grid = [[None for x in range(sc['grid_size'])] for y in range(sc['grid_size'] * 2)]

        # Loops to check and update tetrominoes grid
        for row in range(len(self.tetris_grid)):
            for col in range(len(self.tetris_grid[row])):
                if row >= self.current_tetrominoes.position[1] and self.current_tetrominoes.position[1] + len(
                        self.current_tetrominoes.render_shape[1]
                ) > row:
                    if col >= self.current_tetrominoes.position[0] and self.current_tetrominoes.position[0] + len(
                            self.current_tetrominoes.render_shape[0]
                    ) > col:
                        grid_square = self.current_tetrominoes.render_shape[row - self.current_tetrominoes.position[1]][
                            col - self.current_tetrominoes.position[0]
                            ]
                        if grid_square is not None:
                            self.tetris_grid[row][col] = grid_square
                            self.render_points.append(
                                [col, row])  # Creates a list of indices for blocks to be rendered on the grid

    def render_tetrominoes(self):
        for x in self.render_points:
            block = self.tetris_grid[x[1]][x[0]]
            block.small_block.x = self.tetris_coordinates[x[0]][x[1]][0]
            block.small_block.y = self.tetris_coordinates[x[0]][x[1]][1]
            pg.draw.rect(self.tetris_surface, block.color, block.small_block)

    def render_next_tetromino(self, window):
        for y, row in enumerate(self.next_tetrominoes.render_shape):
            for x, block in enumerate(row):
                if block:
                    pos_x = self.window_size[0] - 150 + x * self.tetris_block_size
                    pos_y = 50 + y * self.tetris_block_size
                    pg.draw.rect(window, block.color, (pos_x, pos_y, self.tetris_block_size, self.tetris_block_size))

    def gravity(self):
        print(f"Gravity applied: Tetromino position before move: {self.current_tetrominoes.position}")
        if not self.check_collision(offset_y=1):
            self.current_tetrominoes.position[1] += 1
            print(f"Tetromino position after move: {self.current_tetrominoes.position}")
        else:
            print("Tetromino settled")
            self.settle_tetromino()
            self.clear_lines()
            self.current_tetrominoes = self.next_tetrominoes
            self.next_tetrominoes = self.generate_tetrominoes()
            if self.check_collision():
                self.game_over = True

    def check_collision(self, offset_x=0, offset_y=0):
        for y, row in enumerate(self.current_tetrominoes.render_shape):
            for x, block in enumerate(row):
                if block:
                    new_x = x + self.current_tetrominoes.position[0] + offset_x
                    new_y = y + self.current_tetrominoes.position[1] + offset_y
                    if new_y >= len(self.tetris_grid) or new_x < 0 or new_x >= len(self.tetris_grid[0]) or (
                        new_y >= 0 and self.tetris_grid[new_y][new_x] is not None
                    ):
                        return True
        return False

    def settle_tetromino(self):
        for y, row in enumerate(self.current_tetrominoes.render_shape):
            for x, block in enumerate(row):
                if block:
                    new_x = x + self.current_tetrominoes.position[0]
                    new_y = y + self.current_tetrominoes.position[1]
                    if new_y >= 0:
                        self.tetris_grid[new_y][new_x] = block

    def clear_lines(self):
        cleared_rows = [index for index, row in enumerate(self.tetris_grid) if all(row)]
        if cleared_rows:
            for row_index in cleared_rows:
                del self.tetris_grid[row_index]
                self.tetris_grid.insert(0, [None] * len(self.tetris_grid[0]))
            self.line_cleared = True
        else:
            self.line_cleared = False