import settingsController as sc
import guiController as gui
import pygame as pg
import dataStructures as ds
from tetrisController import TetrisController
from button import Button
from soundController import SoundController
import math
import random

'''
main_menu
-------------
Configures and runs the main menu sequence the player is initial presented with when the game starts.
'''
def main_menu(window, clock, window_size):

    # Starts background music, selects random song
    sound = SoundController()
    sound.play_bgm()

    # Sets menu grid size
    sc.settings_conduit['grid_size']=32
    sc.save_settings()

    # Spawn and adjust tetris game frames
    bg_tetris_one = TetrisController(window_size, [0,0], 1, fx=False)
    bg_tetris_one.centering = [0,0]
    bg_tetris_one.save_state() # Saves origin state for repeating game

    bg_tetris_two = TetrisController(window_size, [0,0], 1, fx=False)
    bg_tetris_two.centering = [bg_tetris_one.tetris_surface_size[0], 0]
    bg_tetris_two.save_state() # Saves origin state for repeating game

    bg_tetris_three = TetrisController(window_size, [0,0], 1, fx=False)
    bg_tetris_three.centering = [bg_tetris_two.tetris_surface_size[1], 0]
    bg_tetris_three.save_state() # Saves origin state for repeating game
    direction_one = 0
    direction_two = 0
    direction_three = 0

    grid_length = bg_tetris_one.tetris_width
    gravity_timer = 0
    gravity_interval = 60

    # Transparent screen
    transparent = 150
    transparent_surface = pg.Surface(window_size, pg.SRCALPHA)
    transparent_surface.fill((194, 145, 242, transparent)) # COLOR['mono_white']
    transparent_screen = pg.Rect(194, 145, 242, transparent) # COLOR['soft_purple']

    # Title animation variables
    animation_time = 0
    stretch = 128
    increase = 8

    running_menu = True
    large_font = ds.FONTS['default_large']
    title_text = ds.FONTS['title_font'].render('G5-Tetris', True, ds.COLOR['royal_jelly']) # Title text attributes
    title_position = title_text.get_rect(center=gui.grid[16][3]) # Position of where text will render

    game_button = Button( # Defines button that starts single player tetris game
                    position = gui.grid[16][7], # grid (x, y)
                    button_color=ds.COLOR['vapor_blue'],
                    text_color=ds.COLOR['powder_pink'],
                    font=large_font,
                    text='Single Player', # Text
                    hover_color=ds.COLOR['mono_white'],
                    text_outline=True,
                    inflate=[16, 16]
                    )

    game_button_two = Button( # Defines button that starts single player tetris game
                    position = gui.grid[16][10], # grid (x, y)
                    button_color=ds.COLOR['abandon_food_court_in_the_middle_of_the_night_blue'],
                    text_color=ds.COLOR['powder_pink'],
                    font=large_font,
                    text='Multiplayer', # Text
                    hover_color=ds.COLOR['mono_white'],
                    text_outline=True,
                    inflate=[16, 16]
                    )

    game_button_ai = Button( # Defines button that starts single player tetris game
                position = gui.grid[16][13], # grid (x, y)
                button_color=ds.COLOR['abandon_food_court_in_the_middle_of_the_night_blue'],
                text_color=ds.COLOR['royal_jelly'],
                font=large_font,
                text='AI Versus', # Text
                hover_color=ds.COLOR['mono_white'],
                text_outline=True,
                inflate=[16, 16]
                )

    settings_button = Button( # Defines button that navigates to user settings
                position=gui.grid[16][16], # grid (x, y)
                button_color=ds.COLOR['normal_map_blue'],
                text_color=ds.COLOR['powder_pink'],
                font=large_font,
                text='Settings', # Text
                hover_color=ds.COLOR['mono_white'],
                text_outline=True,
                inflate=[16, 16]
                )

    tutorial_button = Button( # Defines button that navigates to tutorial
            position=gui.grid[16][19], # grid (x, y)
            button_color=ds.COLOR['normal_map_blue'],
            text_color=ds.COLOR['powder_pink'],
            font=large_font,
            text='Tutorial', # Text
            hover_color=ds.COLOR['mono_white'],
            text_outline=True,
            inflate=[16, 16]
            )

    exit_button = Button( # Defines button exit button
            position=gui.grid[16][22], # grid (x, y)
            button_color=ds.COLOR['glass_purple'],
            text_color=ds.COLOR['powder_pink'],
            font=large_font,
            text='Exit', # Text
            hover_color=ds.COLOR['mono_white'],
            text_outline=True,
            inflate=[16, 16]
            )

    # Runs the main menu loop
    while running_menu:
        for event in pg.event.get():
            if event.type == pg.QUIT: return None

            elif event.type == sound.bgm_end_event: sound.bgm_ending() # End sound event

            # Listener for player button click on main menu
            elif event.type == pg.MOUSEBUTTONDOWN:

                if event.button == 1: # Left-click button

                    # One-players tetris game
                    mouse_position = pg.mouse.get_pos()
                    if game_button.clicked(mouse_position):
                        sc.settings_conduit['aspect_ratio']=1
                        sc.settings_conduit['grid_size']=12
                        sc.save_settings()
                        return ds.GAME_STATE['p1_game'] # Game state machine return

                    # Two-players tetris game
                    if game_button_two.clicked(mouse_position):
                        sc.settings_conduit['aspect_ratio']=2
                        sc.settings_conduit['grid_size']=12
                        sc.save_settings()
                        return ds.GAME_STATE['p1_game'] # Game state machine return

                    # AI versus tetris game
                    if game_button_ai.clicked(mouse_position):
                        sc.settings_conduit['aspect_ratio']=2
                        sc.settings_conduit['grid_size']=12
                        sc.save_settings()
                        return ds.GAME_STATE['ai'] # Game state machine return

                    if settings_button.clicked(mouse_position): return ds.GAME_STATE['settings'] # Leads to settings menu
                    if tutorial_button.clicked(mouse_position): return ds.GAME_STATE['tutorial'] # Leads to tutorial menu
                    if exit_button.clicked(mouse_position): return None # Exits game; Game state machine return

        gravity_timer += clock.get_time()

        # Title animation
        animation_time += clock.get_time() # Defines x-value for equation
        alpha = (math.sin(animation_time/stretch) + 1) * (increase/2) # Animation algorithm; $f(x)=(\sin(\frac{x}{x-axis_stretch}+1)\cdot{\frac{y-axis_height}{2}})$
        title_text = pg.font.Font('resources/Gabato.ttf', int(164+alpha)).render('G5-Tetris', True, ds.COLOR['royal_jelly']) # Title text attributes
        title_position = title_text.get_rect(center=gui.grid[16][3]) # Position of where text will render

        # Tetris game frame logic
        if gravity_timer >= gravity_interval:
            # Tetris frame one
            bg_tetris_one.gravity()
            if bg_tetris_one.transfer == True: direction_one = random.randint(-1,1)
            bg_tetris_one.movement()
            bg_tetris_one.next_tetrominoes.position[0] = random.randint(-1, grid_length-4)
            if random.randint(0, 12) == 1: bg_tetris_one.tetrominoes_flipping()
            if random.randint(0, 8) == 1: bg_tetris_one.movement(x_change=direction_one)

            # Tetris frame tw
            bg_tetris_two.gravity()
            if bg_tetris_two.transfer == True: direction_two = random.randint(-1,1)
            bg_tetris_two.movement()
            bg_tetris_two.next_tetrominoes.position[0] = random.randint(-1, grid_length-4)
            if random.randint(0, 12) == 1: bg_tetris_two.tetrominoes_flipping()
            if random.randint(0, 8) == 1: bg_tetris_two.movement(x_change=direction_two)

            # Tetris frame three
            bg_tetris_three.gravity()
            if bg_tetris_three.transfer == True: direction_three = random.randint(-1,1)
            bg_tetris_three.movement()
            bg_tetris_three.next_tetrominoes.position[0] = random.randint(-1, grid_length-14)
            if random.randint(0, 12) == 1: bg_tetris_three.tetrominoes_flipping()
            if random.randint(0, 8) == 1 and bg_tetris_three.current_tetrominoes.position[0] < 17:
                bg_tetris_three.movement(x_change=direction_three)

            gravity_timer = 0


        if bg_tetris_one.game_over == True:
            bg_tetris_one.game_over = False
            bg_tetris_one.load_state()
            direction_one = random.randint(-1,1)

        if bg_tetris_two.game_over == True:
            bg_tetris_two.game_over = False
            bg_tetris_two.load_state()
            direction_two = random.randint(-1,1)

        if bg_tetris_three.game_over == True:
            bg_tetris_three.game_over = False
            bg_tetris_three.load_state()
            direction_three = random.randint(-1,1)

        # Render order
        window.fill(ds.COLOR['black'])
        bg_tetris_one.render_tetris(window)
        bg_tetris_two.render_tetris(window)
        bg_tetris_three.render_tetris(window)
        window.blit(transparent_surface, (0,0))
        window.blit(title_text, title_position)
        game_button.render(window)
        game_button_two.render(window)
        game_button_ai.render(window)
        settings_button.render(window)
        tutorial_button.render(window)
        #gui.render_grid(window) # Render grid for GUI placement
        exit_button.render(window) # Render grid window for element placement
        clock.tick(60)
        pg.display.flip()
