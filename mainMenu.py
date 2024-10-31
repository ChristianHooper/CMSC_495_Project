from settingsController import settings_conduit as sc
import pygame as pg
import dataStructures as ds
from button import Button

def main_menu(window, clock, window_size):

   # y = int((window_size[1]/ sc['grid_size']))
   #x = int(window_size[0]/(window_size[0]/ sc['grid_size']))

    '''
    Grid placement is a test, will be located in grid_controller,py soon
    '''
    # Grid layout over entire screen, used for placing GUI elements [[all x-axis], [all y-axis]]
    grid_y = [row_n * (window_size[1]/ sc['grid_size']) for row_n in range(sc['grid_size'])] # y-axis
    grid_x = [col_n * (window_size[1]/ sc['grid_size']) for col_n in range(int(window_size[0]/(window_size[1]/sc['grid_size']))+1)] # x-axis


    running_menu = True
    large_font = ds.FONTS['default_large'] # File path to custom font: if possible add later (https://www.dafont.com/)
    title_text = large_font.render('G5-Tetris', True, ds.COLOR['white']) # Title text attributes
    title_position = title_text.get_rect(center=(window_size[0]/2, window_size[1]/10)) # Position of where text will render

    game_button = Button( # Defines button that starts single player tetris game
                    position=(window_size[0]/2, window_size[1]/3), # (x, y)
                    button_color=ds.COLOR['green'],
                    text_color=ds.COLOR['red'],
                    font=large_font,
                    text='Start Game', # Text
                    hover_color=ds.COLOR['white'],
                    )

    settings_button = Button( # Defines button that navigates to user settings
                position=(window_size[0]/2, window_size[1]/2),
                button_color=ds.COLOR['green'],
                text_color=ds.COLOR['red'],
                font=large_font,
                text='Settings', # Text
                hover_color=ds.COLOR['white'],
                )

    tutorial_button = Button( # Defines button that navigates to tutorial
            position=(window_size[0]/2, window_size[1]/1.5),
            button_color=ds.COLOR['green'],
            text_color=ds.COLOR['red'],
            font=large_font,
            text='Tutorial', # Text
            hover_color=ds.COLOR['white'],
            )

    exit_button = Button( # Defines button exit button
            position=(window_size[0]/2, window_size[1]/1.2),
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
        exit_button.render(window)
        for row_n in range(len(grid_y)): # Grid controller test
            for col_n in range(len(grid_x)):
                pg.draw.circle(window, ds.COLOR['red'],[grid_x[col_n], grid_y[row_n]], 1)

        pg.display.flip()
