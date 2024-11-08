from settingsController import settings_conduit as sc  # Settings controller
from soundController import SoundController  # Import SoundController
from tetrisController import TetrisController  # Updated class name
from guiElement import element
import pygame as pg
import dataStructures as ds
from dataStructures import COLOR
import numpy as np
import guiController as gui


def one_player(window, clock, window_size, sound_controller):

    ts = TetrisController(window_size, [0, 1])  # TetrisController class, game logic & rendering

    grab_bag = element(window, # GUI element for preview oncoming tetrominoes
                    gui.grid[4][1], # Location of grab-bag
                    [gui.grid_square*5, gui.grid_square*7], # Width & Height of grab-bag
                    fill_color=(128,128,128),
                    border_size=[gui.grid_square/8, gui.grid_square/8], # Border width
                    border_color=(64,64,64), # Border color
                    text='Next',
                    font_position=[gui.grid_square, gui.grid_square/4]
    ); next_position = [grab_bag.position[0], grab_bag.position[1]+(gui.grid_square*2)] # The pixel position the new next_tetrominoes object will render


    score_ui = element(window, # GUI element for preview oncoming tetrominoes
                    gui.grid[4][10], # Location of score element
                    [gui.grid_square*5, gui.grid_square*3], # Width & Height of score element
                    fill_color=(128,128,128),
                    border_size=[gui.grid_square/8, gui.grid_square/8], # Border width
                    border_color=(64,64,64),
                    text='Score', # Rendered text
                    font_position=[gui.grid_square/2, gui.grid_square/4] # Font position on surface
    ); score_subsurface = score_ui.surface.subsurface(0, 0, score_ui.bounds[0]-gui.grid_square, gui.grid_square) # Box current score will render
    subsurface_position = [score_ui.position[0]+gui.grid_square/2, int(score_ui.position[1]+(gui.grid_square*1.75))] # Score box window pixel position


    line_ui = element(window, # GUI element for viewing current line count
                    gui.grid[4][15], # Location of line counter element
                    [gui.grid_square*5, gui.grid_square*3], # Width & Height of line counter element
                    fill_color=(128,128,128),
                    border_size=[gui.grid_square/8, gui.grid_square/8], # Border width
                    border_color=(64,64,64), # Border color
                    text='Line',
                    font_position=[gui.grid_square, gui.grid_square/4]
    ); line_subsurface = line_ui.surface.subsurface(0, 0, line_ui.bounds[0]-gui.grid_square, gui.grid_square) # Box current line count will render
    line_position = [line_ui.position[0]+gui.grid_square/2, int(line_ui.position[1]+(gui.grid_square*1.75))] # Line counter element box pixel position

    level_ui = element(window, # GUI element for viewing current line count
                    gui.grid[4][20], # Location of line counter element
                    [gui.grid_square*5, gui.grid_square*3], # Width & Height of line counter element
                    fill_color=(128,128,128),
                    border_size=[gui.grid_square/8, gui.grid_square/8], # Border width
                    border_color=(64,64,64), # Border color
                    text='Level',
                    font_position=[gui.grid_square/2, gui.grid_square/4]
    ); level_subsurface = level_ui.surface.subsurface(0, 0, level_ui.bounds[0]-gui.grid_square, gui.grid_square) # Box current line count will render
    level_position = [level_ui.position[0]+gui.grid_square/2, int(level_ui.position[1]+(gui.grid_square*1.75))] # Line counter element box pixel position


    running = True
    sound_controller.play_bgm()  # Play background music when game starts

    gravity_timer = 0  # Timer for gravity control
    gravity_interval = ds.GRAVITY_SPEED # Milliseconds delay for each gravity step

    # Game-loop
    while running:

        gravity_timer += clock.get_time() # Update gravity timing... meow?!?
        # print(f"Gravity Timer: {gravity_timer}")  # Debugging: Check gravity timer

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            elif event.type == pg.KEYDOWN: # Checks for a key press event

                if event.key == pg.K_LEFT and ts.current_tetrominoes.static == False: # Left key press
                    #print("Left key pressed") # Debugging line
                    ts.movement(x_change=-1)

                elif event.key == pg.K_RIGHT and ts.current_tetrominoes.static == False: # Right key press
                    #print("Right key pressed") # Debugging line
                    # Move right logic
                    ts.movement(x_change=1)

                elif event.key == pg.K_DOWN and ts.current_tetrominoes.static == False: # Down key press
                    #print("Down key pressed") # Debugging line
                    # Move down logic
                    ts.movement(y_change=1)

                elif event.key == pg.K_UP and ts.current_tetrominoes.static == False: # Up key press
                    #print("Rotate key pressed")  # Debugging line
                    # Rotate logic
                    ts.current_tetrominoes.flip()

        # Gravity-based movement
        if gravity_timer >= gravity_interval:
            ts.movement(y_change=1) # Move tetromino down on y-axis
            ts.update_grid() # Updates grid of mechanics and rendering based upon movement changes
            gravity_timer = 0  # Resets the timer
            #ts.delete_lines()
            #for row in ts.tetris_grid: print(f"{row}") # Prints a terminal based tetris grid

        # Rendering
        window.fill(COLOR['black'])
        gui.render_grid(window) # Render GUI placement grid tool
        ts.render_tetris(window) # Render the entire tetris game frame

        grab_bag.blit_update(window)

        score_ui.blit_update(window)
        score_subsurface.fill((200, 200, 245))
        window.blit(score_subsurface, subsurface_position)

        line_ui.blit_update(window)
        line_subsurface.fill((200, 200, 245))
        window.blit(line_subsurface, line_position)

        level_ui.blit_update(window)
        level_subsurface.fill((200, 200, 245))
        window.blit(level_subsurface, level_position)

        ts.render_next_tetromino(window, next_position) # Display the next tetromino
        pg.display.flip()
        #ts.gravity()

        clock.tick(ds.FPS_CAP['default']) # Adheres game ticks to set FPS
        #print("Game loop running...")  # Debugging: Game loop running

    sound_controller.stop_bgm()
    print("Exiting game loop")

