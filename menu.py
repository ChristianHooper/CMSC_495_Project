import pygame as pg
import dataStructures as ds
from button import Button

def menu(window, clock, window_size):

    running_menu = True
    large_font = ds.FONTS['default_large'] # File path to custom font: if possible add later (https://www.dafont.com/)
    title_text = large_font.render('G5-Tetris', True, ds.COLOR['white']) # Title text attributes
    title_position = title_text.get_rect(center=(window_size[0]/2, window_size[1]/10)) # Position of where text will render

    game_button = Button( # Defines button that starts single player tetris game
                    position=(window_size[0]/2, window_size[1]/3),
                    button_color=ds.COLOR['green'],
                    text_color=ds.COLOR['red'],
                    font=large_font,
                    text='Start Game',
                    hover_color=ds.COLOR['white'],
                    )

    settings_button = Button( # Defines button that navigates to user settings
                position=(window_size[0]/2, window_size[1]/2),
                button_color=ds.COLOR['green'],
                text_color=ds.COLOR['red'],
                font=large_font,
                text='Settings',
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

        '''
        # Load sound
        click_sound = pygame.mixer.Sound('click.wav')

        # Play sound on click
        if start_button.is_clicked(mouse_pos):
            click_sound.play()
            return GAME
        '''

        # Render order
        window.fill(ds.COLOR['black'])
        window.blit(title_text, title_position)
        game_button.render(window)
        settings_button.render(window)
        pg.display.flip()
