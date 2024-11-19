'''
Steps:
1. Initial Population
2. Defining fitness function
3. Selection
4. Crossover & mutation
5. Repeat steps 3-4

[Initial Population]
Chromosome: Random string of actions
Gene: A Single action

[Fitness Function]
Create a function that selects the fittest Chromosome sequences.

[Crossover]
After Chromosome selection combine chromosome sequences.

[Mutation]
Have it so some percentage chance the a gene could mutate in the chromosome.

Each generation will pull chromosome weights into JSON file, will be rewritten each generation.
Final generation will copy values will be copied in to be used or discarded.

'''

import numpy as np
import settingsController as sc
import random

class aiComplex:
    def __init__(self, size=16):
        self.grid_width = sc.settings_conduit['grid_size'] # Width of tetris grid
        self.grid_width = sc.settings_conduit['grid_size']*2 # Length of tetris grid
        self.population_size = size # AI complex population size
        self.population = self.population_genesis(self.population_size) # Population weights
        self.movement_sequence = self.possible_movement() # All possible movement sequence commands
        #print(self.movement_sequence)

    def population_genesis(self, population_size):
        population = []
        for _ in range(population_size):
            chromosome = { # Set of chromosomal weights
                'Smoothness': random.uniform(-1, 1), # Variance between heights
                'Heights':    random.uniform(-1, 1), # Sum of all heights
                'Maximum':    random.uniform(-1, 1), # Tallest stack
                'Minimum':    random.uniform(-1, 1), # Lowest spot
                'Lines':      random.uniform(-1, 1), # Number of lines that could be cleared
                'Pit':        random.uniform(-1, 1)  # Number of 3 sided space
            }
            population.append(chromosome)
        return population

    # Creates an array of list of all possible moves
    def possible_movement(self):
        holder_column = [] # Holds left side of movement sequences
        horizontal_max = int((sc.settings_conduit['grid_size']/2)) # Max left and right movement commands
        rotation_max = 4 # Max number of rotations

        for movement_left in range(horizontal_max): # Left-side

            for rotation in range(0, rotation_max): # Places rotation commands
                hold = ['ROTATE']*rotation
                holder_column.append(hold)

            for index in holder_column: index.append('LEFT') # Places left commands

        mirror_holder = holder_column[::-1] # Reflects list for seamless processing from one end of the grid to the other

        # Swaps 'LEFT' command for 'Right' command
        mirror_holder = [['RIGHT' if 'LEFT' in position else position for position in row]for row in mirror_holder]

        # Add middle column rotation
        for middle_rotation in range(0, rotation_max):
            hold = ['ROTATE']*middle_rotation
            holder_column.append(hold)

        return holder_column + mirror_holder # Returns entire movement sequence commands





