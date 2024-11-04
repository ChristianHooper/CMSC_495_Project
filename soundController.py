import pygame as pg


class SoundController:
    def __init__(self):
        pg.mixer.init()

        # Use `pygame.mixer.music` for the background music
        self.bgm_path = 'sounds/background_music.mp3'  # File path to the background music
        self.line_clear_sound = pg.mixer.Sound('sounds/clear_line.wav')
        self.game_over_sound = pg.mixer.Sound('sounds/game_over.wav')
        self.rotate_sound = pg.mixer.Sound('sounds/rotate.wav')

    def play_bgm(self):
        print()
        pg.mixer.music.load(self.bgm_path)
        pg.mixer.music.play(loops=-1)

    def stop_bgm(self):
        pg.mixer.music.stop()

    def play_line_clear(self):
        self.line_clear_sound.play()

    def play_game_over(self):
        self.game_over_sound.play()

    def play_rotate(self):
        self.rotate_sound.play()
