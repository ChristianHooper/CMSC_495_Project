import settingsController as sc
import guiController as gui
import pygame as pg
import dataStructures as ds
from button import Button
import math

'''
main_menu
-------------
Configures and runs the main menu sequence the player is initial presented with when the game starts.
'''
def main_menu(window, clock, window_size):

    # Animation variables
    animation_time = 0
    stretch = 128
    increase = 8

    running_menu = True
    large_font = ds.FONTS['default_large'] # File path to custom font: if possible add later (https://www.dafont.com/)
    title_text = ds.FONTS['title_font'].render('G5-Tetris', True, ds.COLOR['white']) # Title text attributes
    title_position = title_text.get_rect(center=gui.grid[16][3]) # Position of where text will render

    game_button = Button( # Defines button that starts single player tetris game
                    position = gui.grid[16][7], # grid (x, y)
                    button_color=ds.COLOR['green'],
                    text_color=ds.COLOR['red'],
                    font=large_font,
                    text='Single Player', # Text
                    hover_color=ds.COLOR['white'],
                    )

    game_button_two = Button( # Defines button that starts single player tetris game
                    position = gui.grid[16][10], # grid (x, y)
                    button_color=ds.COLOR['green'],
                    text_color=ds.COLOR['red'],
                    font=large_font,
                    text='Multiplayer', # Text
                    hover_color=ds.COLOR['white'],
                    )

    game_button_ai = Button( # Defines button that starts single player tetris game
                position = gui.grid[16][13], # grid (x, y)
                button_color=ds.COLOR['green'],
                text_color=ds.COLOR['red'],
                font=large_font,
                text='AI Versus', # Text
                hover_color=ds.COLOR['white'],
                )

    settings_button = Button( # Defines button that navigates to user settings
                position=gui.grid[16][16], # grid (x, y)
                button_color=ds.COLOR['green'],
                text_color=ds.COLOR['red'],
                font=large_font,
                text='Settings', # Text
                hover_color=ds.COLOR['white'],
                )

    tutorial_button = Button( # Defines button that navigates to tutorial
            position=gui.grid[16][19], # grid (x, y)
            button_color=ds.COLOR['green'],
            text_color=ds.COLOR['red'],
            font=large_font,
            text='Tutorial', # Text
            hover_color=ds.COLOR['white'],
            )

    exit_button = Button( # Defines button exit button
            position=gui.grid[16][22], # grid (x, y)
            button_color=ds.COLOR['green'],
            text_color=ds.COLOR['red'],
            font=large_font,
            text='Exit', # Text
            hover_color=ds.COLOR['white'],
            )

    # Runs the main menu loop
    while running_menu:
        for event in pg.event.get():
            if event.type == pg.QUIT: return None

            # Listener for player button click on main menu
            elif event.type == pg.MOUSEBUTTONDOWN:

                if event.button == 1: # Left-click button

                    # One-players tetris game
                    mouse_position = pg.mouse.get_pos()
                    if game_button.clicked(mouse_position):
                        sc.settings_conduit['aspect_ratio']=1
                        sc.save_settings()
                        return ds.GAME_STATE['p1_game'] # Game state machine return

                    # Two-players tetris game
                    if game_button_two.clicked(mouse_position):
                        sc.settings_conduit['aspect_ratio']=2
                        sc.save_settings()
                        return ds.GAME_STATE['p1_game'] # Game state machine return

                    # AI versus tetris game
                    if game_button_ai.clicked(mouse_position):
                        sc.settings_conduit['aspect_ratio']=2
                        sc.save_settings()
                        return ds.GAME_STATE['ai'] # Game state machine return

                    if settings_button.clicked(mouse_position): return ds.GAME_STATE['settings'] # Leads to settings menu
                    if tutorial_button.clicked(mouse_position): return ds.GAME_STATE['tutorial'] # Leads to tutorial menu
                    if exit_button.clicked(mouse_position): return None # Exits game; Game state machine return

        animation_time += clock.get_time()
        alpha = (math.sin(animation_time/stretch) + 1) * (increase/2)
        title_text = pg.font.Font('resources/Gabato.ttf', int(164+alpha)).render('G5-Tetris', True, ds.COLOR['white']) # Title text attributes
        title_position = title_text.get_rect(center=gui.grid[16][3]) # Position of where text will render

        # Render order
        window.fill(ds.COLOR['black'])
        window.blit(title_text, title_position)
        game_button.render(window)
        game_button_two.render(window)
        game_button_ai.render(window)
        settings_button.render(window)
        tutorial_button.render(window)
        #gui.render_grid(window)
        exit_button.render(window) # Render grid window for element placement
        clock.tick(10)
        pg.display.flip()
