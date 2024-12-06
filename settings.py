import pygame as pg
import dataStructures as ds
from button import Button
from background import Background

'''
settings
-------------
Configures and runs the settings menu ad it associated variables.
'''
def settings(window, clock, window_size):

    running_menu = True # Set running loop for main menu
    medium_font = ds.FONTS['default_medium']

    back_button = Button( # Defines button that navigates back to the main menu
                    position=(window_size[0]/2, window_size[1]/1.2),
                    button_color=ds.COLOR['vapor_blue'],
                    text_color=ds.COLOR['powder_pink'],
                    font=medium_font,
                    text='Main Menu',
                    hover_color=ds.COLOR['mono_white'],
                    text_outline=True,
                    inflate=[16, 16]
                    )

    while running_menu: # Main menu loop
        for event in pg.event.get():
            if event.type == pg.QUIT: return None # Checks for exit

            # Listener for player button click on main menu
            elif event.type == pg.MOUSEBUTTONDOWN:

                if event.button == 1: # Left-click button
                    mouse_position = pg.mouse.get_pos()
                    if back_button.clicked(mouse_position): return ds.GAME_STATE['menu'] # If the back button is clicked

        # Render order
        window.fill(ds.COLOR['glass_purple']) # Renders background color
        back_button.render(window) # Render button
        pg.display.flip() # Updates contents of window
