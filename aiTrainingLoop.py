# Import files
import settingsController as sc
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

'''
main
-------------
Used to set up the training run for the genetic AI complex.
'''
def main(): # Render Parameter, starting function for AI training
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

'''
ai_training
-------------
Starts simulation runs for training AI complex.
'''
def ai_training(window, clock, window_size, sound_controller):
    agents = 2 # Constraining factor for multiplayer
    tst = TetrisController(window_size, [0, 1], agents, player_two=True)  # TetrisController class, player two
    score = [0, 0]; level = [1, 1]; line_count = [0, 0] # Score information

    ai = aiComplex() # Creates the complex of AI agents to be trained

#/////////////////////////////////////////////////////////////////[Training Functions]///////////////////////////////////////////////////////////////////
    '''
    pause_loop
    -------------
    Function called to pause training during training-loop.
    '''
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

    '''
    selection_movement
    -------------
    Places out the selected move for the AI, from the selected COMMANDS sequence.
    '''
    def selection_movement(COMMANDS):
        gravity_timer = 0  # Timer for gravity control
        gravity_interval = 50 # Milliseconds delay for each gravity step
        read = False
        while True:

            if not tst.current_tetrominoes.static and read == False: # Run each ACTION in COMMANDS sequence
                for ACTION in COMMANDS:

                    # Rotate logic player two
                    if ACTION == 'ROTATE': # Up key press
                        tst.tetrominoes_flipping()

                    if ACTION == 'LEFT': # Move left
                        tst.movement(x_change=-1)

                    if ACTION == 'RIGHT': # Move right
                        tst.movement(x_change=1)

                    if ACTION == 'DOWN': # Move down
                        tst.gravity()
                        score[1] += 1

                    tst.movement() # Checks if tetrominoes should move to a static block
                read = True # Marks COMMANDS sequence as read

        #////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

            # if gravity_timer >= gravity_interval: # If set slows down training

            # Defines if the game reaches an end state will running through selected move
            if not tst.game_over:
                if tst.transfer == True:
                    tst.movement()
                    tst.transfer = False
                    tst.save_state()
                    read = False
                    return

                # Move tetromino down on y-axis
                tst.movement(y_change=1)
                tst.gravity()

            if tst.cleared_rows: # Second player line cleared
                scores = tst.line_score(score[1], line_count[1]) # Calculates new scores and lien count
                score[1] = score[1] + scores[1] # Sets new score
                line_count[1] = line_count[1] + line_count[1] # Sets new line count
                if line_count[1] - (10*(level[1])) >= 0:
                    level[1] = level[1] + 1

            tst.update_grid() # Updates grid of mechanics and rendering based upon movement changes
            window.fill(COLOR['black'])
            tst.render_tetris(window) # Render the entire tetris game frame
            pg.display.flip()
            clock.tick(1000)


#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    running = True # Sets uo the game loop for running a single COMMANDS sequence
    paused = False # If the game is paused
    game_over = True # Sets if the game has concluded for a single agent
    read = False # If movement ACTIONS from the COMMANDS sequence have been read

    chromosome = {} # Defines the current chromosome being evaluated
    move_list = [] # Lists of possible moves over one sequence
    gravity_timer = 0  # Timer for gravity control
    gravity_interval = 1 # Milliseconds delay for each gravity step

    SEQUENCE = ai.movement_sequence # Defines the sequence of all possible moves an agent can play

    agent_loop = True # Defines agent loop access
    age = 0
    movement_number = -1 # Holds the movement number of the agent in agent_loop

    rna.evolve_genome() # Transcribes entire empty genome framework in gene seed

