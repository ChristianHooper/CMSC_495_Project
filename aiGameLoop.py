import settingsController as sc
from soundController import SoundController  # Import SoundController
from tetrisController import TetrisController  # Updated class name
from guiElement import element
from button import Button
from geneticAi import aiComplex
import dataStructures as ds
from dataStructures import COLOR
import guiController as gui

# Imported libraries
from pprint import pprint
import pygame as pg
import numpy as np
import threading
import queue

'''
one_player TODO: Rename function
-------------
Default called to create a single or multi-layer tetris game.
'''
def ai_player(window, clock, window_size, sound_controller):

    # Declares and defines GUI attributes and creates tetris game frame objects
    agents = sc.settings_conduit['aspect_ratio'] # Constraining variable for multiplayer & single player
    ts = TetrisController(window_size, [0, 1], agents)  # TetrisController class, game logic & rendering
    tst = TetrisController(window_size, [0, 1], agents, player_two=True)  # TetrisController class, player two
    font_slab = ds.FONTS['default_medium']
    font_tab = ds.FONTS['default_medium']
    if agents > 1: # Converts normal sized font to small font
        font_slab = ds.FONTS['default_small'] # Adjust font sizes if more than one player is playing
        font_tab = ds.FONTS['default_small']

# ////////////////////////////////////////////////////////////[Game-Over GUI]////////////////////////////////////////////////////////////////////////

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
                            COLOR['green'],
                            COLOR['white'],
                            ds.FONTS['default_medium'],
                            'Restart',
                            COLOR['red']
    )

    main_menu_button = Button(gui.grid[18][15], # Navigates to the main menu
                            COLOR['green'],
                            COLOR['white'],
                            ds.FONTS['default_medium'],
                            'Main Menu',
                            COLOR['red']
    )

    next_button = Button(gui.grid[21][15], # Navigates to the main menu
                            COLOR['green'],
                            COLOR['white'],
                            ds.FONTS['default_medium'],
                            '>',
                            COLOR['red']
    )

    input_score_menu = element(window, # GUI element for end of game window
                        gui.grid[10][4], # Location of surface, centered
                        [gui.grid_square*12, gui.grid_square*12], # Width & Height
                        fill_color=COLOR['white'],
                        border_size=[gui.grid_square/8, gui.grid_square/8], # Border width
                        border_color=(64,64,64, 128),
                        text='Enter New High Score', # Rendered text
                        font=ds.FONTS['default_medium'],
                        font_position=[gui.grid_square/2, gui.grid_square/4] # Font position on surface
    )

    score_input_box = pg.Rect(gui.grid[13][14], # Score input box to record players high score; Location
                            [gui.grid_square*6, gui.grid_square*2]) # Size

