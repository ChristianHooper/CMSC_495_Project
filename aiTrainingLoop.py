import settingsController as sc
#from settingsController import settings_conduit as sc  # Settings controller
from soundController import SoundController  # Import SoundController
from tetrisController import TetrisController  # Updated class name
from guiElement import element
from button import Button
import dataStructures as ds
from dataStructures import COLOR
import guiController as gui
from geneticAi import aiComplex
import rna

# Import libraries
from pprint import pprint
import pygame as pg
import numpy as np
import random
import copy
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
    #ts = TetrisController(window_size, [0, 1], agents)  # TetrisController class, game logic & rendering
    tst = TetrisController(window_size, [0, 1], agents, player_two=True)  # TetrisController class, player two
    score = [0, 0]; level = [1, 1]; line_count = [0, 0]

    ai = aiComplex()

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


    # Places out the selected move for the AI, from the selected COMMANDS sequence
    def selection_movement(COMMANDS):
        gravity_timer = 0  # Timer for gravity control
        gravity_interval = 50 # Milliseconds delay for each gravity step
        read = False
        while True:

            #gravity_timer += clock.get_time()
        # Second player movement logic
        #if not tst.current_tetrominoes.static and not tst.game_over:
            if not tst.current_tetrominoes.static and read == False:
                for ACTION in COMMANDS:

                    # Rotate logic player two
                    if ACTION == 'ROTATE': # Up key press
                        tst.tetrominoes_flipping()
                    # Move left logic player two
                    if ACTION == 'LEFT': # Left key press
                        tst.movement(x_change=-1)
                    if ACTION == 'RIGHT': # Right key press
                        tst.movement(x_change=1)
                    # Move down logic player two
                    if ACTION == 'DOWN': # Down key press
                        tst.gravity()
                        score[1] += 1
                        #tst.movement()
                    tst.movement() # Checks if tetrominoes should move to a static block
                read = True
            #read = True
        #////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
            # Gravity-based movement
            # if gravity_timer >= gravity_interval:

            if not tst.game_over:
                if tst.transfer == True:
                    #tst.current_tetrominoes = tst.next_tetrominoes
                    tst.movement()
                    tst.transfer = False
                    tst.save_state()
                    read = False
                    return

                tst.movement(y_change=1) # Move tetromino down on y-axis
                tst.gravity()

            if tst.cleared_rows: # Second player line cleared
                scores = tst.line_score(score[1], line_count[1]) # Calculates new scores and lien count
                score[1] = score[1] + scores[1] # Sets new score
                line_count[1] = line_count[1] + line_count[1] # Sets new line count
                if line_count[1] - (10*(level[1])) >= 0:
                    level[1] = level[1] + 1

            tst.update_grid() # Updates grid of mechanics and rendering based upon movement changes
            #gravity_timer = 0  # Resets the timer
            window.fill(COLOR['black'])
            #gui.render_grid(window) # Render GUI placement grid tool
            #ts.render_tetris(window) # Render the entire tetris game frame
            tst.render_tetris(window) # Render the entire tetris game frame
            pg.display.flip()
            clock.tick(1000)


#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    running = True
    paused = False # If the game is paused
    game_over = True
    read = False # If movement ACTIONS from the COMMANDS sequence have been read

    chromosome = {} # Defines the current chromosome being evaluated
    move_list = [] # Lists of possible moves over one sequence
    gravity_timer = 0  # Timer for gravity control
    gravity_interval = 1 # Milliseconds delay for each gravity step

    SEQUENCE = ai.movement_sequence # Defines the sequence of all possible moves an agent can play

    agent_loop = True # Defines agent loop access
    age = 0
    movement_number = -1 # Holds the movement number of the agent in agent_loop

    rna.evolve_genome()


