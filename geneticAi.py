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
import dataStructures as ds
import settingsController as sc
from pprint import pprint
import copy
import rna
import random

class aiComplex:
    def __init__(self, left_off=False):
        self.generations = ds.GENERATIONS # How many generation the model is trained
        self.grid_width = sc.settings_conduit['grid_size'] # Width of tetris grid
        self.grid_width = sc.settings_conduit['grid_size']*2 # Length of tetris grid
        self.population_size = ds.POPULATION # AI complex population size
        self.population = self.population_genesis(self.population_size) # Current dna population
        #else: rna.load_dna(); self.population = rna.evolution_process # Evolution from last ran point
        #print(self.population)
        self.movement_sequence = self.possible_movement() # All possible movement sequence commands
        self.selected = []
        #print(self.movement_sequence)

    def population_genesis(self, population_size):
        population = []
        for _ in range(population_size): # REMOVED 'Heights':    random.uniform(0, 1), # Sum of all heights
            chromosome = { # Set of chromosomal weights
                'Smoothness': random.uniform(0, 1), # Variance between heights
                'Maximum':    random.uniform(0, 1), # Tallest stack
                'Minimum':    random.uniform(0, 1), # Lowest spot
                'Lines':      random.uniform(0, 1), # Number of lines that could be cleared
                'Pit':        random.uniform(0, 1),  # Number of 3 sided space
                'Hole':       random.uniform(0, 1), # Percentage of hole compared to normal blocks
                'Age':   0
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



    # Updates population genetic information for the next generation
    def update_population(self, generation): self.population = rna.entire_genome[generation]; return self.population



    # Cross-breeds the current generation of agents
    def cross_breed(self, generation):
        #print('\n\nBREED')
        selection_size = 4 # int(self.population_size/2) # Number defines selection size for breeding
        self.selected = None
        age_list = np.zeros(len(self.population))
        self.selected = [] # Holds array of indices of selected parents
        population_rebirth = []
        #print('population rebirth start:', population_rebirth)
        # Population data from gene seed, self.population should mirror is update_population() called
        for index, chromosome in enumerate(self.population):
            age_list[index] = self.population[index]['Age']
        #print('age list: ', age_list)
        selected_ages = np.partition(age_list, -selection_size)[-selection_size:] # Finds highest values
        selected_ages.sort()
        #print('selected ages:', selected_ages)

        for parent in selected_ages: self.selected.append(int(np.where(age_list == parent)[0][0])) # Finds the index of highest values and converts to a int list


        print('BREED self.select: ', self.selected)
        for individual in self.selected: population_rebirth.append(self.population[individual]) # Places successful genes in new generation list for transferring
        selection_range = len(self.selected)
        #print('selection range: ', selection_range)
        # Mating-loop
        for lordosis in range(0, selection_range): # Define mating range
            for group in range(selection_range-1, lordosis, -1): # Defines mate
                female = self.population[lordosis]
                male = self.population[group]
                child = { # Child of mates
                    'Smoothness':(male['Smoothness'] + female['Smoothness']) / 2, # REMOVED: 'Heights':   (male['Heights'] + female['Heights']) / 2,
                    'Maximum':   (male['Maximum'] + female['Maximum']) / 2,
                    'Minimum':   (male['Minimum'] + female['Minimum']) / 2,
                    'Lines':     (male['Lines'] + female['Lines']) / 2,
                    'Pit':       (male['Pit'] + female['Pit']) / 2,
                    'Hole':      (male['Pit'] + female['Pit']) / 2,
                    'Age':       int((male['Age'] + female['Age']) / 2)
                }
                population_rebirth.append(child) # Add child to next generation population
        #print('AP REBIRTH:',)
        #pprint(self.population)
        self.population = population_rebirth # Updates population for next generation

        #print('POST REBIRTH:',)
        #pprint(self.population)

        rna.population_dna = self.population # Places current chromosome into population DNA

        rna.transfer_dna(generation+1) # Transcribes new chromosome and population in entire genome

        #print('\nPopulation:')



    # Selects agents indices to fill remaining birth slots and mutates a single gene
    def mutation(self, generation):
        #print('MUTATE')
        attribute_list = ['Smoothness', 'Maximum', 'Minimum', 'Lines', 'Pit', 'Hole']
        #print('self.selected: ', self.selected)
        mutants = self.selected[-(self.population_size - len(self.population)):] # 12 to be replace with self.population_size TODO
        #print('mutants:', mutants)
        pprint(self.population)
        for mutant in mutants:
            if mutant < 10:
                selected = copy.deepcopy(self.population[mutant]) # Asexual reproduction
                for point in range(random.randint(1,4)):
                    selected[random.choice(attribute_list)] += random.uniform(-0.1, 0.1) # Mutates gene
                    print('Point-Mutation')

                self.population.append(selected) # Updates population for next generation
        rna.population_dna = self.population # Places current chromosome into population DNA
        rna.transfer_dna(generation+1) # Transcribes new chromosome and population in entire genome
        #pprint(self.population[generation])






