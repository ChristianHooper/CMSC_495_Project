import dataStructures as ds
import copy
from pprint import pprint
import pygame as np
import json
import os

SETTINGS_FILE = 'geneSeed.json' # Path to JSON save data, immutable
population_dna = [{} for _ in range(ds.POPULATION)] # Basic storage for population
# Basic storage for entire genome, copies so it isn't creating a reference
entire_genome = [copy.deepcopy(population_dna) for _ in range(ds.GENERATIONS)]
current_generation = 0

'''
load_setting
-------------
Used to load the default setting into game to initialize the controller.
'''
def load_genome(): # Loads all DNA from JSON gene seed
    global entire_genome
    if os.path.exists(SETTINGS_FILE):  # Check if data file exists
        with open(SETTINGS_FILE, 'r') as data:  # Read file
            try:
                entire_genome = json.load(data)  # Load JSON into dictionary
            except json.JSONDecodeError:
                print("!<[JSON Format Error]>!")


def load_population_dna(generation): # Loads from population from gene seed
    global population_dna
    global entire_genome
    load_genome() # Gets current DNA data before making changes
    population_dna = entire_genome[generation] # Load JSON into dictionary


'''
transfer_dna
-------------
Used to transfer modified population DNA in the geneSeed for data persistence.
'''
def transfer_dna(generation):
    global entire_genome
    global population_dna
    entire_genome[generation] = population_dna
    evolve_genome()


# Copies entire genome into geneSeed file
def evolve_genome():
    global entire_genome
    with open(SETTINGS_FILE, 'w') as data: # Write data back to the JSON file
        json.dump(entire_genome, data, indent=4)

#evolve_genome() # Places an empty data structure into file