# ////////////////////////////////////////////////////////////[First-Player GUI]////////////////////////////////////////////////////////////////////////

    grab_bag = element(window, # GUI element for preview oncoming tetrominoes
                    gui.grid[int(4/agents/agents)][1], # Location of grab-bag
                    [(gui.grid_square*5)/agents, (gui.grid_square*7)/agents], # Width & Height of grab-bag
                    fill_color=(128,128,128),
                    border_size=[gui.grid_square/8, gui.grid_square/8], # Border width
                    border_color=(64,64,64), # Border color
                    font=font_slab,
                    text='Next',
                    font_position=[gui.grid_square/agents, gui.grid_square/4]
    ); next_position = [grab_bag.position[0]*agents, grab_bag.position[1]+(gui.grid_square*2.25)/agents] # The pixel position the new next_tetrominoes object will render


    score_ui = element(window, # GUI element for preview oncoming tetrominoes
                    gui.grid[int(4/agents/agents)][10], # Location of score element
                    [(gui.grid_square*5)/agents, gui.grid_square*3], # Width & Height of score element
                    fill_color=(128,128,128),
                    border_size=[gui.grid_square/8, gui.grid_square/8], # Border width
                    border_color=(64,64,64),
                    font=font_slab,
                    text='Score', # Rendered text
                    font_position=[gui.grid_square/2, (gui.grid_square/4)/agents] # Font position on surface
    ); score_subsurface = score_ui.surface.subsurface(0, 0, score_ui.bounds[0]-gui.grid_square, gui.grid_square) # Box current score will render
    subsurface_position = [score_ui.position[0]+gui.grid_square/2, int(score_ui.position[1]+(gui.grid_square*1.75))] # Score box window pixel position
    score = [0, 0] # Declaring & initializing the players' starting scores
    score_text =font_tab.render(str(score[0]), True, COLOR['black']) # Creates text surface score to be imposed on score_subsurface


    line_ui = element(window, # GUI element for viewing current line count
                    gui.grid[int(4/agents/agents)][int(15)], # Location of line counter element
                    [(gui.grid_square*5)/agents, gui.grid_square*3], # Width & Height of line counter element
                    fill_color=(128,128,128),
                    border_size=[gui.grid_square/8, gui.grid_square/8], # Border width
                    border_color=(64,64,64), # Border color
                    font=font_slab,
                    text='Line',
                    font_position=[gui.grid_square/agents, gui.grid_square/4]
    ); line_subsurface = line_ui.surface.subsurface(0, 0, line_ui.bounds[0]-gui.grid_square, gui.grid_square) # Box current line count will render
    line_position = [line_ui.position[0]+gui.grid_square/2, int(line_ui.position[1]+(gui.grid_square*1.75))] # Line counter element box pixel position
    line_count = [0, 0] # Declaring & initializing the players' line scores
    line_text = font_tab.render(str(line_count[0]), True, COLOR['black']) # Creates text surface score to be imposed on score_subsurface


    level_ui = element(window, # GUI element for viewing current line count
                    gui.grid[int(4/agents/agents)][20], # Location of line counter element
                    [(gui.grid_square*5)/agents, gui.grid_square*3], # Width & Height of line counter element
                    fill_color=(128,128,128),
                    border_size=[gui.grid_square/8, gui.grid_square/8], # Border width
                    border_color=(64,64,64), # Border color
                    text='Level',
                    font=font_slab,
                    font_position=[(gui.grid_square/2)/agents, gui.grid_square/4]
    ); level_subsurface = level_ui.surface.subsurface(0, 0, level_ui.bounds[0]-gui.grid_square, gui.grid_square) # Box current line count will render
    level_position = [level_ui.position[0]+gui.grid_square/2, int(level_ui.position[1]+(gui.grid_square*1.75))] # Line counter element box pixel position
    level = [1, 1] # Declaring & initializing the level
    level_text = font_tab.render(str(level[0]), True, COLOR['black']) # Creates text surface score to be imposed on score_subsurface

