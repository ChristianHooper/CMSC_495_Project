import settingsController as sc
#from settingsController import settings_conduit as sc  # Settings controller
from soundController import SoundController  # Import SoundController
from tetrisController import TetrisController  # Updated class name
from guiElement import element
from button import Button
import pygame as pg
import dataStructures as ds
from dataStructures import COLOR
import numpy as np
import guiController as gui


def one_player(window, clock, window_size, sound_controller):

    ts = TetrisController(window_size, [0, 1])  # TetrisController class, game logic & rendering

    end_menu = element(window, # GUI element for end of game window
                    gui.grid[10][4], # Location of surface, centered
                    [gui.grid_square*12, gui.grid_square*12], # Width & Height
                    fill_color=COLOR['white'],
                    border_size=[gui.grid_square/8, gui.grid_square/8], # Border width
                    border_color=(64,64,64, 128),
                    text='Game Over', # Rendered text
                    font_position=[gui.grid_square/2, gui.grid_square/4] # Font position on surface
    ); high_score_subsurface = end_menu.surface.subsurface(0, 0, end_menu.bounds[0]-gui.grid_square, (end_menu.bounds[1]/1.5)) # Box for render high scores
    high_score_position = [end_menu.position[0]+gui.grid_square/2, int(end_menu.position[1]+(gui.grid_square*1.75))] # Score box window pixel position
    high_score_text = ds.FONTS['default_medium'].render('High Scores', True, COLOR['white']) # Creates text surface score to be imposed on score_subsurface

    restart_button = Button(gui.grid[13][15], # Restart game button
                            COLOR['grey'],
                            COLOR['black'],
                            ds.FONTS['default_medium'],
                            'Restart',
                            COLOR['red']
    )
    main_menu_button = Button(gui.grid[18][15], # Navigates to the main menu
                            COLOR['grey'],
                            COLOR['black'],
                            ds.FONTS['default_medium'],
                            'Main Menu',
                            COLOR['red']
    )


    input_score_menu = element(window, # GUI element for end of game window
                        gui.grid[10][4], # Location of surface, centered
                        [gui.grid_square*12, gui.grid_square*16], # Width & Height
                        fill_color=COLOR['white'],
                        border_size=[gui.grid_square/8, gui.grid_square/8], # Border width
                        border_color=(64,64,64, 128),
                        text='Enter New High Score', # Rendered text
                        font=ds.FONTS['default_medium'],
                        font_position=[gui.grid_square/2, gui.grid_square/4] # Font position on surface
    )
    score_input_box = pg.Rect(gui.grid[13][14], # Location
                            [gui.grid_square*6, gui.grid_square*2]) # Size


    grab_bag = element(window, # GUI element for preview oncoming tetrominoes
                    gui.grid[4][1], # Location of grab-bag
                    [gui.grid_square*5, gui.grid_square*7], # Width & Height of grab-bag
                    fill_color=(128,128,128),
                    border_size=[gui.grid_square/8, gui.grid_square/8], # Border width
                    border_color=(64,64,64), # Border color
                    text='Next',
                    font_position=[gui.grid_square, gui.grid_square/4]
    ); next_position = [grab_bag.position[0], grab_bag.position[1]+(gui.grid_square*2.25)] # The pixel position the new next_tetrominoes object will render


    score_ui = element(window, # GUI element for preview oncoming tetrominoes
                    gui.grid[4][10], # Location of score element
                    [gui.grid_square*5, gui.grid_square*3], # Width & Height of score element
                    fill_color=(128,128,128),
                    border_size=[gui.grid_square/8, gui.grid_square/8], # Border width
                    border_color=(64,64,64),
                    text='Score', # Rendered text
                    font_position=[gui.grid_square/2, gui.grid_square/4] # Font position on surface
    ); score_subsurface = score_ui.surface.subsurface(0, 0, score_ui.bounds[0]-gui.grid_square, gui.grid_square) # Box current score will render
    subsurface_position = [score_ui.position[0]+gui.grid_square/2, int(score_ui.position[1]+(gui.grid_square*1.75))] # Score box window pixel position
    score = [0, 0] # Declaring & initializing the players' starting scores
    score_text = ds.FONTS['default_medium'].render(str(score[0]), True, COLOR['black']) # Creates text surface score to be imposed on score_subsurface


    line_ui = element(window, # GUI element for viewing current line count
                    gui.grid[4][15], # Location of line counter element
                    [gui.grid_square*5, gui.grid_square*3], # Width & Height of line counter element
                    fill_color=(128,128,128),
                    border_size=[gui.grid_square/8, gui.grid_square/8], # Border width
                    border_color=(64,64,64), # Border color
                    text='Line',
                    font_position=[gui.grid_square, gui.grid_square/4]
    ); line_subsurface = line_ui.surface.subsurface(0, 0, line_ui.bounds[0]-gui.grid_square, gui.grid_square) # Box current line count will render
    line_position = [line_ui.position[0]+gui.grid_square/2, int(line_ui.position[1]+(gui.grid_square*1.75))] # Line counter element box pixel position
    line_count = [0, 0] # Declaring & initializing the players' line scores
    line_text = ds.FONTS['default_medium'].render(str(line_count[0]), True, COLOR['black']) # Creates text surface score to be imposed on score_subsurface


    level_ui = element(window, # GUI element for viewing current line count
                    gui.grid[4][20], # Location of line counter element
                    [gui.grid_square*5, gui.grid_square*3], # Width & Height of line counter element
                    fill_color=(128,128,128),
                    border_size=[gui.grid_square/8, gui.grid_square/8], # Border width
                    border_color=(64,64,64), # Border color
                    text='Level',
                    font_position=[gui.grid_square/2, gui.grid_square/4]
    ); level_subsurface = level_ui.surface.subsurface(0, 0, level_ui.bounds[0]-gui.grid_square, gui.grid_square) # Box current line count will render
    level_position = [level_ui.position[0]+gui.grid_square/2, int(level_ui.position[1]+(gui.grid_square*1.75))] # Line counter element box pixel position
    level = [1, 1] # Declaring & initializing the level
    level_text = ds.FONTS['default_medium'].render(str(level[0]), True, COLOR['black']) # Creates text surface score to be imposed on score_subsurface

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    # Function called to run end-game sequence
    def conclude(game_over):
        score_sort = sorted(sc.settings_conduit['scores'], key=lambda key : sc.settings_conduit['scores'][key])
        change_score = False # If a new high-score is recorded
        input_active = False
        user_text = ''
        saved_key = []

        #Searches for new high-score and sets it in JSON file
        for place, key in enumerate(score_sort):
            if sc.settings_conduit['scores'][key] < score[0]:
                saved_key = [key, place]
                change_score = True
                break

        # User entering in new score GUI
        while change_score: # Changing score loop
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return None # Quits game

                if event.type == pg.MOUSEBUTTONDOWN: # Detect if the mouse click
                    if score_input_box.collidepoint(event.pos): input_active = True  # Activate the input box
                    else: input_active = False
                    #if ok_button_rect.collidepoint(event.pos):
                        #print(f"Entered Initials: {user_text}")
                        #user_text = ''  # Reset text input if needed
                        # You can add additional functionality for when "OK" is clicked

                # Keyboard input for text
                if event.type == pg.KEYDOWN and input_active:
                    if event.key == pg.K_RETURN:
                        if user_text not in score_sort:
                            sc.settings_conduit['scores'].update({user_text: score[0]})
                            del sc.settings_conduit['scores'][saved_key[0]] # If username enter already exists, doesn't delete slot
                            score_sort[saved_key[1]] = user_text
                        elif user_text in score_sort:
                            sc.settings_conduit['scores'][user_text] = score[0]
                            print('AP:', score_sort)
                            print('DIS: ', sc.settings_conduit['scores'])
                            #score_sort = sorted(sc.settings_conduit['scores'], key=lambda key : sc.settings_conduit['scores'][key])
                        sc.save_settings()
                        change_score = False


                    elif event.key == pg.K_BACKSPACE:
                        user_text = user_text[:-1]
                    elif len(user_text) < 3 and event.unicode.isalpha():  # Limits input to 3 letters
                        user_text += event.unicode.upper()

                input_score_menu.surface.fill(COLOR['grey'])
                input_score_menu.blit_update(window)
                pg.draw.rect(window, COLOR['black'], score_input_box, border_radius=10)
                pg.draw.rect(window, COLOR['white'], score_input_box, 2, border_radius=10)

                score_text = ds.FONTS['default_large'].render('New High-Score', True, COLOR['black'])
                score_number = ds.FONTS['default_large'].render(f'{score[0]}', True, COLOR['red'])
                input_text = ds.FONTS['default_large'].render(user_text, True, COLOR['white'])

                window.blit(score_text, (score_input_box.x-gui.grid_square*2, score_input_box.y - gui.grid_square * 4))
                window.blit(score_number, (score_input_box.center[0]-gui.grid_square*2, score_input_box.y - gui.grid_square * 2))
                window.blit(input_text, (score_input_box.x+gui.grid_square, score_input_box.y+10))
                #input_score_menu.surface.blit(input_score_menu, [100, 100])
                pg.display.flip()

        score_sort = sorted(sc.settings_conduit['scores'], key=lambda key : sc.settings_conduit['scores'][key]) # Resorts scores

        # Viewing current top scores
        while game_over: # Game over loop
            for event in pg.event.get(): # Check for game exit
                if event.type == pg.QUIT:
                    game_over = False # Unpauses game

                # Listener for player button click
                elif event.type == pg.MOUSEBUTTONDOWN:

                    if event.button == 1: # Left-click button
                        mouse_position = pg.mouse.get_pos()
                        if restart_button.clicked(mouse_position): return ds.GAME_STATE['p1_game']
                        if main_menu_button.clicked(mouse_position): return ds.GAME_STATE['menu']

            # Calculate text output for first place
            score_one = ds.FONTS['default_medium'].render(f'First Place:      {score_sort[-1]} | {sc.settings_conduit["scores"][score_sort[-1]]}', True, COLOR['black'])
            score_two = ds.FONTS['default_medium'].render(f'Second Place: {score_sort[-2]} | {sc.settings_conduit["scores"][score_sort[-2]]}', True, COLOR['black'])
            score_third = ds.FONTS['default_medium'].render(f'Third Place:     {score_sort[-3]} | {sc.settings_conduit["scores"][score_sort[-3]]}', True, COLOR['black'])
            score_fourth = ds.FONTS['default_medium'].render(f'Fourth Place:   {score_sort[-4]} | {sc.settings_conduit["scores"][score_sort[-4]]}', True, COLOR['black'])
            score_fifth = ds.FONTS['default_medium'].render(f'Fifth Place:      {score_sort[-5]} | {sc.settings_conduit["scores"][score_sort[-5]]}', True, COLOR['black'])

            end_menu.blit_update(window)
            high_score_subsurface.fill(COLOR['grey'])
            high_score_subsurface.blit(high_score_text, [10, 10])
            high_score_subsurface.blit(score_one, [10, gui.grid_square*2])
            high_score_subsurface.blit(score_two, [10, gui.grid_square*3])
            high_score_subsurface.blit(score_third, [10, gui.grid_square*4])
            high_score_subsurface.blit(score_fourth, [10, gui.grid_square*5])
            high_score_subsurface.blit(score_fifth, [10, gui.grid_square*6])

            restart_button.render(window)
            main_menu_button.render(window)

            window.blit(high_score_subsurface, high_score_position)
            pg.display.flip()

        return None # Exiting return


    # Function called to pause the game
    def pause_loop(pause):
        while pause: # Defines pause loop
            for event in pg.event.get(): # Check for game exit
                if event.type == pg.QUIT:
                    pause = False # Unpauses game

                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        pause = False # Unpauses game

            pause_text = ds.FONTS['default_large'].render("[Game Paused]", False, COLOR['white']) # Font object rendered for pausing game
            window.blit(pause_text, [gui.grid[16][10][0] - pause_text.get_width()/2 , gui.grid[16][10][1]]) # Centered font render
            pg.display.flip()
        return False # Sets pause condition to false with return

    running = True
    paused = False # If the game is paused
    game_over = True
    sound_controller.play_bgm()  # Play background music when game starts

    gravity_timer = 0  # Timer for gravity control
    gravity_interval = ds.GRAVITY_SPEED # Milliseconds delay for each gravity step
    pg.key.set_repeat(500, 25) # Allows for repeated movement calls when keys are held down, increase tetrominoes' speed

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    # Game-loop
    while running:

        gravity_timer += clock.get_time() # Update gravity timing

        for event in pg.event.get():
            pg.key.set_repeat(100, 20)
            if event.type == pg.QUIT:
                running = False

            elif event.type == pg.KEYDOWN: # Checks for a key press event
                # Pauses game
                if event.key == pg.K_SPACE:
                    paused = True # Sets pause condition to true
                    paused = pause_loop(paused) # Sets pause condition to false

                # Move left logic
                if event.key == pg.K_LEFT and ts.current_tetrominoes.static == False: # Left key press
                    ts.movement(x_change=-1)

                # Move right logic
                elif event.key == pg.K_RIGHT and ts.current_tetrominoes.static == False: # Right key press
                    ts.movement(x_change=1)

                # Move down logic
                elif event.key == pg.K_DOWN and ts.current_tetrominoes.static == False: # Down key press
                    ts.movement(y_change=1)
                    score[0] += 1
                    score_text = ds.FONTS['default_medium'].render(str(score[0]), True, COLOR['black'])

                # Rotate logic
                elif event.key == pg.K_UP and ts.current_tetrominoes.static == False: # Up key press
                    pg.key.set_repeat(500, 500) # Allows for repeated movement calls when keys are held down, increase tetrominoes' speed
                    ts.tetrominoes_flipping()

        # Gravity-based movement
        if gravity_timer >= gravity_interval:
            ts.movement(y_change=1) # Move tetromino down on y-axis

            if ts.cleared_rows:
                scores = ts.line_score(score[0], line_count[0]) # Calculates new scores and lien count
                score[0] = score[0] + scores[0] # Sets new score
                line_count[0] = line_count[0] + scores[1] # Sets new line count

                score_text = ds.FONTS['default_medium'].render(str(score[0]), True, COLOR['black'])
                line_text = ds.FONTS['default_medium'].render(str(line_count[0]), True, COLOR['black'])

                if line_count[0] - (10*(level[0])) >= 0:
                    level[0] = level[0] + 1
                    gravity_interval = gravity_interval - 25
                    level_text = ds.FONTS['default_medium'].render(str(level[0]), True, COLOR['black'])

            ts.update_grid() # Updates grid of mechanics and rendering based upon movement changes
            gravity_timer = 0  # Resets the timer
            #for row in ts.tetris_grid: print(f"{row}") # Prints a terminal based tetris grid

        # Rendering
        window.fill(COLOR['black'])
        gui.render_grid(window) # Render GUI placement grid tool
        ts.render_tetris(window) # Render the entire tetris game frame

        # Render grab-bag
        grab_bag.blit_update(window)
        ts.render_next_tetromino(window, next_position) # Display the next tetromino

        # Render score UI
        score_ui.blit_update(window)
        score_subsurface.fill((200, 200, 245))
        score_subsurface.blit(score_text, [10, 10])
        window.blit(score_subsurface, subsurface_position)

        # Render line score UI
        line_ui.blit_update(window)
        line_subsurface.fill((200, 200, 245))
        line_subsurface.blit(line_text, [10,10])
        window.blit(line_subsurface, line_position)

        # Render current level UI
        level_ui.blit_update(window)
        level_subsurface.fill((200, 200, 245))
        level_subsurface.blit(level_text, [10,10])
        window.blit(level_subsurface, level_position)

        pg.display.flip()

        if ts.game_over: return conclude(game_over) # Checks is game is over

        clock.tick(ds.FPS_CAP['default']) # Adheres game ticks to set FPS

    sound_controller.stop_bgm()
    print("Exiting game loop")

