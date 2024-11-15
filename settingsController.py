import pygame as np
import json
import os

SETTINGS_FILE = 'saved_data.json' # Path to JSON save data, immutable
settings_conduit = {} # Global variable for function access

'''
load_setting
-------------
Used to load the default setting into game to initialize the controller.
'''
def load_settings(): # Loads JSON setting into game
    global settings_conduit
    if os.path.exists(SETTINGS_FILE): # Checks data file
        print("JSON")
        with open(SETTINGS_FILE, 'r') as data: # Reads file, defines object

            try: settings_conduit = json.load(data) # JSON to dictionary
            except json.JSONDecodeError: # Error path
                print("!<[JSON Format Error]>!")
                load_default_settings() # Loads presets if error occurs

'''
save_settings
-------------
Used to transfer modified values in the setting dictionary to JSON for data persistence.
'''
def save_settings(): # Saves controller changes to JSON file
    global settings_conduit
    with open(SETTINGS_FILE, 'w') as data: # Write file, defines object
        json.dump(settings_conduit, data, indent=4) # Dump setting to JSON object


'''
load_default_settings
-------------
Sets the settings dictionary to the default settings, for errors.
'''
def load_default_settings(): # Loads defaults settings for game
    global settings_conduit
    settings_conduit = {
    "screen_size": "1024x768",
    "fps_cap": 60,
    "grid_size": 12,
    "aspect_ratio": 2,
    "scores": {
        "first": 0,
        "second": 0,
        "third": 0,
        "fourth": 0,
        "fifth": 0
    }
}

load_settings() # Initialize controller