#/////////////////////////////////////////////////////////////[Game-Loop]///////////////////////////////////////////////////////////////////////
    for generation in range(ai.generations):

        if generation != 0:
            ai.update_population(generation-1) # Adds ages to the previous population
            ai.cross_breed(generation-1)
            ai.mutation(generation-1)
        print('GEN:', generation)

        #pprint(rna.entire_genome)
        #print(ai.population)
        #population = ai.update_population(generation) # Updates so population pulls from new genetic data

        for agent in range(len(ai.population)):

            agents = 2
            tst = TetrisController(window_size, [0, 1], agents, player_two=True)
            tst.save_state() # Saves the starting grid state for initial agent_loop
            #pprint(ai.population)
            chromosome = ai.population[agent]
            agent_loop = True
            age = 0

            while agent_loop: # Loops though a game single agents game of tetris
                if movement_number != -1: # Not run on the first agents move, but run every move after
                    move_array = np.array(move_list) # Movement score list for a sequence
                    #pprint(move_array); print()
                    selected_score = np.max(move_array) # Finds optimal move-set; selects list of COMMANDS sequence
                    #pprint(selected_score); print()
                    selected_index = np.random.choice(np.where(move_array == selected_score)[0]) # Selects optimal move; single COMMANDS sequence
                    #pprint(selected_index); print()
                    tst.load_state() # Load previous state
                    selection_movement(ai.movement_sequence[selected_index]) # Runs the optimal selected COMMANDS sequence

                movement_number += 1 # Tracks agents move number; mirrors the COMMANDS index in SEQUENCE
                move_list = [] # Resets move list for sequencing
                age += 1


                for COMMANDS in SEQUENCE: # Loops through all possible move-sets
                    tst.load_state() # Resets game for optimal movement search
                    if not tst.game_over: running = True # # Sets running state for a single COMMANDS

                    while running: # 'Game-loop' to run single COMMANDS

                        gravity_timer += clock.get_time() # Update gravity timing

                        for event in pg.event.get(): # Event listener for quitting
                            if event.type == pg.QUIT:
                                return None

                            elif event.type == pg.KEYDOWN: # Checks for a key press event
                                if event.key == pg.K_SPACE: # Pauses game
                                    paused = True # Sets pause condition to true
                                    paused = pause_loop(paused) # Sets pause condition to false

                        #/////////////////////////////////////////////////////////////[AI Movement]///////////////////////////////////////////////////////////////////////

                        # Second player movement logic, is tetrominoes is in play and COMMANDS sequence hasn't been read
                        if not tst.current_tetrominoes.static and not tst.game_over and read == False:
                            for ACTION in COMMANDS: # Pull a single ACTION to be run from the COMMANDS sequence
                                # Rotate logic player two
                                if ACTION == 'ROTATE': # Up key press
                                    tst.tetrominoes_flipping()

                                # Move left logic player two
                                if ACTION == 'LEFT': # Left key press
                                    tst.movement(x_change=-1)

                                if ACTION == 'RIGHT': # Right key press
                                    tst.movement(x_change=1)

                                # Move down logic player two
                                if ACTION == 'DOWN': # Down key press
                                    tst.gravity()
                                    score[1] += 1
                                    #tst.movement()

                                '''
                                if keys[pg.K_RSHIFT]: # Up key press
                                    if key_press_timer_two >= key_press_interval_two:
                                        tst.plummet()
                                        tst.update_grid()
                                        key_press_timer_two = 0
                                        plummet_timer_two = 0
                                '''

                                tst.movement() # Checks if tetrominoes should move to a static block

                            read = True # Marks COMMANDS sequence as having been read

                        #////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

                        # Gravity-based movement
                        if gravity_timer >= gravity_interval:

                            if not tst.game_over:
                                if tst.transfer == True:
                                    read = False
                                    move_list.append(tst.score(chromosome)) # Scores possible movement choice
                                    running = False

                                tst.movement(y_change=1) # Move tetrominoes down on y-axis
                                tst.gravity()

                            if tst.cleared_rows: # Second player line cleared
                                scores = tst.line_score(score[1], line_count[1]) # Calculates new scores and lien count
                                score[1] = score[1] + scores[1] # Sets new score
                                line_count[1] = line_count[1] + line_count[1] # Sets new line count
                                if line_count[1] - (10*(level[1])) >= 0:
                                    level[1] = level[1] + 1

                            tst.update_grid() # Updates grid of mechanics and rendering based upon movement changes
                            gravity_timer = 0  # Resets the timer

                        # Rendering
                        #window.fill(COLOR['black'])
                        #tst.render_tetris(window) # Render the entire tetris game frame
                        #pg.display.flip()

                        if agents > 1 and tst.game_over: # TODO: Transfer function to next agent; wrong placement

                            window.fill(COLOR['black'])
                            tst.render_tetris(window) # Render the entire tetris game frame
                            pg.display.flip()
                            chromosome['Age'] = age
                            print(chromosome['Age'])

                            rna.load_population_dna(generation) # Load current population DNA

                            rna.population_dna[agent] = chromosome # Places current chromosome into population DNA

                            rna.transfer_dna(generation) # Transcribes new chromosome and population in entire genome

                            agent_loop = False
                            running = False
                            agents = 0
                            break

                        clock.tick(100000) # Adheres game ticks to set FPS
                        #clock.tick()
                        #print(f"SPF: {clock.tick() / 1000}", end="\r")
    #ai.cross_breed(generation) # Final breeding protocol
    #ai.mutation
    rna.population_dna = ai.population
    rna.transfer_dna(ai.generations-1)
    print("EVOLVED{{{{{{}}}}}}")
    rna.evolve_genome() # Transcribes all generational DNA into gene seed file
if __name__ == '__main__':
    main()