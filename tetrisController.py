from settingsController import settings_conduit as sc
from dataStructures import COLOR, GUI_GRID
import tetrominoes as tm
import guiController as gui
import pygame as pg

'''
An object that controls the game logic and rendering of a single game of tetris
----------
Attributes
----------
tetris_grid : Creates a 2D list to hold tetrominoes' block objects, length is twice the width. |tetrisBlock.block|

border : Defines the width and length of the border around the tetris frame by count the number of grid square on each axis. |[int, int]|

window_size : Pixel size of the render window.

tetris_surface_size : Defines the pixel width and length of the tetris game surface based upon grid width and length including border. |tuple(int, int)|

tetris_block_size : Defines the block size for the tetris game surface and tetrominoes. |int|

tetris_coordinates : A 2D list of pixel coordinates [x, y] which are the render points mapped to the self.tetris_grid parameter. |[[int][int]]|

tetris_surface : Surface of the tetris game object, where contented is rendered to before it is blit to the render window. |pg.surface.Surface|

centering : Pixel coordinate position for centering the tetris game window object. |tuple(int, int)|

tetris_grid_color : The render color of the tetris game surface. |(int, int, int)|

static_block : List of blocks after they are no longer apart of a tetromino, used for rendering and placing into self.tetris_grid upon update. |set(tetrisBlock.block)|

current_tetrominoes : The current falling tetrominoes object that player controls. |tetrominoes.tetrominoes|

next_tetrominoes : The next tetrominoes to spawn after self.current_tetrominoes becomes static. |tetrominoes.tetrominoes|

render_points : A 2D list of indices render points mapped to self.tetris_grid |[[row,col]]|

line_cleared : Temporarily holds the row index for a lines to be cleared |[int,]|

game_over : Boolean that defines if game is over. |boolean|
'''