# ////////////////////////////////////////////////////////////[Second-Player GUI]////////////////////////////////////////////////////////////////////////

    if agents > 1: # If the game is multiplayer or not
        grab_bag_two = element(window, # GUI element for preview oncoming tetrominoes
                        gui.grid[int(4*agents*agents+1)][1], # Location of grab-bag
                        [(gui.grid_square*5)/agents, (gui.grid_square*7)/agents], # Width & Height of grab-bag
                        fill_color=(128,128,128),
                        border_size=[gui.grid_square/8, gui.grid_square/8], # Border width
                        border_color=(64,64,64), # Border color
                        font=font_slab,
                        text='Next',
                        font_position=[gui.grid_square/agents, gui.grid_square/4]
        ); next_position_two = [grab_bag_two.position[0]*agents, grab_bag_two.position[1]+(gui.grid_square*2.25)/agents] # The pixel position the new next_tetrominoes object will render


        score_ui_two = element(window, # GUI element for preview oncoming tetrominoes
                        gui.grid[int(4*agents*agents+1)][10], # Location of score element
                        [(gui.grid_square*5)/agents, gui.grid_square*3], # Width & Height of score element
                        fill_color=(128,128,128),
                        border_size=[gui.grid_square/8, gui.grid_square/8], # Border width
                        border_color=(64,64,64),
                        font=font_slab,
                        text='Score', # Rendered text
                        font_position=[gui.grid_square/2, (gui.grid_square/4)/agents] # Font position on surface
        ); score_subsurface_two = score_ui_two.surface.subsurface(0, 0, score_ui_two.bounds[0]-gui.grid_square, gui.grid_square) # Box current score will render
        subsurface_position_two = [score_ui_two.position[0]+gui.grid_square/2, int(score_ui_two.position[1]+(gui.grid_square*1.75))] # Score box window pixel position
        score_text_two =font_tab.render(str(score[1]), True, COLOR['black']) # Creates text surface score to be imposed on score_subsurface


        line_ui_two = element(window, # GUI element for viewing current line count
                        gui.grid[int(4*agents*agents+1)][int(15)], # Location of line counter element
                        [(gui.grid_square*5)/agents, gui.grid_square*3], # Width & Height of line counter element
                        fill_color=(128,128,128),
                        border_size=[gui.grid_square/8, gui.grid_square/8], # Border width
                        border_color=(64,64,64), # Border color
                        font=font_slab,
                        text='Line',
                        font_position=[gui.grid_square/agents, gui.grid_square/4]
        ); line_subsurface_two = line_ui_two.surface.subsurface(0, 0, line_ui_two.bounds[0]-gui.grid_square, gui.grid_square) # Box current line count will render
        line_position_two = [line_ui_two.position[0]+gui.grid_square/2, int(line_ui_two.position[1]+(gui.grid_square*1.75))] # Line counter element box pixel position
        line_text_two = font_tab.render(str(line_count[1]), True, COLOR['black']) # Creates text surface score to be imposed on score_subsurface


        level_ui_two = element(window, # GUI element for viewing current line count
                        gui.grid[int(4*agents*agents+1)][20], # Location of line counter element
                        [(gui.grid_square*5)/agents, gui.grid_square*3], # Width & Height of line counter element
                        fill_color=(128,128,128),
                        border_size=[gui.grid_square/8, gui.grid_square/8], # Border width
                        border_color=(64,64,64), # Border color
                        text='Level',
                        font=font_slab,
                        font_position=[(gui.grid_square/2)/agents, gui.grid_square/4]
        ); level_subsurface_two = level_ui_two.surface.subsurface(0, 0, level_ui_two.bounds[0]-gui.grid_square, gui.grid_square) # Box current line count will render
        level_position_two = [level_ui_two.position[0]+gui.grid_square/2, int(level_ui_two.position[1]+(gui.grid_square*1.75))] # Line counter element box pixel position
        level_text_two = font_tab.render(str(level[1]), True, COLOR['black']) # Creates text surface score to be imposed on score_subsurface


