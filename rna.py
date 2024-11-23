import dataStructures as ds
from pprint import pprint
import pygame as np
import json
import os

SETTINGS_FILE = 'geneSeed.json' # Path to JSON save data, immutable
population_dna = {} # Global variable for function access
evolution_process = [[] for _ in range(ds.GENERATIONS)]
print(evolution_process)
current_generation = 0

'''
load_setting
-------------
Used to load the default setting into game to initialize the controller.
'''
def load_dna(): # Loads JSON setting into game
    global population_dna
    if os.path.exists(SETTINGS_FILE):  # Check if data file exists
        with open(SETTINGS_FILE, 'r') as data:  # Read file
            try:
                population_dna = json.load(data)  # Load JSON into dictionary
            except json.JSONDecodeError:
                print("!<[JSON Format Error]>!")


'''
save_settings
-------------
Used to transfer modified values in the setting dictionary to JSON for data persistence.
'''
def transfer_dna(generation): # Saves controller changes to JSON file
    global evolution_process
    global population_dna
    current_data = []
    '''
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as data:
            try:
                current_data = json.load(data)
            except json.JSONDecodeError:
                print("!<[JSON Decode Error]>!")
                current_data = []
    '''
    # Append the new data

    #current_data.append(population_dna)
    evolution_process[generation].append(population_dna)
    #pprint(evolution_process)

def evolution_data():
    global evolution_process
    with open(SETTINGS_FILE, 'w') as data: # Write data back to the JSON file
        json.dump(evolution_process, data, indent=4)

load_dna() # Initialize controller