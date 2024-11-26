import pygame as pg
import dataStructures as ds
from button import Button

'''
settings
-------------
Configures and runs the settings menu ad it associated variables.
'''
def settings(window, clock, window_size):

    running_menu = True # Set running loop for main menu
    large_font = ds.FONTS['default_large'] # Sets default font for menu

    back_button = Button( # Defines button that navigates back to the main menu
                    position=(window_size[0]/1.2, window_size[1]/3),
                    button_color=ds.COLOR['green'],
                    text_color=ds.COLOR['red'],
                    font=large_font,
                    text='Main Menu',
                    hover_color=ds.COLOR['white'],
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
        window.fill(ds.COLOR['black']) # Renders background color
        back_button.render(window) # Render button
        pg.display.flip() # Updates contents of window