#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    '''
    conclude
    -------------
    Sequence run to conclude the game for both single and multiplayer sessions.
    '''
    def conclude(game_over, player): # player=0 is player one; player=1 is player two
        score_sort = sorted(sc.settings_conduit['scores'], key=lambda key : sc.settings_conduit['scores'][key])
        change_score = False # If a new high-score is recorded
        input_active = False
        user_text = ''
        saved_key = []

        #Searches for new high-score and sets it in JSON file
        for place, key in enumerate(score_sort):
            if sc.settings_conduit['scores'][key] < score[player]:
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

                    # Button used for entering in a new high-score
                    if event.button == 1: # Left-click button
                        mouse_position = pg.mouse.get_pos()
                        if next_button.clicked(mouse_position):

                            # Scoring logic for leaderboard
                            if user_text not in score_sort:
                                sc.settings_conduit['scores'].update({user_text: score[player]})
                                del sc.settings_conduit['scores'][saved_key[0]] # If username enter already exists, doesn't delete slot
                                score_sort[saved_key[1]] = user_text
                            elif user_text in score_sort:
                                sc.settings_conduit['scores'][user_text] = score[player]
                            sc.save_settings()
                            change_score = False

                # Keyboard input for text taking username of player for leaderboard
                if event.type == pg.KEYDOWN and input_active:
                    if event.key == pg.K_RETURN:
                        if user_text not in score_sort:
                            sc.settings_conduit['scores'].update({user_text: score[player]})
                            del sc.settings_conduit['scores'][saved_key[0]] # If username enter already exists, doesn't delete slot
                            score_sort[saved_key[1]] = user_text
                        elif user_text in score_sort:
                            sc.settings_conduit['scores'][user_text] = score[player]
                        sc.save_settings()
                        change_score = False

                    # Backspace and letter constraints
                    elif event.key == pg.K_BACKSPACE:
                        user_text = user_text[:-1]
                    elif len(user_text) < 3 and event.unicode.isalpha():  # Limits input to 3 letters
                        user_text += event.unicode.upper()

                # Defines & renders username input box
                input_score_menu.surface.fill(COLOR['grey'])
                input_score_menu.blit_update(window)
                pg.draw.rect(window, COLOR['black'], score_input_box, border_radius=10)
                pg.draw.rect(window, COLOR['white'], score_input_box, 2, border_radius=10)

                # Render text linked to high score
                score_text = ds.FONTS['default_medium'].render('New High-Score', True, COLOR['black'])
                score_number = ds.FONTS['default_large'].render(f'{score[player]}', True, COLOR['red'])
                input_text = ds.FONTS['default_large'].render(user_text, True, COLOR['white'])

                # Render text and swaps buffer
                window.blit(score_text, (score_input_box.x-gui.grid_square*2, score_input_box.y - gui.grid_square * 4))
                window.blit(score_number, (score_input_box.center[0]-gui.grid_square*2, score_input_box.y - gui.grid_square * 2))
                window.blit(input_text, (score_input_box.x+gui.grid_square, score_input_box.y+10))
                next_button.render(window)
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
                        if next_button.clicked(mouse_position): return None

            # Calculate text output for first place
            score_one = ds.FONTS['default_medium'].render(f'First Place:      {score_sort[-1]} | {sc.settings_conduit["scores"][score_sort[-1]]}', True, COLOR['black'])
            score_two = ds.FONTS['default_medium'].render(f'Second Place: {score_sort[-2]} | {sc.settings_conduit["scores"][score_sort[-2]]}', True, COLOR['black'])
            score_third = ds.FONTS['default_medium'].render(f'Third Place:     {score_sort[-3]} | {sc.settings_conduit["scores"][score_sort[-3]]}', True, COLOR['black'])
            score_fourth = ds.FONTS['default_medium'].render(f'Fourth Place:   {score_sort[-4]} | {sc.settings_conduit["scores"][score_sort[-4]]}', True, COLOR['black'])
            score_fifth = ds.FONTS['default_medium'].render(f'Fifth Place:      {score_sort[-5]} | {sc.settings_conduit["scores"][score_sort[-5]]}', True, COLOR['black'])

            # Renders leaderboard
            end_menu.blit_update(window)
            high_score_subsurface.fill(COLOR['grey'])
            high_score_subsurface.blit(high_score_text, [10, 10])
            high_score_subsurface.blit(score_one, [10, gui.grid_square*2])
            high_score_subsurface.blit(score_two, [10, gui.grid_square*3])
            high_score_subsurface.blit(score_third, [10, gui.grid_square*4])
            high_score_subsurface.blit(score_fourth, [10, gui.grid_square*5])
            high_score_subsurface.blit(score_fifth, [10, gui.grid_square*6])

            # Renders buttons & flips buffer
            restart_button.render(window)
            main_menu_button.render(window)
            if agents > 1 and player == 0: next_button.render(window)
            window.blit(high_score_subsurface, high_score_position)
            pg.display.flip()

        return None # Exiting return

    '''
    conclude
    -------------
    Function called to pause the game.
    '''
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

    '''
    selection_movement
    -------------
    Places out the selected move for the AI, from the selected COMMANDS sequence.
    '''
    def selection_movement():
        chromosome = ds.PRIME # Defines the chromosome
        read = False
        moving = True
        move_list = [] # Lists of possible moves over one sequence
        tst.save_state()
        selection_interval = 100
        selection_timer = 0

        while True:
            for COMMANDS in SEQUENCE: # Loops through all possible move-sets
                moving = True # Sets loop for tetrominoes movement
                tst.load_state() # Resets game for optimal movement search
                if not tst.current_tetrominoes.static and read == False: # Run each ACTION in COMMANDS sequence
                    for ACTION in COMMANDS:

                        # Rotate logic player two
                        if ACTION == 'ROTATE': # Up key press
                            tst.tetrominoes_flipping()

                        if ACTION == 'LEFT': # Move left
                            tst.movement(x_change=-1)

                        if ACTION == 'RIGHT': # Move right
                            tst.movement(x_change=1)

                        if ACTION == 'DOWN': # Move down
                            tst.gravity()
                            score[1] += 1

                        tst.movement() # Checks if tetrominoes should move to a static block
                        #tst.load_state()
                    read = True # Marks COMMANDS sequence as read
                #////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

                while moving: # If the tetrominoes is currently moving

                    if tst.transfer == True:
                        read = False
                        moving = False

                        tst.movement(y_change=1, ai_eval=True)
                        tst.load_state()

                        move_list.append(tst.score(chromosome)) # Scores possible movement choice
                        continue


                    # Move tetromino down on y-axis
                    tst.render_tetris(window)
                    tst.gravity()


                    if tst.cleared_rows: # Second player line cleared
                        scores = tst.line_score(score[1], line_count[1]) # Calculates new scores and lien count
                        score[1] = score[1] + scores[1] # Sets new score
                        line_count[1] = line_count[1] + line_count[1] # Sets new line count
                        if line_count[1] - (10*(level[1])) >= 0:
                            level[1] = level[1] + 1



            move_array = np.array(move_list) # Defines the score for call possible moves in COMMANDS sequence
            #print(move_array); print()

            selected_score = np.max(move_array) # Finds optimal move-set; selects list of COMMANDS sequence, gets highest scores
            #3pprint(selected_score); print()

            selected_index = np.random.choice(np.where(move_array == selected_score)[0]) # Selects optimal move; single COMMANDS sequence
            #pprint(selected_index); print()
            tst.game_over = False

            move_queue.put(ai.movement_sequence[selected_index]) # Safely passes movement commands to primary thread
            return


#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    running = True # Defines if the game-loop is running
    paused = False # If the game is paused
    game_over = True # Defines if the game is in a game over state
    read = False # If movement ACTIONS from the COMMANDS sequence have been read
    sound_controller.play_bgm()  # Play background music when game starts

    # AI
    #chromosome = ds.PRIME # Defines the chromosome
    move_selection = None # List of movement commands for AI tetrominoes placement, x-axis movement
    move_queue = queue.Queue()

    ai_timer = 0
    ai_interval = 100



    agent_loop = True # Defines agent loop access
    movement_loop = True
    movement_number = -1 # Holds the movement number of the agent in agent_loop
    ai = aiComplex() # Made just for movement sequence TODO: Replace
    SEQUENCE = ai.movement_sequence # Defines the sequence of all possible moves an agent can play

    selection_clock = pg.time.Clock() # Starts game clock

    # Time variables used with clock ticks to meter plummet keypress calls
    plummet_timer = 0
    #plummet_timer_two = 0

    # Time variables used with clock ticks to define gravity speed
    gravity_timer = 0  # Timer for gravity control
    gravity_interval = ds.GRAVITY_SPEED # Milliseconds delay for each gravity step

    # Time variables used with clock ticks to meter keypress calls for tetrominoes movement
    key_press_timer = 0
    key_press_timer_two = 0
    key_press_interval = 100 # Milliseconds delay for each gravity step
    key_press_interval_two = 100 # Milliseconds delay for each gravity step

    pg.key.set_repeat(100, 100) # Allows for repeated movement calls when keys are held down, increase tetrominoes' speed


    # Creates a thread object for AI processing
    selection_thread = threading.Thread(target=selection_movement)
    selection_thread.start()
    decimate_thread = threading.Event()

#/////////////////////////////////////////////////////////////[Game-Loop]///////////////////////////////////////////////////////////////////////

    # Game-loop
    while running:

        # Sets update timer variables
        ai_timer += clock.get_time()
        gravity_timer += clock.get_time() # Update gravity timing
        key_press_timer += clock.get_time() # Update player one timer for key presses
        key_press_timer_two += clock.get_time() # Update player two timer for key presses
        plummet_timer += clock.get_time() # Update player one timer for plummet calls
        #plummet_timer_two += clock.get_time() # Update player two timer for plummet calls

        for event in pg.event.get():
            if event.type == pg.QUIT:
                decimate_thread.set()
                running = False

            elif event.type == pg.KEYDOWN: # Checks for a key press event

                if event.key == pg.K_SPACE: # Pauses game
                    paused = True # Sets pause condition to true
                    paused = pause_loop(paused) # Sets pause condition to false

#/////////////////////////////////////////////////////////////[Player-One Keys]///////////////////////////////////////////////////////////////////////

        keys = pg.key.get_pressed() # Create an object for key press retrieval

        # First player movement logic
        if not ts.current_tetrominoes.static and not ts.game_over:
            # Move left logic player one
            if keys[pg.K_a]: # Left key press
                if key_press_timer > key_press_interval:
                    ts.movement(x_change=-1)
                    key_press_timer = 0

            # Move right logic player one
            if keys[pg.K_d]: # Right key press
                if key_press_timer >= key_press_interval:
                    ts.movement(x_change=1)
                    key_press_timer = 0

            # Move down logic player one
            if keys[pg.K_s]: # Down key press
                if key_press_timer >= key_press_interval:
                    ts.gravity()
                    score[0] += 1
                    score_text = font_tab.render(str(score[0]), True, COLOR['black'])
                    key_press_timer = 0

            # Rotate logic player one
            if keys[pg.K_w]: # Up key press
                #pg.key.set_repeat(gravity_interval, 100) # Allows for repeated movement calls when keys are held down, increase tetrominoes' speed
                if key_press_timer >= key_press_interval:
                    ts.tetrominoes_flipping()
                    key_press_timer = 0

            if keys[pg.K_e]: # Up key press
                if key_press_timer >= key_press_interval:
                    ts.plummet()
                    ts.update_grid()
                    key_press_timer = 0
                    plummet_timer = 0

            ts.movement() # Checks if tetrominoes should move to a static block

#/////////////////////////////////////////////////////////////[Player-Two Keys]///////////////////////////////////////////////////////////////////////

        # Run AI selected movement ACTIONS
        #selection_thread.join() # May not need this join thread command; stops main thread processing at this point!

        # Tries to grab movement ACTIONS from movement selection thread
        try: move_selection = move_queue.get_nowait()
        except queue.Empty: pass

        if move_selection != None and not tst.current_tetrominoes.static and not tst.game_over and not read:
            #print('move_selection:', move_selection)
            #print('tst.current_tetrominoes.static', tst.current_tetrominoes.static)
            #print('tst.game_over', tst.game_over)
            #print('read', read)
            #tst.load_state()
            for ACTIONS in move_selection:

                # Move left logic player two
                if ACTIONS == 'LEFT': # Left key press
                    tst.movement(x_change=-1)
                    #print('LEFT')

                if ACTIONS == 'RIGHT': # Right key press
                    tst.movement(x_change=1)
                    #print('RIGHT')

                # Rotate logic player two
                if ACTIONS == 'ROTATE': # Up key press
                    tst.tetrominoes_flipping()
                    #print('ROTATE')
                '''
                if keys[pg.K_RSHIFT]: # Up key press
                    if key_press_timer_two >= key_press_interval_two:
                        tst.plummet()
                        tst.update_grid()
                        key_press_timer_two = 0
                        plummet_timer_two = 0
                '''
                #print('APRI TET POS: ', tst.current_tetrominoes.position)
            tst.movement() # Checks if tetrominoes should move to a static block
            read = True


#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

        # Gravity-based movement
        if plummet_timer >= gravity_interval: ts.current_tetrominoes.plumbed = False
        if gravity_timer >= gravity_interval:

            if not ts.game_over:
                ts.movement(y_change=1) # Move tetromino down on y-axis
                ts.gravity()


            if ts.cleared_rows: # Ran when a line is cleared to update score variables
                scores = ts.line_score(score[0], line_count[0]) # Calculates new scores and lien count
                score[0] = score[0] + scores[0] # Sets new score
                line_count[0] = line_count[0] + scores[1] # Sets new line count
                score_text = font_tab.render(str(score[0]), True, COLOR['black'])
                line_text = font_tab.render(str(line_count[0]), True, COLOR['black'])
                if line_count[0] - (10*(level[0])) >= 0:
                    level[0] = level[0] + 1
                    gravity_interval = gravity_interval - 25
                    level_text = font_tab.render(str(level[0]), True, COLOR['black'])

            ts.update_grid() # Updates grid of mechanics and rendering based upon movement changes
            if move_selection != None: tst.update_grid() # Updates grid of mechanics and rendering based upon movement changes
            gravity_timer = 0  # Resets the timer
            key_press_timer = 0 # Resets the timer
            key_press_timer_two = 0

        if ai_timer >= ai_interval:

            if move_selection != None and not tst.game_over:
                tst.movement() # Move tetromino down on y-axis
                tst.gravity()
                score[1] += 1
                score_text_two = font_tab.render(str(score[1]), True, COLOR['black'])

                if tst.transfer == True:
                    # Creates a thread object for AI processing
                    move_selection = None # REsets move selection list
                    read = False
                    tst.save_state() # Save tetrominoes that was just placed
                    tst.movement()
                    selection_thread = threading.Thread(target=selection_movement)
                    selection_thread.start()

            # NEEDS TO MOVE WHEN MAKING AI CALCULATIONS
            if move_selection != None and tst.cleared_rows:
                scores = tst.line_score(score[1], line_count[1]) # Calculates new scores and lien count
                score[1] = score[1] + scores[1] # Sets new score
                line_count[1] = line_count[1] + line_count[1] # Sets new line count
                score_text_two = font_tab.render(str(score[1]), True, COLOR['black'])
                line_text_two = font_tab.render(str(line_count[1]), True, COLOR['black'])
                if line_count[1] - (10*(level[1])) >= 0:
                    level[1] = level[1] + 1
                    #gravity_interval = gravity_interval - 25 # Not needed, handled in first player
                    level_text_two = font_tab.render(str(level[1]), True, COLOR['black'])
            ai_timer = 0

        # Rendering
        window.fill(COLOR['black'])
        gui.render_grid(window) # Render GUI placement grid tool
        ts.render_tetris(window) # Render the entire tetris game frame

        if move_selection != None: tst.render_tetris(window) # Render the entire tetris game frame
        # tst.render_tetris(window) # Render the entire tetris game frame


        # Render grab-bag
        grab_bag.blit_update(window)
        ts.render_next_tetromino(window, next_position) # Display the next tetromino

        if agents > 1:
            # Render score UI
            grab_bag_two.blit_update(window)
            if move_selection != None: tst.render_next_tetromino(window, next_position_two) # Display the next tetromino

            # Render line score UI
            score_ui_two.blit_update(window)
            score_subsurface_two.fill((200, 200, 245))
            score_subsurface_two.blit(score_text_two, [10, 10])
            window.blit(score_subsurface_two, subsurface_position_two)

            # Render line score UI
            line_ui_two.blit_update(window)
            line_subsurface_two.fill((200, 200, 245))
            line_subsurface_two.blit(line_text, [10,10])
            window.blit(line_subsurface_two, line_position_two)

            # Render current level UI
            level_ui_two.blit_update(window)
            level_subsurface_two.fill((200, 200, 245))
            level_subsurface_two.blit(level_text_two, [10,10])
            window.blit(level_subsurface_two, level_position_two)

        # Player One
        # Render score UI
        score_ui.blit_update(window)
        score_subsurface.fill((200, 200, 245))
        score_subsurface.blit(score_text, [10, 1])
        window.blit(score_subsurface, subsurface_position)

        # Render line score UI
        line_ui.blit_update(window)
        line_subsurface.fill((200, 200, 245))
        line_subsurface.blit(line_text, [10, 1])
        window.blit(line_subsurface, line_position)

        # Render current level UI
        level_ui.blit_update(window)
        level_subsurface.fill((200, 200, 245))
        level_subsurface.blit(level_text, [10, 1])
        window.blit(level_subsurface, level_position)

        pg.display.flip()

        # Checks if game is over form single and multi-player sessions
        #if agents > 1 and ts.game_over and tst.game_over: conclude(game_over, 0); return conclude(game_over, 1)
        if ts.game_over: return conclude(game_over, 0) # Checks is game is over

        #clock.tick(ds.FPS_CAP['default']) # Adheres game ticks to set FPS
        print(f"SPF: {clock.tick() / 1000}", end="\r")
    sound_controller.stop_bgm()
    print("Exiting game loop")