#/////////////////////////////////////////////////////////////[AI-Loop]///////////////////////////////////////////////////////////////////////
    '''
    Main recursive loop ran during AI the training phase.
    '''
    for generation in range(ai.generations): # Outer-loop that runs epochs for AI training

        if generation != 0: # Skips breeding and mutating initial population
            ai.update_population(generation-1) # Adds ages to the previous pulling from gene seed
            ai.cross_breed(generation-1) # Breeds the latest generation
        print('GEN:', generation) # Tracks generation

        for agent in range(len(ai.population)): # The loop used to evaluate a single agent
            agents = 2 # Resets agent for loop
            tst = TetrisController(window_size, [0, 1], agents, player_two=True) # Creates a new game for the agent to play
            tst.save_state() # Saves the starting grid state for initial agent_loop to recall starting state
            chromosome = ai.population[agent] # Gets current chromosome of Ai agent to evaluate
            agent_loop = True # Set agent loop to true from play
            age = 0 # Default age ever agents start with

            while agent_loop: # Loops though a game single agents game of tetris
                if movement_number != -1: # Not ran initially as it selected the best move for a tetrominoes piece after all possible move are considered
                    move_array = np.array(move_list) # Defines the score for call possible moves in COMMANDS sequence
                    #print(move_array); print()
                    selected_score = np.max(move_array) # Finds optimal move-set; selects list of COMMANDS sequence, gets highest scores
                    #pprint(selected_score); print()
                    selected_index = np.random.choice(np.where(move_array == selected_score)[0]) # Selects optimal move; single COMMANDS sequence
                    #pprint(selected_index); print()
                    tst.load_state() # Load previous state, so the agent can make the move
                    selection_movement(ai.movement_sequence[selected_index]) # Runs the optimal selected COMMANDS sequence

                movement_number += 1 # Tracks agents move number; mirrors the COMMANDS index in SEQUENCE
                move_list = [] # Resets move list for sequencing
                age += 1 # Increase age after move is made


                for COMMANDS in SEQUENCE: # Loops through all possible move-sets
                    tst.load_state() # Resets game for optimal movement search
                    if not tst.game_over: running = True # # Sets running state for a single COMMANDS

                    while running: # Runs single COMMANDS sequence
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

                                if ACTION == 'ROTATE': # Rotate
                                    tst.tetrominoes_flipping()

                                if ACTION == 'LEFT': # Move left
                                    tst.movement(x_change=-1)

                                if ACTION == 'RIGHT': # Move right
                                    tst.movement(x_change=1)

                                if ACTION == 'DOWN': # Move down
                                    tst.gravity()
                                    score[1] += 1

                                tst.movement() # Checks if tetrominoes should move to a static block
                            read = True # Marks COMMANDS sequence as having been read

                        #////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

                        # Gravity-based movement
                        if gravity_timer >= gravity_interval: # Used to slow down AI training; or use clock ticks

                            if not tst.game_over: # Checks if game is over
                                if tst.transfer == True:
                                    read = False
                                    running = False
                                    tst.movement(y_change=1)
                                    move_list.append(tst.score(chromosome)) # Scores possible movement choice

                                 # Movement y-axis
                                tst.movement(y_change=1)
                                tst.gravity()

                            if tst.cleared_rows: # Second player line cleared
                                scores = tst.line_score(score[1], line_count[1]) # Calculates new scores and lien count
                                score[1] = score[1] + scores[1] # Sets new score
                                line_count[1] = line_count[1] + line_count[1] # Sets new line count
                                if line_count[1] - (10*(level[1])) >= 0:
                                    level[1] = level[1] + 1

                            tst.update_grid() # Updates grid of mechanics and rendering based upon movement changes
                            gravity_timer = 0  # Resets the timer

                        # Runs after an agent play a game and have run into a game over state, copies chromosome over to gene seed
                        if agents > 1 and tst.game_over:
                            window.fill(COLOR['black'])
                            tst.render_tetris(window) # Render the entire tetris game frame
                            pg.display.flip()

                            chromosome['Age'] = age # Writes age to gene seed
                            print(chromosome['Age'])
                            rna.load_population_dna(generation) # Load current population DNA
                            rna.population_dna[agent] = chromosome # Places current chromosome into population DNA
                            rna.transfer_dna(generation) # Transcribes new chromosome and population to gene seed

                            # Resets loops for additional agents
                            agent_loop = False
                            running = False
                            agents = 0
                            break
                        #window.fill(COLOR['black'])
                        #tst.render_tetris(window) # Render the entire tetris game frame
                        #pg.display.flip()
                        clock.tick(100000) # Sets clock rate

    rna.population_dna = ai.population # Updates final population
    rna.transfer_dna(ai.generations-1) # Transcribes final population
    rna.evolve_genome() # Transcribes all generational DNA into gene seed file; failsafe
    print("EVOLVED")

if __name__ == '__main__':
    main()
