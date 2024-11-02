from settingsController import settings_conduit as sc
import dataStructures as ds
import pygame as pg

'''
guiController is a development tool for aligning GUI elements to a dynamic screen wide grid.
The main object calls are made to: 'grid', 'grid_square', and the function 'render_grid'

grid : Is a 3-D list the holds each point of the grid which spans the length and width of the screen render size.
        Default grid size 32 grid square across x-axis, a call to the center of the grid would look like:
        gui.grid[16][8] returning [512, 256] which can then be used to position object within the grid.

grid_square : Holds the calculated width/length on one grid square, used to create GUI elements

render_grid : Development tool for setting gui elements, creates a dot grid in conjunction with 'grid' array object.

n_grid = : Returns the number of grid squares on the x & y-axis [x-axis_number, y-axis_number]
'''

grid = []
grid_square = 0
n_grid = []

def init():
    global grid
    global grid_square

    # Grid layout over entire screen, used for placing GUI elements [[all x-axis], [all y-axis]]
    grid_y = [row_n * (ds.SCREEN_SIZE[sc['screen_size']][1]/ (ds.GUI_GRID+1)) for row_n in range(ds.GUI_GRID+1)] # Divides screen length into grid
    grid_x = [cols_n * (ds.SCREEN_SIZE[sc['screen_size']][1]/ (ds.GUI_GRID+1)) for cols_n in range(ds.GUI_GRID+1)] # Divides screen width into grid
    #grid_x = [col_n * (window_size[1]/ (sc['grid_size']+1)) for col_n in range(int(window_size[0]/(window_size[1]/(sc['grid_size']+1))))] # x-axis added generation from y-axis height

    offset = ((ds.SCREEN_SIZE[sc['screen_size']][0] - grid_x[-1]) / (len(grid_x)-1)) # Calculates each grid offset to align to screen margins on x&y-axis

    # Adds offset to each grid square
    grid_x = [x + (n * offset) for n, x in enumerate(grid_x)]
    grid_y = [y + (n * offset) for n, y in enumerate(grid_y)]
    grid_square = grid_x[1] # Defines the dimensions of a single grid square
    n_grid = [len(grid_x)-1, int(ds.SCREEN_SIZE[sc['screen_size']][1]/grid_square)] # Calculates grid length & width totals

    # Compose all points for the grid object for gui referencing, default width 32 grid squares
    for row_n in range(len(grid_y)):
        if row_n > 0: grid.append(holder)
        holder=[]
        for col_n in range(len(grid_x)):
            holder.append([grid_x[row_n], grid_y[col_n]])

# Development tool for setting gui elements, creates a dot grid in conjunction with grid array object.
def render_grid(window):
        for row_n in range(len(grid)): # Grid controller test
            for col_n in range(len(grid[0])):
                pg.draw.circle(window, ds.COLOR['red'],grid[row_n][col_n], 1) # Render dot grid

init() # Initializes controller
