from settingsController import settings_conduit as sc  # Settings controller
import pygame as pg
import dataStructures as ds
from dataStructures import COLOR
import numpy as np
from tetrisController import TetrisController  # Updated class name
import guiController as gui
from soundController import SoundController  # Import SoundController


def one_player(window, clock, window_size, sound_controller):
    ts = TetrisController(window_size, [0, 1])  # Use TetrisController class here

    running = True
    sound_controller.play_bgm()  # Play background music when game starts

    gravity_timer = 0  # Timer for gravity control
    gravity_interval = 500  # Milliseconds delay for each gravity step (adjust as needed)

    # Game-loop
    while running:
        # Update gravity timing
        gravity_timer += clock.get_time()
        print(f"Gravity Timer: {gravity_timer}")  # Debugging: Check gravity timer

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    print("Left key pressed")  # Debugging line
                    # Move left logic
                elif event.key == pg.K_RIGHT:
                    print("Right key pressed")  # Debugging line
                    # Move right logic
                elif event.key == pg.K_DOWN:
                    print("Down key pressed")  # Debugging line
                    # Move down logic
                elif event.key == pg.K_UP:
                    print("Rotate key pressed")  # Debugging line
                    # Rotate logic

        # Gravity-based movement
        if gravity_timer >= gravity_interval:
            ts.gravity()  # Move tetromino down automatically
            gravity_timer = 0  # Reset the timer

        # Rendering
        window.fill(COLOR['black'])
        gui.render_grid(window)
        ts.render_tetris(window)
        pg.display.flip()

        clock.tick(ds.FPS_CAP['default'])
        print("Game loop running...")  # Debugging: Game loop running

    sound_controller.stop_bgm()
    print("Exiting game loop")

    return ds.GAME_STATE['menu']
