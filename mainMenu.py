from settingsController import settings_conduit as sc
import guiController as gui
import pygame as pg
import dataStructures as ds
from button import Button

def main_menu(window, clock, window_size):

    running_menu = True
    large_font = ds.FONTS['default_large'] # File path to custom font: if possible add later (https://www.dafont.com/)
    title_text = large_font.render('G5-Tetris', True, ds.COLOR['white']) # Title text attributes
    title_position = title_text.get_rect(center=gui.grid[16][3]) # Position of where text will render

    game_button = Button( # Defines button that starts single player tetris game
                    position = gui.grid[16][6], # grid (x, y)
                    button_color=ds.COLOR['green'],
                    text_color=ds.COLOR['red'],
                    font=large_font,
                    text='Start Game', # Text
                    hover_color=ds.COLOR['white'],
                    )

    settings_button = Button( # Defines button that navigates to user settings
                position=gui.grid[16][9], # grid (x, y)
                button_color=ds.COLOR['green'],
                text_color=ds.COLOR['red'],
                font=large_font,
                text='Settings', # Text
                hover_color=ds.COLOR['white'],
                )

    tutorial_button = Button( # Defines button that navigates to tutorial
            position=gui.grid[16][12], # grid (x, y)
            button_color=ds.COLOR['green'],
            text_color=ds.COLOR['red'],
            font=large_font,
            text='Tutorial', # Text
            hover_color=ds.COLOR['white'],
            )

    exit_button = Button( # Defines button exit button
            position=gui.grid[16][15], # grid (x, y)
            button_color=ds.COLOR['green'],
            text_color=ds.COLOR['red'],
            font=large_font,
            text='Exit', # Text
            hover_color=ds.COLOR['white'],
            )

    while running_menu:
        for event in pg.event.get():
            if event.type == pg.QUIT: return None

            # Listener for player button click on main menu
            elif event.type == pg.MOUSEBUTTONDOWN:

                if event.button == 1: # Left-click button
                    mouse_position = pg.mouse.get_pos()
                    if game_button.clicked(mouse_position): return ds.GAME_STATE['p1_game']
                    if settings_button.clicked(mouse_position): return ds.GAME_STATE['settings']
                    if tutorial_button.clicked(mouse_position): return ds.GAME_STATE['tutorial']
                    if exit_button.clicked(mouse_position): return None


        # Render order
        window.fill(ds.COLOR['black'])
        window.blit(title_text, title_position)
        game_button.render(window)
        settings_button.render(window)
        tutorial_button.render(window)
        gui.render_grid(window)
        exit_button.render(window) # Render grid window for element placement
        pg.display.flip()