class TetrisController:
    def __init__(self, window_size, border, agents):
        # Initialize attributes
        self.tetris_grid = [[None for _ in range(sc['grid_size'])] for _ in range((sc['grid_size'] * 2))]
        self.tetris_width = len(self.tetris_grid[0])
        self.tetris_length = len(self.tetris_grid)
        self.gen = agents # Number of players apart of the game-loop
        self.border = [x * gui.grid_square for x in border]
        self.window_size = window_size

        self.tetris_surface_size = (
            ((self.window_size[1]/1) - (self.border[1] * 2) - (self.border[0] * 2)) / 2, # x-axis
            (self.window_size[1]) - (self.border[1] * 2)) # y-axis

        self.tetris_block_size = self.tetris_surface_size[0] / sc['grid_size']
        self.tetris_coordinates = self.create_coordinates()
        self.tetris_surface = pg.Surface(self.tetris_surface_size)
        self.centering = [gui.grid[int(GUI_GRID / 2)][0][0] - (self.tetris_surface_size[0] / 2*self.gen), self.border[1]] # Defines general position of the grid
        if self.gen > 1: self.centering[0] -= gui.grid_square/self.gen
        self.tetris_grid_color = COLOR['black']
        self.tetris_surface_color = (100, 100, 100)

        # Transition set the position for all past static tetrominoes locations for copying over to tetris grid upon calling update_grid()
        self.static_blocks = set()

        # Initialize the current and next tetromino
        self.current_tetrominoes = self.generate_tetrominoes() # Create current user interactive tetrominoes
        self.next_tetrominoes = self.generate_tetrominoes() # Creates the next tetrominoes to

        self.render_points = [] # Tetris grid points the render on the screen
        self.line_cleared = False
        self.game_over = False
        self.cleared_rows = []

        self.animation_interval = 500 # Length of tetrominoes animation
        self.collision_list = [] # List of colliding block used in flip function
        self.transfer = False # If the current tetrominoes is slated for static block conversion



    # Defines pixel coordinates [x, y] which are the render points mapped to the self.tetris_grid
    # Indices of the grid match indices of self.tetris_grid
    # This means that indices of self.tetris grid can call indices of grid to get pixel render locations and vise-versa
    def create_coordinates(self):
        grid = [] # Whole 2D grid object to be return as the self.tetris_coordinates
        for row_n in range(len(self.tetris_grid) + 1):
            if row_n > 0:
                grid.append(holder)
            holder = [] # Represents a single row at a time in grid
            for col_n in range(len(self.tetris_grid[0])): # Appends pixel coordinate points to row
                holder.append([int(self.tetris_block_size * row_n), int(self.tetris_block_size * col_n)])
        return grid


    # Renders all contents of the tetris controller after game logic
    def render_tetris(self, window):
        self.tetris_surface.fill(self.tetris_surface_color) # Fills the tetris game object with set color
        self.update_grid() # Updates current object position prior to rendering
        self.render_tetrominoes() # Renders self.current_tetrominoes

        for line_row in range(len(self.tetris_coordinates)): # Renders horizontal grid lines
            if line_row > 0:
                pg.draw.aaline( # Draws horizontal line
                    self.tetris_surface,
                    self.tetris_grid_color,
                    (0, self.tetris_coordinates[line_row][0][0]),
                    (self.tetris_surface_size[0], self.tetris_coordinates[line_row][0][0]),
                    blend=1,
                )

        for line_col in range(len(self.tetris_coordinates)): # Renders vertical grid lines
            if line_col > 0:
                pg.draw.aaline( # Draws vertical line
                    self.tetris_surface,
                    self.tetris_grid_color,
                    (self.tetris_coordinates[line_col][0][0], 0),
                    (self.tetris_coordinates[line_col][0][0], self.tetris_surface_size[1]),
                )

        #self.render_next_tetromino(window) # Display the next tetromino
        window.blit(self.tetris_surface, self.centering) # Imposes tetris game surface and lal drawings onto game window


    def generate_tetrominoes(self): # Creates a new tetrominoes object composed of tetrisBlock objects
        return tm.tetrominoes(
            self.tetris_block_size, # Size of block in tetrominoes
            [3, 0]) # Spawn location, starting position

    # Calculates the score and line count when clearing lines
    def line_score(self, score, level):
        cleared = len(self.cleared_rows)
        self.cleared_rows = [] # Deletes clear row marker
        match cleared:
            case 1: return (40 * (level + cleared), 1)
            case 2: return (100 * (level + cleared), 2)
            case 3: return (300 * (level + cleared), 3)
            case 4: return (1200 * (level + cleared), 4)

    # Updates state of the tetris grid and render list
    # Transcribes tetrominoes shape into the self.tetris_grid
    def update_grid(self):
        self.render_points = [] # Empties old render points
        self.tetris_grid = [[None for x in range(sc['grid_size'])] for y in range(sc['grid_size'] * 2)] # Empties self.tetris_grid to be recalculated

        for block in self.static_blocks: # Sets prior tetrominoes blocks back into the grid
            self.tetris_grid[block.position[1]][block.position[0]] = block
            self.render_points.append(block.position)

        # Loops to check and update tetrominoes grid
        for row in range(len(self.tetris_grid)): # Row indices
            for col in range(len(self.tetris_grid[row])): # Column indices

                # Checks tetrominoes shape against y-axis of grid
                if row >= self.current_tetrominoes.position[1] and self.current_tetrominoes.position[1] + len(self.current_tetrominoes.render_shape) > row:

                    # Checks tetrominoes shape against x-axis of grid
                    if col >= self.current_tetrominoes.position[0] and self.current_tetrominoes.position[0] + len(self.current_tetrominoes.render_shape[0]) > col:

                        # Defines the object and indices on the self.tetris_grid the tetromino will be placed
                        grid_square = self.current_tetrominoes.render_shape[row - self.current_tetrominoes.position[1]][
                            col - self.current_tetrominoes.position[0]]

                        # Places object into self.tetris_grid
                        if grid_square is not None:
                            self.tetris_grid[row][col] = grid_square
                            self.render_points.append([col, row])  # Creates a list of indices for blocks to be rendered on the grid


    # Passes over tetrominoes object and renders the blocks defined grid coordinates in update_grid()
    def render_tetrominoes(self):
        for x in self.render_points: # Gets render coordinates for grid one-by-one
            block = self.tetris_grid[x[1]][x[0]] # Defines singular block from the tetris grid
            # Places grid pixel coordinates for rendering on tetris grid into the block objects position on the x&y-axis
            block.position = x # Sets the indices for the position of the block in the tetris grid
            block.small_block.x = self.tetris_coordinates[x[1]][x[0]][1] # Sets render location on block on x-axis
            block.small_block.y = self.tetris_coordinates[x[1]][x[0]][0] # Sets render location on block on y-axis
            pg.draw.rect(self.tetris_surface, block.color, block.small_block) # Draws block onto tetris surface before being blit


    def render_next_tetromino(self, window, position): # Renders the coming tetrominoes before being placed in the controllable self.current_tetrominoes
        for y, row in enumerate(self.next_tetrominoes.render_shape):
            for x, block in enumerate(row):
                if block: # Renders grab-bag tetrominoes
                    pos_x = int((position[0]/self.gen + x * self.tetris_block_size/self.gen))
                    pos_y = int(position[1] + y * self.tetris_block_size/self.gen)
                    pg.draw.rect(window, block.color,
                    ((pos_x, pos_y), # Window position of render
                    ((self.tetris_block_size/self.gen)+1, (self.tetris_block_size/self.gen)+1)))


    def gravity(self): # Used for constant gravity pull and player induced block movement
        for block_position in self.current_tetrominoes.block_locations: # Gets the position of the blocks in the 4x4 matrices of the current tetrominoes
            # Transfers matrices coordinates to grid coordinates based upon current tetrominoes
            grid_position = [block_position[0] + self.current_tetrominoes.position[1], block_position[1] + self.current_tetrominoes.position[0]]
            if grid_position[0] > len(self.tetris_grid)-2 or ( # Checks tetris grid depth
            self.tetris_grid[grid_position[0]+1][grid_position[1]] in self.static_blocks): # Checks for existing static blocks
                self.transfer = True # If collision is found begins tetrominoes transmission to static blocks
                return
        self.current_tetrominoes.position[1] += 1


    # Checks the x&y-axis for collisions, and increments the movement based upon direction input
    def movement(self, x_change=0, y_change=0):
        if x_change != 0 and not self.check_collision(offset_x=x_change): # Horizontal check
            self.current_tetrominoes.position[0] += x_change

        # DEPRECATED ---------------------------------------------------------------------------------------------------
        #if self.check_collision(offset_y=y_change) != True: # Checks to see if y-axis increase will lead to a collision
            #self.current_tetrominoes.position[1] += y_change
        # DEPRECATED ---------------------------------------------------------------------------------------------------

        elif self.transfer: # If collision detected with tetris game frame or another block
            self.current_tetrominoes.static = True # Halts the self.current_tetrominoes object
            self.settle_tetromino() # Converts self.current tetrominoes object into blocks to be rendered
            self.clear_lines() # Check to see if block line needs to be cleared from self.tetris_gris and self.static_blocks
            self.current_tetrominoes = self.next_tetrominoes # Switches previewed tetrominoes for current controllable tetrominoes
            self.next_tetrominoes = self.generate_tetrominoes() # Generates a new preview tetrominoes
            if self.check_collision(): # Checks to see if game is over
                self.game_over = True
                print(f'GameOver: {self.game_over}')
                return
            self.transfer = False

    # Checks if the tetrominoes object collides with the tetris game frame of block object, checks x&y-axis separately
    def check_collision(self, offset_x=0, offset_y=0):
        for y, row in enumerate(self.current_tetrominoes.render_shape): # Defines row list 0-3, get respective row number through y (render shape 4x4)
            for x, block in enumerate(row): # Get block value at x of a row in the 4x4 shape
                if block: # Checks to see if index is a block object or is None

                    new_x = x + self.current_tetrominoes.position[0] + offset_x # Sets new x-axis position for checking x-axis collision
                    new_y = y + self.current_tetrominoes.position[1] + offset_y  # Sets new y-axis position for checking y-axis collision

                    # Check to see if the tetrominoes in a new position would meet any out-of-bounds conditions
                    if new_y >= len(self.tetris_grid) or new_x < 0 or new_x >= len(self.tetris_grid[0]): # Tetris object collision checks
                        return True # If collision is detected

                    if (self.tetris_grid[new_y][new_x] in self.static_blocks): return True
        return False # If collision False


    # Checks if the tetrominoes object collides with the tetris game frame of block object, used to check flipping conditions
    def flipping_collision(self):
        for y, row in enumerate(self.current_tetrominoes.preview_shape): # Defines row list 0-3, get respective row number through y (render shape 4x4)
            for x, block in enumerate(row): # Get block value at x of a row in the 4x4 shape
                if block: # Checks to see if index is a block object or is None
                    x_pos = x + self.current_tetrominoes.position[0]# Sets new x-axis position for checking x-axis collision
                    y_pos = y + self.current_tetrominoes.position[1]# Sets new y-axis position for checking y-axis collision
                    if y_pos >= len(self.tetris_grid) or y_pos < 0 or x_pos < 0 or x_pos >= len(self.tetris_grid[0]) or (
                    self.tetris_grid[y_pos][x_pos] in self.static_blocks): self.collision_list.append([y_pos, x_pos])


    # Called when flipping the current tetrominoes object, checking for possible collision on flip
    def tetrominoes_flipping(self):
        self.current_tetrominoes.flip() # Create an image of the tetrominoes if flipped
        self.flipping_collision() # Test image for collision
        apriori_position = self.current_tetrominoes.position # Tetrominoes position before any movement action
        apriori_shape = self.current_tetrominoes.render_shape # Tetrominoes shape before any movement action
        apriori_block_location = self.current_tetrominoes.block_locations

        for position in self.collision_list: # Moves tetrominoes based upon flip position
            # Left wall collision
            if position[1] == -2: self.current_tetrominoes.position[0] += 2; break
            if position[1] == -1: self.current_tetrominoes.position[0] += 1; break
            # Right wall collision
            if position[1] == self.tetris_width: self.current_tetrominoes.position[0] -= 1
            if position[1] == self.tetris_width+1: self.current_tetrominoes.position[0] -= 1; break
            # Floor collision
            if position[0] == self.tetris_length: self.current_tetrominoes.position[1] -= 1
            if position[0] == self.tetris_length+1: self.current_tetrominoes.position[1] -= 1; break

        # Assigns flipped image of tetrominoes as current tetrominoes
        self.current_tetrominoes.render_shape = self.current_tetrominoes.preview_shape
        self.current_tetrominoes.update_blocks() # Updates where the array that holds the block location in the 4x4 matrices

        if self.check_collision(): # Checks to make sure tetrominoes hasn't flipped into another static block
            self.current_tetrominoes.position = apriori_position # Reset to previous position
            self.current_tetrominoes.render_shape = apriori_shape # Reset to previous shape
            self.current_tetrominoes.block_locations = apriori_block_location

        self.collision_list = []


    # Divides current self.current_tetrominoes once it becomes static into a persistent block list for logic and rendering
    def settle_tetromino(self):
        for y, row in enumerate(self.tetris_grid):
            for x, block in enumerate(row):
                if block:
                    self.static_blocks.add(block)


    # Checks entire grid and clear line moving current block down by one
    def clear_lines(self):
        self.cleared_rows = [index for index, row in enumerate(self.tetris_grid) if all(row)] # Tag rows to be clear

        if self.cleared_rows: # If there are lines to be cleared
            for row_index in self.cleared_rows: # Gets row
                for block in self.tetris_grid[row_index]: # Gets block
                    if block in self.static_blocks:
                        self.static_blocks.remove(block) # Deleted block from render list and grid

        # Physics for moving all block down one line after cleared lines
        for index in self.cleared_rows:
            for row in range(0,(index)): # Loops through all rows from top to clear row
                for block in self.tetris_grid[row]:
                    if block != None:
                        block.position[1] += 1 # Moves block object down by one grid square
        #self.cleared_rows = [] # Deletes clear row marker


