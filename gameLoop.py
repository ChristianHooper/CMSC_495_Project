from settingsController import settings_conduit as sc  # Settings controller
import pygame as pg
import dataStructures as ds
from dataStructures import COLOR
import numpy as np
from tetrisController import TetrisController  # Updated class name
import guiController as gui
from soundController import SoundController  # Import SoundController


def one_player(window, clock, window_size, sound_controller):
    ts = TetrisController(window_size, [0, 1])  # Use TetrisController class here

    running = True
    sound_controller.play_bgm()  # Play background music when game starts

    gravity_timer = 0  # Timer for gravity control
    gravity_interval = ds.GRAVITY_SPEED # Milliseconds delay for each gravity step

    # Game-loop
    while running:

        gravity_timer += clock.get_time() # Update gravity timing
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
            #for row in ts.tetris_grid: print(f"{row}") # Prints a terminal based tetris grid

        # Rendering
        window.fill(COLOR['black'])
        gui.render_grid(window) # Render GUI placement grid tool
        ts.render_tetris(window) # Render the entire tetris game frame
        pg.display.flip()
        #ts.gravity()

        clock.tick(ds.FPS_CAP['default']) # Adheres game ticks to set FPS
        #print("Game loop running...")  # Debugging: Game loop running

    sound_controller.stop_bgm()
    print("Exiting game loop")

