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

import settingsController as sc
import random

def population_genesis(population_size):
    population = []
    for _ in range(population_size):
        chromosome = { # Set of chromosomal weights
            'Smoothness': random.uniform(-1, 1), # Variance between heights
            'Heights':    random.uniform(-1, 1), # Sum of all heights
            'Maximum':    random.uniform(-1, 1), # Tallest stack
            'Lines':      random.uniform(-1, 1), # Number of lines that could be cleared
            'Holes':      random.uniform(-1, 1), # Empty spaces between blocks
            'Shifting':   random.uniform(-1, 1)  # If holes are open to be shifted into
        }
        population.append(chromosome)
    return population




