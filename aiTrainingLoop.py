import settingsController as sc
#from settingsController import settings_conduit as sc  # Settings controller
from soundController import SoundController  # Import SoundController
from tetrisController import TetrisController  # Updated class name
from guiElement import element
from button import Button
import dataStructures as ds
from dataStructures import COLOR
import guiController as gui

# Import libraries
import pygame as pg
import numpy as np
import sys
import os


def main():
    # Render Parameter
    pg.init() # Initialize pygame
    os.environ['SDL_VIDEO_WINDOW_POS'] = '100,100' # Positions game window at (0, 0) Left-side of screen
    running = True # If game is running
    window_size = ds.SCREEN_SIZE[sc.settings_conduit['screen_size']] # Default window size (x, y)

    # Window display on GPU, dual buffer
    window = pg.display.set_mode(window_size, pg.HWSURFACE | pg.DOUBLEBUF)
    clock = pg.time.Clock() # Starts game clock
    pg.display.set_caption("G5-Tetris") # Group-Five-Tetris

    # Initialize Sound Controller
    sound_controller = SoundController()
    sound_controller.play_bgm()  # Start background music

    ai_training(window, clock, window_size, sound_controller) # Start simulation run


def ai_training(window, clock, window_size, sound_controller):

    agents = 2 # Constraining factor for multiplayer
    ts = TetrisController(window_size, [0, 1], agents)  # TetrisController class, game logic & rendering
    tst = TetrisController(window_size, [0, 1], agents, player_two=True)  # TetrisController class, player two
    score = [0, 0]; level = [1, 1]; line_count = [0, 0]


#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    # Function called to pause the game
    def pause_loop(pause):
        while pause: # Defines pause loop
            for event in pg.event.get(): # Check for game exit
                if event.type == pg.QUIT:
                    pause = False # Unpauses game

                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        pause = False # Unpauses game

            pause_text = ds.FONTS['default_large'].render("[Game Paused]", False, COLOR['white']) # Font object rendered for pausing game
            window.blit(pause_text, [gui.grid[16][10][0] - pause_text.get_width()/2 , gui.grid[16][10][1]]) # Centered font render
            pg.display.flip()
        return False # Sets pause condition to false with return

    running = True
    paused = False # If the game is paused
    game_over = True
    sound_controller.play_bgm()  # Play background music when game starts

    gravity_timer = 0  # Timer for gravity control
    key_press_timer = 0
    key_press_timer_two = 0
    gravity_interval = ds.GRAVITY_SPEED # Milliseconds delay for each gravity step
    key_press_interval = 100 # Milliseconds delay for each gravity step
    key_press_interval_two = 100 # Milliseconds delay for each gravity step
    pg.key.set_repeat(100, 100) # Allows for repeated movement calls when keys are held down, increase tetrominoes' speed

#/////////////////////////////////////////////////////////////[Game-Loop]///////////////////////////////////////////////////////////////////////

    # Game-loop
    while running:

        # Sets update timer variables
        gravity_timer += clock.get_time() # Update gravity timing
        key_press_timer += clock.get_time() # Update player one timer for key presses
        key_press_timer_two += clock.get_time() # Update player two timer for key presses

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            elif event.type == pg.KEYDOWN: # Checks for a key press event
                # Pauses game
                if event.key == pg.K_SPACE:
                    paused = True # Sets pause condition to true
                    paused = pause_loop(paused) # Sets pause condition to false

#/////////////////////////////////////////////////////////////[AI Movement]///////////////////////////////////////////////////////////////////////

        keys = pg.key.get_pressed()

        # Second player movement logic
        if not tst.current_tetrominoes.static and not tst.game_over:
            # Move left logic player two
            if keys[pg.K_LEFT]: # Left key press
                if key_press_timer_two >= key_press_interval_two:
                    tst.movement(x_change=-1)
                    key_press_timer_two = 0

            if keys[pg.K_RIGHT]: # Right key press
                if key_press_timer_two >= key_press_interval_two:
                    tst.movement(x_change=1)
                    key_press_timer_two = 0

            # Move down logic player two
            if keys[pg.K_DOWN]: # Down key press
                if key_press_timer_two >= key_press_interval_two:
                    tst.gravity()
                    score[1] += 1
                    key_press_timer_two = 0


            # Rotate logic player two
            if keys[pg.K_UP]: # Up key press
                if key_press_timer_two >= key_press_interval_two:
                    tst.tetrominoes_flipping()
                    key_press_timer_two = 0

            if keys[pg.K_RSHIFT]: # Up key press
                if key_press_timer_two >= key_press_interval_two:
                    tst.plummet()
                    tst.update_grid()
                    key_press_timer_two = 0
                    plummet_timer_two = 0

            tst.movement() # Checks if tetrominoes should move to a static block

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

        # Gravity-based movement
        if gravity_timer >= gravity_interval:
            for row in tst.tetris_grid: print(row)
            print()

            if not tst.game_over:
                tst.movement(y_change=1) # Move tetromino down on y-axis
                tst.gravity()

            if tst.cleared_rows: # Second player line cleared
                scores = tst.line_score(score[1], line_count[1]) # Calculates new scores and lien count
                score[1] = score[1] + scores[1] # Sets new score
                line_count[1] = line_count[1] + line_count[1] # Sets new line count
                if line_count[1] - (10*(level[1])) >= 0:
                    level[1] = level[1] + 1


            ts.update_grid() # Updates grid of mechanics and rendering based upon movement changes
            tst.update_grid() # Updates grid of mechanics and rendering based upon movement changes
            gravity_timer = 0  # Resets the timer
            key_press_timer = 0 # Resets the timer
            key_press_timer_two = 0

        # Rendering
        window.fill(COLOR['black'])
        gui.render_grid(window) # Render GUI placement grid tool
        ts.render_tetris(window) # Render the entire tetris game frame
        tst.render_tetris(window) # Render the entire tetris game frame
        pg.display.flip()

        if agents > 1 and ts.game_over and tst.game_over: conclude(game_over, 0); return None
        if ts.game_over and agents == 1: return None # Checks is game is over

        #clock.tick(ds.FPS_CAP['default']) # Adheres game ticks to set FPS
        print(f"SPF: {clock.tick() / 1000}", end="\r")
    sound_controller.stop_bgm()
    print("Exiting game loop")

if __name__ == '__main__':
    main()